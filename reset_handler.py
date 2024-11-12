#reset_handler.py
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from db_handler import save_player_data, get_player_data, delete_player_data
from logger_config import logger  # Importiert den zentralen Logger aus logger_config.py

# Pfad zum Titelbild
TITLECARD_PATH = "Bilder/Titelkarte.jpg"

# Funktion zur Bestätigung des vollständigen Resets
async def confirm_reset(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    # Abbrechen aller `schedule_hint`-Tasks für diesen Chat
    for task in asyncio.all_tasks():
        if task.get_name() == f"hint_task_{chat_id}":
            task.cancel()
            logger.info(f"Hint-Task für Chat {chat_id} wurde abgebrochen.")

    # Vollständiges Löschen der Spielerdaten und setzen auf Initialwerte
    try:
        delete_player_data(chat_id)  # Funktion zur vollständigen Löschung der Spielerdaten

        # Überprüfen, ob die Daten erfolgreich gelöscht wurden
        if not get_player_data(chat_id, "game_active"):
            logger.info(f"Spielerdaten für Chat {chat_id} erfolgreich zurückgesetzt.")

            # Bild senden
            if os.path.exists(TITLECARD_PATH):
                with open(TITLECARD_PATH, 'rb') as photo:
                    await context.bot.send_photo(chat_id=chat_id, photo=photo)
            else:
                logger.error(f"Bild {TITLECARD_PATH} nicht gefunden.")
                await context.bot.send_message(chat_id=chat_id, text="🔔 Die Einführung wird ohne Titelbild fortgesetzt.")
            
            # Begrüßungsnachricht und Abfrage des Teamnamens senden
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    "✨ <b>Willkommen im Rätsel möchten gelöst, nicht alle Türen geöffnet werden.</b>\n\n"
                    "📜 <b>Wichtige Hinweise für eure Reise:</b>\n"
                    "1. <b>Teamname festlegen</b>: Gebt <i>euren geheimen Teamnamen ohne das Wort Team</i> ein, um das Tor in die Welt der Illusionen zu öffnen.\n"
                    "2. <b>Ruft nach Unterstützung</b>: Gebt <code>/help</code> ein, falls die Dunkelheit euch überwältigen sollte.\n"
                    "3. <b>Zurücksetzen</b>: Gebt <code>/reset</code> ein, um das Abenteuer von Neuem zu beginnen, solltet ihr im Labyrinth der Geheimnisse verloren gehen.\n\n"
                    "✨ <b>Möge das Schicksal euch wohlgesonnen sein</b> und euch durch die Nebel der Ungewissheit führen. <b>Viel Erfolg auf eurer Reise ins Unbekannte!</b> ✨"
                ),
                parse_mode="HTML"
            )

    except Exception as e:
        logger.error(f"Fehler beim Löschen der Spielerdaten für Chat {chat_id}: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Es gab ein Problem beim Zurücksetzen des Spiels. Bitte versuche es erneut oder kontaktiere den Support.")

# Funktion zum Anzeigen des Reset-Bestätigungsdialogs
async def reset(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Ja", callback_data="confirm_reset"),
            InlineKeyboardButton("Nein", callback_data="cancel_reset"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "⚠️ Bist du sicher, dass du deinen Fortschritt zurücksetzen möchtest?",
        reply_markup=reply_markup,
    )
    logger.info("Reset-Bestätigungsdialog angezeigt.")

# Funktion zum Abbruch des Reset-Bestätigungsdialogs
async def cancel_reset(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🔙 Spielstand bleibt erhalten. Weiter geht's!")
    logger.info("Reset-Abbruch durch den Benutzer bestätigt.")
