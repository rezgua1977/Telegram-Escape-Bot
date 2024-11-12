#rating_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from db_handler import save_player_data, get_player_data  # Annahme: Die Datenbank speichert auch Bewertungen
from email_handler import send_email  # Import der E-Mail-Funktion für Benachrichtigungen
from logger_config import logger  # Importiert den zentralen Logger aus logger_config.py

# Funktion zum Senden der Bewertungsumfrage am Spielende
async def send_survey(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    keyboard = [
        [InlineKeyboardButton("⭐ 1", callback_data='rating_1')],
        [InlineKeyboardButton("⭐⭐ 2", callback_data='rating_2')],
        [InlineKeyboardButton("⭐⭐⭐ 3", callback_data='rating_3')],
        [InlineKeyboardButton("⭐⭐⭐⭐ 4", callback_data='rating_4')],
        [InlineKeyboardButton("⭐⭐⭐⭐⭐ 5", callback_data='rating_5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text="Vielen Dank fürs Spielen! Bitte gib eine Bewertung ab, um uns zu helfen, das Spiel zu verbessern.",
        reply_markup=reply_markup
    )
    logger.info(f"Bewertungsumfrage an Chat {chat_id} gesendet.")

# Callback-Funktion zur Verarbeitung der Bewertungsauswahl und zum Senden einer E-Mail
async def rating_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Bewertung extrahieren und auf Gültigkeit prüfen
    try:
        rating_value = int(query.data.split('_')[1])
        if rating_value not in range(1, 6):
            raise ValueError("Ungültiger Bewertungswert.")
    except (IndexError, ValueError) as e:
        await query.edit_message_text("Ungültige Bewertung. Bitte versuche es erneut.")
        logger.error(f"Ungültiger Bewertungswert erhalten: {query.data} für Chat {query.message.chat.id}: {e}")
        return

    # Speichern der Bewertung in der Datenbank
    chat_id = query.message.chat.id
    try:
        # Teamname abrufen, falls vorhanden
        team_name = get_player_data(chat_id, "team_name") or "Unbekanntes Team"
        
        # Speichern der Bewertung in der Datenbank
        save_player_data(chat_id, rating=rating_value)
        await query.edit_message_text(f"Vielen Dank für deine Bewertung von {rating_value} Stern(en)! ⭐")
        logger.info(f"Bewertung von {rating_value} für Spiel von Chat {chat_id} erfolgreich gespeichert.")
        
        # E-Mail senden
        subject = f"Spielbewertung für Team {team_name}"
        body = f"Team {team_name} hat das Spiel mit {rating_value} Stern(en) bewertet."
        send_email(subject, body)
        logger.info(f"E-Mail über Bewertung von {rating_value} Sternen für Team {team_name} erfolgreich gesendet.")
        
    except Exception as e:
        await query.edit_message_text("Fehler beim Speichern der Bewertung. Bitte versuche es später erneut.")
        logger.error(f"Fehler beim Speichern der Bewertung für Chat {chat_id}: {e}")
