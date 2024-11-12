import os
from dotenv import load_dotenv

# Definiere den Pfad zur .env-Datei und lade die Umgebungsvariablen
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# Prüfe, ob die .env-Datei vorhanden ist und lade sie
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print("Umgebungsvariablen wurden erfolgreich geladen.")
else:
    print("Warnung: Die .env-Datei wurde nicht gefunden. Bitte sicherstellen, dass sie im Verzeichnis vorhanden ist.")
