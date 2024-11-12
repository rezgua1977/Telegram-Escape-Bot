#email_handler.py
import os
import smtplib
import sqlite3
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from logger_config import logger  # Importiert den zentralen Logger aus logger_config.py

# Lade Umgebungsvariablen
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
DB_PATH = 'game_data.db'  # Pfad zur SQLite-Datenbank

def check_env_variables():
    """Überprüft, ob alle notwendigen Umgebungsvariablen geladen wurden."""
    missing_vars = [var for var in ["EMAIL_USER", "EMAIL_PASS", "RECIPIENT_EMAIL"] if not globals()[var]]
    if missing_vars:
        logger.error(f"Fehlende Umgebungsvariablen: {', '.join(missing_vars)}. Bitte überprüfen Sie die .env-Datei.")
        return False
    return True

def create_email(subject, body, is_html=False):
    """Erstellt eine E-Mail-Nachricht."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
    return msg

def send_email(subject, body, is_html=False):
    """Sendet eine E-Mail mit dem gegebenen Betreff und Inhalt."""
    if not check_env_variables():
        logger.error("E-Mail-Versand abgebrochen, da erforderliche Umgebungsvariablen fehlen.")
        return

    if not subject or not body:
        logger.error("E-Mail-Betreff oder -Inhalt darf nicht leer sein.")
        return

    msg = create_email(subject, body, is_html)

    try:
        with smtplib.SMTP('mail.gmx.net', 587, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
            logger.info(f"E-Mail erfolgreich gesendet: Betreff = {subject}")
    except smtplib.SMTPAuthenticationError:
        logger.error("Authentifizierungsfehler: Überprüfen Sie die Anmeldeinformationen für den E-Mail-Server.")
    except smtplib.SMTPConnectError:
        logger.error("Verbindungsfehler: Verbindung zum SMTP-Server konnte nicht hergestellt werden.")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP-Fehler: {e}")
    except Exception as e:
        logger.error(f"Unbekannter Fehler beim Senden der E-Mail: {e}")

def fetch_game_data(team_name):
    """Holt Spieldaten für das gegebene Team aus der Datenbank."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT team_name, current_riddle, start_time, game_active FROM players WHERE team_name = ?",
                (team_name,)
            )
            data = cursor.fetchone()
            if data:
                logger.info(f"Spieldaten für Team '{team_name}' erfolgreich abgerufen.")
            else:
                logger.warning(f"Keine Spieldaten für Team '{team_name}' gefunden.")
            return data
    except sqlite3.Error as e:
        logger.error(f"Datenbankfehler beim Abrufen der Spieldaten für Team '{team_name}': {e}")
        return None

def format_email_body(team_name, start_time, game_duration, total_riddles, current_riddle, game_active):
    """Erstellt den HTML-Inhalt für die E-Mail."""
    start_time_formatted = datetime.fromisoformat(start_time).strftime('%d.%m.%Y %H:%M:%S')
    formatted_duration = str(timedelta(seconds=game_duration)).split(".")[0]

    return f"""
    <html>
    <body>
        <h2>🎉 Spielende für Team {team_name} 🎉</h2>
        <p><strong>📅 Startzeit:</strong> {start_time_formatted}</p>
        <p><strong>🕒 Gesamtdauer:</strong> {formatted_duration} (HH:MM:SS)</p>
        <p><strong>🔍 Gelöste Rätsel:</strong> {total_riddles} von {current_riddle}</p>
        <p><strong>🏁 Spielstatus:</strong> {'Beendet' if not game_active else 'Aktiv'}</p>
    </body>
    </html>
    """

def send_end_game_email(team_name, chat_id, game_duration, total_riddles):
    """Sendet eine detaillierte Abschluss-E-Mail nach Spielende."""
    logger.info(f"Beginne das Senden der Abschluss-E-Mail für Team '{team_name}'.")
    game = fetch_game_data(team_name)
    if not game:
        logger.error(f"Keine Spieldaten für Team '{team_name}' gefunden.")
        return

    # Extrahiere Datenbankwerte
    _, current_riddle, start_time, game_active = game

    # Erstelle und sende die E-Mail
    email_body = format_email_body(
        team_name, start_time, game_duration, total_riddles, current_riddle, game_active
    )
    logger.info(f"Sende Abschluss-E-Mail an Team '{team_name}'.")
    send_email(f"Spielende: Team {team_name}", email_body, is_html=True)
