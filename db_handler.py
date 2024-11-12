#db_handler.py
import sqlite3
from logger_config import logger  # Importiere den zentralen Logger

# Pfad zur SQLite-Datenbankdatei
DB_PATH = 'game_data.db'

def init_db():
    """Initialisiert die Datenbank und erstellt die Tabelle 'players', falls sie noch nicht existiert."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Tabelle 'players' erstellen, falls sie noch nicht existiert
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    team_name TEXT,
                    current_riddle INTEGER,
                    start_time TEXT,
                    email_sent INTEGER DEFAULT 0,
                    game_active INTEGER DEFAULT 0,
                    rated INTEGER DEFAULT 0,
                    rating INTEGER
                )
            ''')
            conn.commit()
            logger.info("Datenbank und Tabelle 'players' erfolgreich initialisiert.")
    except sqlite3.Error as e:
        logger.error(f"Fehler bei der Initialisierung der Datenbank: {e}")

def save_player_data(player_id, team_name=None, current_riddle=None, start_time=None, email_sent=0, game_active=False, rated=0, rating=None):
    """
    Speichert oder aktualisiert die Daten eines Spielers in der Datenbank.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            query = '''
                INSERT INTO players (player_id, team_name, current_riddle, start_time, email_sent, game_active, rated, rating)
                VALUES (:player_id, :team_name, :current_riddle, :start_time, :email_sent, :game_active, :rated, :rating)
                ON CONFLICT(player_id) DO UPDATE SET
                    team_name = COALESCE(:team_name, team_name),
                    current_riddle = COALESCE(:current_riddle, current_riddle),
                    start_time = COALESCE(:start_time, start_time),
                    email_sent = COALESCE(:email_sent, email_sent),
                    game_active = COALESCE(:game_active, game_active),
                    rated = COALESCE(:rated, rated),
                    rating = COALESCE(:rating, rating)
            '''
            params = {
                "player_id": player_id,
                "team_name": team_name,
                "current_riddle": current_riddle,
                "start_time": start_time,
                "email_sent": email_sent,
                "game_active": game_active,
                "rated": rated,
                "rating": rating
            }

            cursor.execute(query, params)
            conn.commit()
            logger.info(f"Spielerdaten für player_id={player_id} erfolgreich gespeichert/aktualisiert.")
    
    except sqlite3.Error as e:
        logger.error(f"Fehler beim Speichern der Spielerdaten für player_id={player_id}: {e}")

def get_player_data(player_id, field):
    """
    Ruft ein spezifisches Feld für einen Spieler basierend auf der player_id ab.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {field} FROM players WHERE player_id = ?", (player_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                logger.warning(f"Keine Daten für player_id={player_id} und Feld '{field}' gefunden.")
                return None
    except sqlite3.Error as e:
        logger.error(f"Fehler beim Abrufen des Feldes '{field}' für player_id={player_id}: {e}")
        return None

def delete_player_data(player_id):
    """
    Löscht alle Daten eines Spielers basierend auf der player_id.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM players WHERE player_id = ?", (player_id,))
            conn.commit()
            logger.info(f"Spielerdaten für player_id={player_id} erfolgreich gelöscht.")
    except sqlite3.Error as e:
        logger.error(f"Fehler beim Löschen der Spielerdaten für player_id={player_id}: {e}")
