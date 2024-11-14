#riddle_handler.py
import os
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CallbackContext
from db_handler import save_player_data, get_player_data
from email_handler import send_end_game_email
from certificate_generator import generate_certificate
from logger_config import logger  # Importiert den zentralen Logger aus logger_config.py

# Ordner des aktuellen Skripts und Titelkarten-Bildpfad
current_directory = os.path.dirname(os.path.abspath(__file__))
TITLECARD_PATH = "/root/telegram-escape-bot/Bilder/Titelkarte.jpg"

# Lösungen für die einzelnen Rätsel
solutions = {
    1: "text",
    2: "zahl",
    3: "456",
    4: "lösung",
    5: "zauberrei",
    6: "viktor",
    7: "veritas"
}

# Funktion für den Start des Spiels und Begrüßung
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    game_active = get_player_data(chat_id, "game_active")
    
    if game_active:
        await update.message.reply_text("⚠️ Um das Spiel neu zu starten, gib bitte **/reset** ein.")
    else:
        await send_greeting(context, chat_id)

# Begrüßungsnachricht und Teamname-Eingabe anfordern
async def send_greeting(context: CallbackContext, chat_id: int) -> None:
    try:
        with open(TITLECARD_PATH, 'rb') as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)
        logger.info("Titelbild erfolgreich gesendet.")
    except FileNotFoundError:
        await context.bot.send_message(chat_id=chat_id, text="🔔 Die Einführung wird ohne Titelbild fortgesetzt.")
    
    logger.info("Sende Begrüßungstext.")
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "✨ <b>Willkommen im alle Rätsel </b>\n\n"
            "📜 <b>Wichtige Hinweise für eure Reise:</b>\n"
            "1. <b>Teamname festlegen</b>: Gebt <i>euren geheimen Teamnamen ohne das Wort Team</i> ein, um das Tor in die Welt zu öffnen.\n"
            "2. <b>Ruft nach Unterstützung</b>: Gebt <code>/help</code> ein, falls die Dunkelheit euch überwältigen sollte.\n"
            "3. <b>Zurücksetzen</b>: Gebt <code>/reset</code> ein, um das Abenteuer von Neuem zu beginnen, solltet ihr im Labyrinth der Geheimnisse verloren gehen.\n\n"
            "✨ <b>Möge das Schicksal euch wohlgesonnen sein</b> und euch durch die Nebel der Ungewissheit führen. <b>Viel Erfolg auf eurer Reise ins Unbekannte!</b> ✨"
        ),
        parse_mode="HTML"
    )
    logger.info("Begrüßungstext erfolgreich gesendet.")

# Hilfefunktion - nur verfügbar, wenn ein Teamname gesetzt ist
async def help_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    team_name = get_player_data(chat_id, "team_name")
    
    if not team_name:
        await update.message.reply_text("⚠️ Bitte setze zuerst deinen Teamnamen, um das Spiel zu starten.")
        return

    current_riddle = get_player_data(chat_id, "current_riddle")
    hint_text = get_hint_text(current_riddle)
    
    await update.message.reply_text(hint_text, parse_mode='HTML')

# Funktion zur Bereitstellung der Hinweise je nach aktuellem Rätsel
def get_hint_text(current_riddle):
    hints = {
        1: "🔍 <b>Hilfe für Rätsel 1</b>:  hinterlassen.",
        2: "🔍 <b>Hilfe für Rätsel 2</b>: bekannten Code entsprechen.",
        3: "🔍 <b>Hilfe für Rätsel 3</b>:  Zahl bilden.",
        4: "🔍 <b>Hilfe für Rätsel 4</b>:  ihre numerischen Werte.",
        5: "🔍 <b>Hilfe für Rätsel 5</b>: ein Passwort.",
        6: "🔍 <b>Hilfe für Rätsel 6</b>: wohin er dich führt.",
        7: "🔍 <b>Hilfe für Rätsel 7</b>: bilden sie zusammen?"
    }
    return hints.get(current_riddle, "Kein Hinweis verfügbar.")

