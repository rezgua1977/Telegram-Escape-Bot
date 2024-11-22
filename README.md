
# Telegram Escape Bot

Der **Telegram Escape Bot** ist ein interaktives Escape-Spiel, das direkt in Telegram gespielt werden kann. Spieler lösen Rätsel, um im Spiel voranzukommen, und erhalten Hinweise bei Bedarf. Der Bot ist vollständig anpassbar und einfach zu installieren.

---

## 📥 Installation

### 1. Projekt herunterladen
Öffne ein Terminal oder die Eingabeaufforderung und führe folgende Befehle aus:
```bash
git clone https://github.com/rezgua1977/Telegram-Escape-Bot.git
cd telegram-escape-bot
```

### 2. Virtuelle Umgebung einrichten
Erstelle und aktiviere eine virtuelle Umgebung, um Abhängigkeiten zu isolieren:

- **Linux/macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

Installiere die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

### 3. Bot konfigurieren
Erstelle eine `.env`-Datei, um sensible Daten wie den Bot-Token sicher zu speichern:
```bash
nano .env
```

Füge folgende Einträge hinzu:
```plaintext
TOKEN=dein_telegram_bot_token
EMAIL_USER=deine_email_adresse
EMAIL_PASS=dein_email_passwort
RECIPIENT_EMAIL=empfaenger_email
```

Speichere und verlasse die Datei.

### 4. Testen des Bots
Starte den Bot manuell:
```bash
python main_bot.py
```

Sende eine Nachricht an den Bot, um sicherzustellen, dass er reagiert.

---

## ⚙️ Einrichtung als Systemdienst
Damit der Bot automatisch gestartet wird, wenn der Server hochfährt, richte ihn als Systemdienst ein.

1. Erstelle die Dienstdatei:
   ```bash
   sudo nano /etc/systemd/system/telegram-escape-bot.service
   ```

2. Füge folgenden Inhalt hinzu:
   ```plaintext
   [Unit]
   Description=Telegram Escape Bot
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/root/telegram-escape-bot
   Environment="TZ=Europe/Berlin"
   ExecStart=/root/telegram-escape-bot/venv/bin/python /root/telegram-escape-bot/main_bot.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   **Hinweis:** Passe die Pfade zu deinem Projekt an.

3. Lade die Systemdienste neu:
   ```bash
   sudo systemctl daemon-reload
   ```

4. Aktiviere und starte den Dienst:
   ```bash
   sudo systemctl enable telegram-escape-bot
   sudo systemctl start telegram-escape-bot
   ```

5. Prüfe den Status:
   ```bash
   sudo systemctl status telegram-escape-bot
   ```

---

## 🛠 Anpassung und Nutzung

### Rätsel bearbeiten mit `riddle_handler.py`

Die Datei `riddle_handler.py` ist der zentrale Ort, an dem die Rätsel und Lösungen definiert sind. Hier kannst du die Logik für jedes Rätsel individuell anpassen.

#### Rätsellösungen definieren
Die Lösungen für die Rätsel werden in einem Dictionary gespeichert:
```python
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

```

- Der Schlüssel (`1`, `2`, etc.) entspricht der Rätselnummer.
- Der Wert ist die richtige Antwort. Es kann sich um einen String oder eine Liste handeln, wenn mehrere Antworten erlaubt sind.

#### Hinweise hinzufügen
Die Funktion `get_hint_text` liefert die Hinweise für jedes Rätsel:
```python
def get_hint_text(riddle_number):
    hints = {
        1: "Hinweis für Rätsel 1.",
        2: "Hinweis für Rätsel 2.",
        3: "Hinweis für Rätsel 3.",
        4: "Hinweis für Rätsel 4.",
        5: "Hinweis für Rätsel 5.",
        6: "Hinweis für Rätsel 6.",
        7: "Hinweis für Rätsel 7.",
        8: "Hinweis für Rätsel 8."
    }
    return hints.get(riddle_number, "Kein Hinweis verfügbar.")

```

- Füge neue Hinweise für deine Rätsel hinzu, indem du das `hints`-Dictionary erweiterst.
- Achte darauf, dass die Schlüssel mit den Rätselnummern übereinstimmen.

#### Rätselbeschreibung anpassen
Jedes Rätsel kann eine eigene Beschreibung haben, die den Spielern angezeigt wird:
```python
def get_riddle_description(riddle_number):
    descriptions = {
        1: "Beschreibung für Rätsel 1.",
        2: "Beschreibung für Rätsel 2.",
        3: "Beschreibung für Rätsel 3.",
        4: "Beschreibung für Rätsel 4.",
        5: "Beschreibung für Rätsel 5.",
        6: "Beschreibung für Rätsel 6.",
        7: "Beschreibung für Rätsel 7.",
        8: "Beschreibung für Rätsel 8."
    }
    return descriptions.get(riddle_number, "Beschreibung fehlt.")


```

#### Neue Rätsel hinzufügen
Wenn du neue Rätsel hinzufügen möchtest:
1. Füge die Lösung im `solutions`-Dictionary hinzu.
2. Ergänze die Beschreibung in `get_riddle_description`.
3. Definiere optional Hinweise in `get_hint_text`.

#### Beispiel für ein neues Rätsel
```python
solutions[9] = "neue_lösung"
def get_hint_text(riddle_number):
    hints = {
        # vorherige Hinweise ...
        9: "Hinweis für Rätsel 9."
    }
    return hints.get(riddle_number, "Kein Hinweis verfügbar.")

def get_riddle_description(riddle_number):
    descriptions = {
        # vorherige Beschreibungen ...
        9: "Beschreibung für Rätsel 9."
    }
    return descriptions.get(riddle_number, "Beschreibung fehlt.")

```

---

## 📋 Nützliche Befehle

- **Bot starten**:  
  ```bash
  sudo systemctl start telegram-escape-bot
  ```

- **Bot stoppen**:  
  ```bash
  sudo systemctl stop telegram-escape-bot
  ```

- **Bot neu starten**:  
  ```bash
  sudo systemctl restart telegram-escape-bot
  ```

- **Logs anzeigen**:  
  ```bash
  sudo journalctl -u telegram-escape-bot
  ```

---

## ❓ Fehlerbehebung

- **Bot reagiert nicht**:
  Stelle sicher, dass der Dienst läuft:
  ```bash
  sudo systemctl status telegram-escape-bot
  ```
  Prüfe die Logs:
  ```bash
  sudo journalctl -u telegram-escape-bot
  ```

- **Fehlende Abhängigkeiten**:
  Installiere die Pakete erneut:
  ```bash
  pip install -r requirements.txt
  ```

- **Probleme mit Zeitzonen**:
  Stelle sicher, dass die Zeitzone korrekt eingestellt ist:
  ```bash
  timedatectl set-timezone Europe/Berlin
  ```

---

## 🌟 Hilfreiche Tipps

- **Lerne Git**: Speichere Änderungen mit Git und GitHub:
  ```bash
  git add .
  git commit -m "Erste Version des Bots"
  git push origin main
  ```

- **Nutze virtuelle Umgebungen**: Verhindere Konflikte zwischen Python-Paketen.

- **Frage um Hilfe**: Nutze Plattformen wie Stack Overflow oder GitHub Discussions.

---

## 📝 Lizenz
Dieses Projekt steht unter der [MIT-Lizenz](LICENSE). Du kannst es frei verwenden, anpassen und teilen.

---

Viel Erfolg mit deinem Telegram Escape Bot! 🎉
