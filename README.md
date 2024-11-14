
# Telegram Escape Bot

Ein flexibler und anpassbarer Telegram-Bot für Escape-Spiele, der als Systemdienst eingerichtet werden kann. Der Bot läuft automatisch auf einem Server oder Raspberry Pi und lässt sich bequem über `systemctl` starten, stoppen und neustarten.

## Funktionen

- **Systemdienst-Steuerung**: Einfache Steuerung über `systemctl` für automatischen Start, Stop und Neustart des Bots.
- **Rätselverwaltung**: Unterstützt die Erstellung und Verwaltung eigener Rätsel.
- **Teamnamen-Funktion**: Die Spieler können vor Spielbeginn einen Teamnamen festlegen.
- **Hinweis- und Hilfefunktion**: Der Bot kann automatische Hinweise nach einer festgelegten Zeitspanne senden oder den Spielern auf Anfrage über den `/help`-Befehl helfen.
- **Zeitmessung und Abschlussevaluation**: Misst die Spieldauer und zeigt sie in einer abschließenden Zusammenfassung an.

## Voraussetzungen

- **Python 3.x**: Stelle sicher, dass Python 3.x auf deinem System installiert ist.
- **Telegram-Bot API-Token**: Du benötigst einen Bot-Token, den du über [BotFather](https://t.me/botfather) auf Telegram erstellen kannst.

## Installation

### Schritt 1: Repository klonen und virtuelle Umgebung einrichten

1. **Repository klonen**:
   ```bash
   git clone https://github.com/rezgua1977/Telegram-Escape-Bot.git
   cd Telegram-Escape-Bot
   ```

2. **Virtuelle Umgebung einrichten und aktivieren**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Für Linux/macOS
   venv\Scripts\activate      # Für Windows
   ```

3. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

### Schritt 2: Umgebungsvariablen konfigurieren

Erstelle eine `.env`-Datei im Projektordner und füge deinen Bot-Token hinzu:

```plaintext
BOT_TOKEN=DeinBotTokenHier
```

Ersetze `DeinBotTokenHier` durch den tatsächlichen Token, den du von BotFather erhalten hast.

### Schritt 3: Konfigurationsdatei `config.py` erstellen

Erstelle die Datei `config.py` im Hauptverzeichnis des Projekts mit folgendem Inhalt:

```python
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
```

Diese Datei sorgt dafür, dass die Umgebungsvariablen aus der `.env`-Datei geladen werden.

### Schritt 4: Einrichten als Systemdienst

Um den Bot als Systemdienst zu konfigurieren, erstelle eine Systemdienst-Datei.

1. **Systemdienst-Datei erstellen**:

   ```bash
   sudo nano /etc/systemd/system/telegram-escape-bot.service
   ```

2. **Inhalt der Dienstdatei**:

```plaintext
[Unit]
Description=Telegram Escape Bot
After=network.target

[Service]
User=root
WorkingDirectory=/root/telegram-escape-bot
# Stellt die Zeitzone Europe/Berlin sicher
Environment="TZ=Europe/Berlin"
ExecStartPre=/bin/bash -c 'timedatectl set-timezone Europe/Berlin'
ExecStart=/root/telegram-escape-bot/venv/bin/python /root/telegram-escape-bot/main_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

   - **WorkingDirectory**: Ersetze `/pfad/zu/Telegram-Escape-Bot` mit dem tatsächlichen Pfad zu deinem Projektordner.
   - **ExecStart**: Achte darauf, dass der Pfad zur Python-Umgebung und zur `main_bot.py` korrekt ist.
   - **User**: Gib deinen Benutzernamen auf dem Server oder Raspberry Pi an.
   - **EnvironmentFile**: Pfad zur `.env`-Datei.

3. **Systemdienst laden und aktivieren**:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable telegram-escape-bot
   ```

4. **Bot-Dienst starten**:

   ```bash
   sudo systemctl start telegram-escape-bot
   ```

### Schritt 5: Bot-Steuerung über `systemctl`

- **Starten**: `sudo systemctl start telegram-escape-bot`
- **Stoppen**: `sudo systemctl stop telegram-escape-bot`
- **Neustarten**: `sudo systemctl restart telegram-escape-bot`
- **Status prüfen**: `sudo systemctl status telegram-escape-bot`

## Anpassung und Nutzung

- **Eigene Rätsel hinzufügen**: Bearbeite die Datei `riddle_handler.py`, um eigene Rätsel hinzuzufügen.
- **Abschlussbewertung anpassen**: Passe die Schlussnachricht in `rating_handler.py` an.

## Hinweise

- **Sicherer Umgang mit dem Bot-Token**: Stelle sicher, dass die `.env`-Datei nicht ins Repository hochgeladen wird. Füge sie zur `.gitignore` hinzu.
- **Modularer Aufbau**: Der Bot ist modular aufgebaut, was die Anpassung erleichtert.

## Beispiel für `.gitignore`

Erstelle eine `.gitignore`-Datei im Hauptverzeichnis mit folgendem Inhalt:

```plaintext
.env
config.py
__pycache__/
*.pyc
venv/
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der Datei `LICENSE`.

---

Mit dieser Anleitung läuft dein Bot als Systemdienst und lädt die Umgebungsvariablen über die `config.py`. Wenn du weitere Hilfe benötigst, stehe ich dir gerne zur Verfügung.
