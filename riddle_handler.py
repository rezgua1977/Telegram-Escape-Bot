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

# Lösungen für die einzelnen Rätsel (alle standardisiert in Kleinbuchstaben)
solutions = {
    1: ["lösung1"],
    2: ["lösung2"],
    3: ["lösung3"],
    4: ["lösung4"],
    5: ["lösung5"],
    6: ["lösung6"],
    7: ["lösung7"],
    8: ["lösung8"]
}

# Dictionary für die Zeitverzögerungen für jedes Rätsel in Sekunden
riddle_delays = {
    1: 420,   # 7 Minuten für Rätsel 1
    2: 360,   # 6 Minuten für Rätsel 2
    3: 360,   # 6 Minuten für Rätsel 3
    4: 360,   # 6 Minuten für Rätsel 4
    5: 420,   # 7 Minuten für Rätsel 5
    6: 420,   # 7 Minuten für Rätsel 6
    7: 360,   # 6 Minuten für Rätsel 7
    8: 480    # 8 Minuten für Rätsel 8
}

# Funktion für den Start des Spiels und Begrüßung
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    game_active = await get_player_data_async(chat_id, "game_active")

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
            "Willkommen zum Spiel!\n\n"
            "Hier sind einige wichtige Hinweise für deine Reise:\n"
            "1️⃣ <b>Teamname festlegen</b>: Gib deinen Teamnamen ein, um das Abenteuer zu beginnen.\n"
            "2️⃣ <b>Hilfe rufen</b>: Gib <b>/help</b> ein, falls du auf deiner Reise Unterstützung benötigst.\n"
            "3️⃣ <b>Zurücksetzen</b>: Gib <b>/reset</b> ein, um das Abenteuer von Neuem zu starten, sollte dir der Weg verloren gehen.\n\n"
            "Viel Erfolg auf deiner Reise!"
        ),
        parse_mode='HTML'
    )
    logger.info("Begrüßungstext erfolgreich gesendet.")

# Hilfefunktion - nur verfügbar, wenn ein Teamname gesetzt ist
async def help_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    team_name = await get_player_data_async(chat_id, "team_name")

    if not team_name:
        await update.message.reply_text("⚠️ Bitte setze zuerst deinen Teamnamen, um das Spiel zu starten.")
        return

    current_riddle = await get_player_data_async(chat_id, "current_riddle")
    hint_text = get_hint_text(current_riddle)

    await update.message.reply_text(hint_text, parse_mode='HTML')