# Hinweis-Funktion, die nach einer Verzögerung über JobQueue aufgerufen wird
async def schedule_hint_job(context: CallbackContext) -> None:
    chat_id = context.job.data['chat_id']
    logger.info(f"Geplanter Hinweis für Chat-ID {chat_id} wird jetzt gesendet.")
    try:
        await schedule_hint(chat_id, context)
    except Exception as e:
        logger.error(f"Fehler beim Senden des Hinweises an Chat-ID {chat_id}: {e}")
        retry_delay = 60  # Wiederholen nach 60 Sekunden bei Fehler
        logger.info(f"Einreihen eines erneuten Hinweises für Chat-ID {chat_id} in {retry_delay} Sekunden.")
        context.job_queue.run_once(schedule_hint_job, retry_delay, data={'chat_id': chat_id}, name=f"hint_{chat_id}_retry")

# Asynchrone Funktion, die den Hinweis sendet
async def schedule_hint(chat_id: int, context: CallbackContext) -> None:
    logger.info(f"Sende Hinweis für Chat-ID {chat_id}.")
    if get_player_data(chat_id, "game_active"):
        current_riddle = get_player_data(chat_id, "current_riddle")
        hint_text = get_hint_text(current_riddle)
        await context.bot.send_message(chat_id=chat_id, text=f"🕒 Hinweis: {hint_text}", parse_mode='HTML')

