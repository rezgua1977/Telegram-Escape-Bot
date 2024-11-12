
# Telegram Escape Bot

Ein flexibler und anpassbarer Telegram-Bot für Escape-Spiele, der Entwicklern die Möglichkeit gibt, ihre eigenen Rätsel und Inhalte hinzuzufügen. Dieser Bot stellt die Grundstruktur bereit, um Teilnehmer durch ein spannendes, interaktives Abenteuer zu führen.

## Funktionen

- **Rätselverwaltung**: Eine einfache Struktur, um eigene Rätsel zu erstellen und zu integrieren.
- **Teamnamen-Funktion**: Spieler können sich vor Spielbeginn einen Teamnamen geben.
- **Hinweis- und Hilfefunktion**: Der Bot kann den Spielern entweder automatisch nach einer festgelegten Zeitspanne Hinweise geben oder den Spielern auf Anfrage über den `/help`-Befehl helfen.
- **Zeitmessung**: Misst die benötigte Zeit, um das Spiel abzuschließen, und zeigt die Gesamtdauer am Ende an.
- **Abschlussevaluation**: Zeigt eine Zusammenfassung des Spiels mit Teamname, Spieldauer und anderen Details.

## Voraussetzungen

- **Python 3.x**: Stelle sicher, dass Python 3.x auf deinem System installiert ist.
- **Telegram-Bot API-Token**: Du benötigst einen Bot-Token, den du über [BotFather](https://t.me/botfather) auf Telegram erstellen kannst.

## Installation

1. **Repository klonen**:
   Klone das Repository in das gewünschte Verzeichnis auf deinem Computer:
   ```bash
   git clone https://github.com/rezgua1977/Telegram-Escape-Bot.git
   cd Telegram-Escape-Bot
   ```

2. **Virtuelle Umgebung einrichten und aktivieren**:
   Erstelle eine virtuelle Umgebung und aktiviere sie:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Für Linux/macOS
   venv\Scripts\activate      # Für Windows
   ```

3. **Abhängigkeiten installieren**:
   Installiere die erforderlichen Python-Pakete:
   ```bash
   pip install -r requirements.txt
   ```

4. **Umgebungsvariablen konfigurieren**:
   Erstelle eine `.env`-Datei im Projektordner und füge deinen Bot-Token hinzu:
   ```plaintext
   BOT_TOKEN=DeinBotTokenHier
   ```
   Ersetze `DeinBotTokenHier` durch den tatsächlichen Bot-Token, den du von BotFather erhalten hast.

## Nutzung

1. **Bot starten**:
   Starte den Bot, indem du den folgenden Befehl im Terminal ausführst:
   ```bash
   python main_bot.py
   ```

2. **Interaktion im Telegram-Chat**:
   Der Bot wird Nachrichten in deinem Telegram-Chat empfangen und das Spiel beginnen, sobald die Teilnehmer einen Teamnamen festgelegt haben.

## Anpassung

- **Eigene Rätsel hinzufügen**: Du kannst in der Datei `riddle_handler.py` eigene Rätsel und die dazugehörige Logik definieren. Die bestehende Struktur erleichtert es, die Rätsel an das gewünschte Escape-Spiel anzupassen.
- **Abschlussbewertung**: Passe die Schlussnachricht oder das Abschlussszenario in der `rating_handler.py` an, um das Spiel je nach Verlauf individuell abzuschließen.

## Hinweise

- **Hinweis- und Hilfefunktion**: Der Bot bietet zwei Optionen für Hinweise:
  - **Automatisierte Hinweise**: Der Bot sendet automatisch Hinweise, wenn die Teilnehmer nach einer festgelegten Zeitspanne keine Lösung gefunden haben.
  - **Manuelle Hinweise über den `/help`-Befehl**: Teilnehmer können selbst einen Hinweis anfordern, indem sie den Befehl `/help` verwenden.
- **Sicherer Umgang mit dem Bot-Token**: Achte darauf, dass die `.env`-Datei in der `.gitignore` aufgelistet ist, um sicherzustellen, dass dein Bot-Token nicht versehentlich veröffentlicht wird.
- **Modularer Aufbau**: Der Bot ist so aufgebaut, dass sich die Hauptfunktionen in verschiedenen Modulen befinden, was die Anpassung und Wartung erleichtert.
- **Zeitmessung**: Der Bot misst die Zeit vom Start des Spiels bis zur Lösung des letzten Rätsels. Diese Zeit wird in der Abschlussevaluation angezeigt.

## Beispiel für eine .gitignore-Datei

Erstelle eine `.gitignore`-Datei im Hauptverzeichnis des Projekts mit folgendem Inhalt, um sicherzustellen, dass sensible Daten und unnötige Dateien nicht ins GitHub-Repository hochgeladen werden:

```plaintext
.env
__pycache__/
*.pyc
venv/
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der Datei `LICENSE`.

---

Viel Spaß beim Entwickeln deines eigenen Escape-Spiels mit dem Telegram Escape Bot! Falls du Fragen hast, wende dich gerne an den Repository-Entwickler.
