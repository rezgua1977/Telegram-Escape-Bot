#main_bot.py
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from db_handler import init_db
from riddle_handler import start, help_command, check_solution, escape_riddle
from reset_handler import reset, confirm_reset, cancel_reset
from rating_handler import send_survey, rating_callback
from logger_config import logger  # Importiere den zentralen Logger

# Konfiguration der Umgebungsvariablen
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Überprüfung des Tokens
if not TOKEN:
    logger.error("Bot-Token fehlt. Überprüfe die .env-Datei auf einen gültigen Token-Eintrag.")
    raise ValueError("Bot-Token fehlt. Überprüfe die .env-Datei auf einen gültigen Token-Eintrag.")

# Hauptfunktion zur Initialisierung und Start des Bots
def main():
    try:
        init_db()
        logger.info("Datenbank erfolgreich initialisiert.")
    except Exception as e:
        logger.error("Fehler bei der Initialisierung der Datenbank", exc_info=True)
        return

    # Bot-Application erstellen
    try:
        application = Application.builder().token(TOKEN).build()
        logger.info("Bot-Application erfolgreich erstellt.")
    except Exception as e:
        logger.error("Fehler beim Erstellen der Bot-Application", exc_info=True)
        return

    # `JobQueue` wird automatisch durch die `Application`-Instanz bereitgestellt
    job_queue = application.job_queue

    # Handler hinzufügen
    application.add_handler(CommandHandler("start", start))               # Start-Befehl
    application.add_handler(CommandHandler("help", help_command))         # Hilfe-Befehl
    application.add_handler(CommandHandler("reset", reset))               # Reset-Befehl
    application.add_handler(CommandHandler("bewertung", send_survey))     # Bewertung-Befehl

    # CallbackHandler für Bestätigungen und Bewertungen
    application.add_handler(CallbackQueryHandler(confirm_reset, pattern='^confirm_reset$'))
    application.add_handler(CallbackQueryHandler(cancel_reset, pattern='^cancel_reset$'))
    application.add_handler(CallbackQueryHandler(rating_callback, pattern='^rating_'))

    # Nachrichten-Handler für Rätsel-Lösungen, ignoriert andere Befehle
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_solution))

    # Bot starten und nach Eingaben von Nutzern suchen
    logger.info("Bot gestartet und wartet auf Eingaben.")
    application.run_polling()  # Starte das Polling synchron

if __name__ == "__main__":
    main()
