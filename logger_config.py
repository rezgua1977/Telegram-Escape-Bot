import logging
from logging.handlers import RotatingFileHandler

# Haupt-Logger-Konfiguration
logger = logging.getLogger("TelegramEscapeBot")
logger.setLevel(logging.DEBUG)  # Ermöglicht auch das Debugging

# Formatter für eine klare Log-Ausgabe
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File-Handler für allgemeine Log-Datei (bot_log.log), mit Rotation
file_handler = RotatingFileHandler(
    "bot_log.log", maxBytes=5*1024*1024, backupCount=3  # 5 MB pro Datei, 3 Backups behalten
)
file_handler.setLevel(logging.INFO)  # Protokolliert allgemeine Informationen und höher
file_handler.setFormatter(formatter)

# Separater File-Handler nur für Fehler (bot_errors.log)
error_handler = logging.FileHandler("bot_errors.log")
error_handler.setLevel(logging.ERROR)  # Nur ERROR und schwerwiegendere Meldungen
error_handler.setFormatter(formatter)

# Hinzufügen der Handler zum Logger
logger.addHandler(file_handler)
logger.addHandler(error_handler)

# Optional: Konsolenausgabe für Entwickler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Ausgabe aller Meldungen in der Konsole
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