# Überprüfung der Rätsellösung und Fortschritt
async def check_solution(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    awaiting_team_name = not get_player_data(chat_id, "team_name")

    if awaiting_team_name:
        new_team_name = update.message.text.strip()
        save_player_data(chat_id, team_name=new_team_name, current_riddle=1, game_active=True, start_time=str(datetime.now()))
        await update.message.reply_text(f"Teamname '{new_team_name}' wurde erfolgreich festgelegt! Beginne das erste Rätsel.")
        await escape_riddle(update, context, 1)
        return

    current_riddle = get_player_data(chat_id, "current_riddle")
    user_solution = update.message.text.strip().lower()
    
    if user_solution == solutions.get(current_riddle):
        logger.info(f"Richtige Lösung für Rätsel {current_riddle} von Chat-ID {chat_id}")
        await update.message.reply_text(f"✅ Richtig! Du hast das Rätsel {current_riddle} gelöst!")
        if current_riddle + 1 in solutions:
            await escape_riddle(update, context, current_riddle + 1)
        elif current_riddle == 7 and user_solution == "veritas":
            await handle_codeword_veritas(update, context)
        else:
            await update.message.reply_text("✨ Herzlichen Glückwunsch, du hast alle Rätsel gelöst! Das Spiel ist beendet.")
            save_player_data(chat_id, game_active=False)  # Spiel als beendet markieren
    else:
        logger.info(f"Falsche Lösung für Rätsel {current_riddle} von Chat-ID {chat_id}")
        await update.message.reply_text(f"❌ Falsch! Versuche das Rätsel {current_riddle} erneut.")

# Funktion zur Verarbeitung des Codeworts "veritas"
async def handle_codeword_veritas(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    start_time = get_player_data(chat_id, "start_time")
    
    # Berechnung der Gesamtspielzeit
    if start_time:
        end_time = datetime.now()
        total_time = end_time - datetime.fromisoformat(start_time)
        total_time_formatted = str(timedelta(seconds=total_time.total_seconds())).split(".")[0]
        time_message = f"Gesamtspielzeit: {total_time_formatted}."
    else:
        time_message = "Die Zeitmessung konnte nicht ermittelt werden."

    team_name = get_player_data(chat_id, "team_name")
    current_riddle = get_player_data(chat_id, "current_riddle")
    
    # Sende Abschlussnachricht an den Spieler
    await update.message.reply_text(
        "🔑 <b>Ihr habt das Codewort 'Veritas' korrekt eingegeben!</b> 🔑\n\n"
      oder soll es für immer ruhen?\n\n"
        f"{time_message}\n\n"
        "Vielen Dank für das Spielen! Möchtet ihr eine Bewertung abgeben? Gebt <b>/bewertung</b> ein.",
        parse_mode='HTML'
    )

    # Beende alle geplanten Hinweise für den Chat
    current_jobs = context.job_queue.get_jobs_by_name(f"hint_{chat_id}")
    for job in current_jobs:
        job.schedule_removal()
        logger.info(f"Geplanter Hinweis für Chat-ID {chat_id} wurde entfernt.")

    # E-Mail und Zertifikat senden
    await asyncio.to_thread(send_end_game_email, team_name, chat_id, total_time.total_seconds(), current_riddle)
    certificate_path = generate_certificate(team_name, total_time_formatted)
    try:
        await context.bot.send_document(chat_id, document=open(certificate_path, "rb"))
    finally:
        os.remove(certificate_path)

    # Spiel als abgeschlossen speichern
    save_player_data(chat_id, game_active=False)

# Dictionary für die Zeitverzögerungen für jedes Rätsel in Sekunden
riddle_delays = {
    1: 300,   # 5 Minuten für Rätsel 1
    2: 300,   # 5 Minuten für Rätsel 2
    3: 300,   # 5 Minuten für Rätsel 3
    4: 300,   # 5 Minuten für Rätsel 4
    5: 420,   # 7 Minuten für Rätsel 5
    6: 420,   # 7 Minuten für Rätsel 6
    7: 300    # 5 Minuten für Rätsel 7
}

# Texte für jedes Rätsel anzeigen und zum nächsten überleiten
async def escape_riddle(update: Update, context: CallbackContext, riddle_number) -> None:
    # Entfernt bestehende Jobs, um Dopplungen zu vermeiden
    current_jobs = context.job_queue.get_jobs_by_name(f"hint_{update.message.chat.id}")
    for job in current_jobs:
        job.schedule_removal()
    
    riddle_texts = {
    1: (
        "<b>✨ Kapitel 1: \n\n"
        "🔮 <b>Rätsel 1: </b>\n"
        "<b>Öffnet den ersten Umschlag.</b> Darin erwartet euch eine Überraschung. "
    ),
    2: (
        "<b>🚨 Kapitel 2:  🚨</b>\n\n"
        "Nachdem sich der Tumult \n\n"
        "🔮 <b>Rätsel 2: t</b>\n"
        "<b>Öffnet den zweiten Umschlag.</b> Darin findet ihr ."
    ),
    3: (
        "<b>📜 Kapitel 3:  📜</b>\n\n"
        "
        "🔮 <b>Rätsel 3: </b>\n"
        "<b>Öffnet den dritten Umschlag.</b> "
    ),
    4: (
        "<b>🕯️ Kapitel 4:  🕯️</b>\n\n"
        
        "🔮 <b>Rätsel 4: </b>\n"
        "<b>Öffnet den vierten Umschlag.</b> ."
    ),
    5: (
        "<b>📮 Kapitel 5: 📮</b>\n\n"
        "
        "🔮 <b>Rätsel 5: </b>\n"
        "<b>Öffnet den fünften Umschlag.</b> ."
    ),
    6: (
        "<b>🗺️ Kapitel 6:  🗺️</b>\n\n"
        " "
        "er, die Puzzleteile zusammenzusetzen.\n\n"
        "🔮 <b>Rätsel 6: </b>\n"
        "<b>Öffnet den sechsten Umschlag.</b> ?"
    ),
    7: (
        "<b>🔑 Kapitel 7:  🔑</b>\n\n"
        ""
        "🔮 <b>Rätsel 7: Das endgültige Codewort</b>\n"
        "."
    )
}

    
    await update.message.reply_text(riddle_texts.get(riddle_number, "Ende des Spiels"), parse_mode='HTML')

    # Speichert das aktuelle Rätsel und setzt game_active auf True
    save_player_data(update.message.chat.id, current_riddle=riddle_number, game_active=True)
    logger.info(f"Spielstatus für Chat-ID {update.message.chat.id}: aktuelles Rätsel ist {riddle_number}")

    # Starte schedule_hint über JobQueue mit einer spezifischen Verzögerung für das aktuelle Rätsel
    delay_seconds = riddle_delays.get(riddle_number, 300)  # Standardverzögerung: 300 Sekunden
    if get_player_data(update.message.chat.id, "game_active"):
        logger.info(f"Verzögerter Hinweis für Chat-ID {update.message.chat.id} wird in die JobQueue eingereiht mit {delay_seconds} Sekunden Verzögerung.")
        context.job_queue.run_once(schedule_hint_job, delay_seconds, data={'chat_id': update.message.chat.id}, name=f"hint_{update.message.chat.id}")