# Funktion zur Bereitstellung der Hinweise je nach aktuellem Rätsel
def get_hint_text(current_riddle: int) -> str:
    hints = {
        1: "🔍 <b>Hilfe für Rätsel 1</b>: Hier kommt der Hinweis für Rätsel 1.",
        2: "🔍 <b>Hilfe für Rätsel 2</b>: Hier kommt der Hinweis für Rätsel 2.",
        3: "🔍 <b>Hilfe für Rätsel 3</b>: Hier kommt der Hinweis für Rätsel 3.",
        4: "🔍 <b>Hilfe für Rätsel 4</b>: Hier kommt der Hinweis für Rätsel 4.",
        5: "🔍 <b>Hilfe für Rätsel 5</b>: Hier kommt der Hinweis für Rätsel 5.",
        6: "🔍 <b>Hilfe für Rätsel 6</b>: Hier kommt der Hinweis für Rätsel 6.",
        7: "🔍 <b>Hilfe für Rätsel 7</b>: Hier kommt der Hinweis für Rätsel 7.",
        8: "🔍 <b>Hilfe für Rätsel 8</b>: Hier kommt der Hinweis für Rätsel 8."
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
    if await get_player_data_async(chat_id, "game_active"):
        current_riddle = await get_player_data_async(chat_id, "current_riddle")
        hint_text = get_hint_text(current_riddle)
        await context.bot.send_message(chat_id=chat_id, text=f"🕒 Hinweis: {hint_text}", parse_mode='HTML')

# Überprüfung der Rätsellösung und Fortschritt
async def check_solution(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    awaiting_team_name = not await get_player_data_async(chat_id, "team_name")

    if awaiting_team_name:
        new_team_name = update.message.text.strip()
        if not new_team_name:
            await update.message.reply_text("Bitte geben Sie einen gültigen Teamnamen ein.")
            return
        await save_player_data_async(chat_id, team_name=new_team_name, current_riddle=1, game_active=True, start_time=str(datetime.now()))
        await update.message.reply_text(f"Teamname '{new_team_name}' wurde erfolgreich festgelegt! Beginne das erste Rätsel.")
        await escape_riddle(update, context, 1)
        return

    try:
        current_riddle = await get_player_data_async(chat_id, "current_riddle")
        user_solution = update.message.text.strip().lower()
        valid_solutions = [solution.lower() for solution in solutions.get(current_riddle, [])]
        if user_solution in valid_solutions:
            logger.info(f"Richtige Lösung für Rätsel {current_riddle} von Chat-ID {chat_id}")
            await update.message.reply_text(f"✅ Richtig! Du hast das Rätsel {current_riddle} gelöst!")
            if current_riddle + 1 in solutions:
                await escape_riddle(update, context, current_riddle + 1)
            elif current_riddle == 8 and user_solution == "lösung8":
                await handle_final_riddle_solution(update, context)
            else:
                await update.message.reply_text("✨ Herzlichen Glückwunsch, du hast alle Rätsel gelöst! Das Spiel ist beendet.")
                await save_player_data_async(chat_id, game_active=False)
        else:
            logger.info(f"Falsche Lösung für Rätsel {current_riddle} von Chat-ID {chat_id}")
            await update.message.reply_text(f"❌ Falsch! Versuche das Rätsel {current_riddle} erneut.")
    except Exception as e:
        logger.error(f"Fehler beim Überprüfen der Lösung für Chat-ID {chat_id}: {e}")
        await update.message.reply_text("Es ist ein Fehler aufgetreten. Bitte versuche es erneut.")

# Logik zum Behandeln der endgültigen Lösung
async def handle_final_riddle_solution(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    team_name = await get_player_data_async(chat_id, "team_name")
    start_time = await get_player_data_async(chat_id, "start_time")
    current_riddle = await get_player_data_async(chat_id, "current_riddle")  # Fetch the current riddle value

    # Berechnung der Gesamtspielzeit
    if start_time:
        end_time = datetime.now()
        total_time = end_time - datetime.fromisoformat(start_time)
        total_time_formatted = str(timedelta(seconds=total_time.total_seconds())).split(".")[0]
        time_message = f"Gesamtspielzeit: {total_time_formatted}."
    else:
        total_time = None
        total_time_formatted = "Unbekannt"
        time_message = "Die Zeitmessung konnte nicht ermittelt werden."

    # Sende Abschlussnachricht an den Spieler
    await update.message.reply_text(
        "✨ <b>Herzlichen Glückwunsch! Du hast das Spiel erfolgreich abgeschlossen!</b> ✨\n\n"
        f"{time_message}\n\n"
        "Vielen Dank, dass du Teil dieser Reise warst. Wenn dir das Spiel gefallen hat, "
        "würde sich der Autor über eine kurze Rückmeldung freuen. Gib <b>/bewertung</b> ein, "
        "um deine Erfahrung zu teilen und andere an diesem Abenteuer teilhaben zu lassen.",
        parse_mode='HTML'
    )

    # Beende alle geplanten Hinweise für den Chat
    current_jobs = context.job_queue.get_jobs_by_name(f"hint_{chat_id}")
    for job in current_jobs:
        job.schedule_removal()
        logger.info(f"Geplanter Hinweis für Chat-ID {chat_id} wurde entfernt.")

    # E-Mail und Zertifikat senden
    if total_time:
        await asyncio.to_thread(send_end_game_email, team_name, chat_id, total_time.total_seconds(), current_riddle)
    else:
        await asyncio.to_thread(send_end_game_email, team_name, chat_id, None, current_riddle)

    certificate_path = generate_certificate(team_name, total_time_formatted)
    try:
        await context.bot.send_document(chat_id, document=open(certificate_path, "rb"))
    finally:
        os.remove(certificate_path)

    # Spiel als abgeschlossen speichern
    await save_player_data_async(chat_id, game_active=False)
    logger.info(f"Spiel beendet für Chat-ID {chat_id}.")

# Texte für jedes Rätsel anzeigen und zum nächsten überleiten
async def escape_riddle(update: Update, context: CallbackContext, riddle_number: int) -> None:
    chat_id = update.message.chat.id
    riddle_text = get_riddle_text(riddle_number)

    if riddle_number == 8:
        await send_riddle_8_content(update, context, chat_id, riddle_text)
    else:
        await update.message.reply_text(riddle_text, parse_mode='HTML')

    await save_player_data_async(chat_id, current_riddle=riddle_number, game_active=True)
    logger.info(f"Spielstatus für Chat-ID {chat_id}: aktuelles Rätsel ist {riddle_number}")

    delay_seconds = riddle_delays.get(riddle_number, 300)
    context.job_queue.run_once(schedule_hint_job, delay_seconds, data={'chat_id': chat_id}, name=f"hint_{chat_id}")
    logger.info(f"Geplanter Hinweis in {delay_seconds} Sekunden für Chat-ID {chat_id}")

def get_riddle_text(riddle_number: int) -> str:
    riddle_texts = {
        1: "<b>Rätsel 1</b>\n\nHier kommt der Text für Rätsel 1.",
        2: "<b>Rätsel 2</b>\n\nHier kommt der Text für Rätsel 2.",
        3: "<b>Rätsel 3</b>\n\nHier kommt der Text für Rätsel 3.",
        4: "<b>Rätsel 4</b>\n\nHier kommt der Text für Rätsel 4.",
        5: "<b>Rätsel 5</b>\n\nHier kommt der Text für Rätsel 5.",
        6: "<b>Rätsel 6</b>\n\nHier kommt der Text für Rätsel 6.",
        7: "<b>Rätsel 7</b>\n\nHier kommt der Text für Rätsel 7.",
        8: "<b>Rätsel 8</b>\n\nHier kommt der Text für Rätsel 8."
    }
    return riddle_texts.get(riddle_number, "Ende des Spiels")

async def send_riddle_8_content(update: Update, context: CallbackContext, chat_id: int, riddle_text: str) -> None:
    await update.message.reply_text(riddle_text, parse_mode='HTML')
    video_path = "/root/telegram-escape-bot/Videos/riddle8.mp4"
    try:
        if os.path.exists(video_path):
            with open(video_path, 'rb') as video:
                await context.bot.send_video(chat_id=chat_id, video=video)
                logger.info(f"Video für Rätsel 8 an Chat-ID {chat_id} gesendet.")
        else:
            await update.message.reply_text("⚠️ Das Video für Rätsel 8 konnte nicht gefunden werden.")
    except Exception as e:
        logger.error(f"Fehler beim Senden des Videos für Rätsel 8: {e}")
        await update.message.reply_text("⚠️ Fehler beim Abspielen des Videos.")

    await update.message.reply_text(
        "🎥 <b>Aufgabe:</b> Achtet genau auf die Symbole, Wörter oder Botschaften im Film. "
        "Sie könnten das letzte Geheimnis enthüllen. Was zeigt euch der Film?",
        parse_mode='HTML'
    )

# Asynchrone Datenbankoperationen
async def save_player_data_async(chat_id: int, **kwargs) -> None:
    await asyncio.to_thread(save_player_data, chat_id, **kwargs)

async def get_player_data_async(chat_id: int, key: str) -> Any:
    return await asyncio.to_thread(get_player_data, chat_id, key)
