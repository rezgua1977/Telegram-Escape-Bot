import os
import tempfile
from fpdf import FPDF
from datetime import datetime
from logger_config import logger  # Importiert den zentralen Logger

# Funktion zur Erstellung der Urkunde als PDF
def generate_certificate(team_name, game_duration):
    pdf = FPDF(format='A4')
    pdf.add_page()

    # Hintergrundfarbe auf ein etwas dunkleres Pergament-ähnliches Beige setzen
    pdf.set_fill_color(235, 215, 190)
    pdf.rect(0, 0, 210, 297, 'F')

    # Pfade für Bild und Schriftarten
    image_path = os.path.join(os.path.dirname(__file__), "Bilder", "Titelkarte.jpg")
    liberationsans_regular = os.path.join(os.path.dirname(__file__), "Schriftart", "LiberationSans-Regular.ttf")
    liberationsans_bold = os.path.join(os.path.dirname(__file__), "Schriftart", "LiberationSans-Bold.ttf")
    dejavusans_path = os.path.join(os.path.dirname(__file__), "Schriftart", "DejaVuSans.ttf")
    signature_path = os.path.join(os.path.dirname(__file__), "Bilder", "Signatur.png")
    stamp_path = os.path.join(os.path.dirname(__file__), "Bilder", "stempel.png")

    # Titelkarte hinzufügen und Abstand nach unten schaffen
    if os.path.exists(image_path):
        pdf.image(image_path, x=10, y=10, w=190)
        pdf.ln(93)

    # Liberation Sans und DejaVu Sans Schriftarten hinzufügen
    if os.path.exists(liberationsans_regular):
        pdf.add_font("LiberationSans", "", liberationsans_regular, uni=True)
    if os.path.exists(liberationsans_bold):
        pdf.add_font("LiberationSans", "B", liberationsans_bold, uni=True)
    if os.path.exists(dejavusans_path):
        pdf.add_font("DejaVuSans", "", dejavusans_path, uni=True)

    # Wasserzeichen in DejaVu Sans
    pdf.set_font("DejaVuSans", "", 50)
    pdf.set_text_color(200, 200, 200)
    pdf.text(30, 150, "✵ ✧ ✪ ✫ ✬ ✯ ✰")

    # Rahmen
    pdf.set_draw_color(100, 50, 30)
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, 190, 277)

    # Titel weiter unterhalb des Bildes platzieren
    pdf.set_font("LiberationSans", "B", 22)
    pdf.set_text_color(212, 175, 55)  # Goldton
    pdf.cell(0, 40, " Rätsel der ", 0, 1, "C")
    pdf.ln(8)

    # Einführungstext im "Blocksatz"
    pdf.set_font("LiberationSans", "", 12)
    pdf.set_text_color(34, 34, 34)
    intro_text = (
        "gelüftet. "
        "der "
        " aufgedeckt.\n"
    )
    pdf.multi_cell(190, 7, intro_text)
    pdf.ln(3)

    # Teamname und Dauer
    pdf.set_font("LiberationSans", "B", 14)
    pdf.cell(0, 10, f"Herzlichen Glückwunsch, Team {team_name}!", 0, 1, "C")
    pdf.set_font("LiberationSans", "", 12)
    pdf.cell(0, 10, f"Ihr habt das Spiel in {game_duration} gelöst.", 0, 1, "C")
    pdf.ln(6)

    # Abschlussnachricht im "Blocksatz"
    closing_text = (
        "Vielen Dank für die Teilnahme an  das Rätsel '.\n"
        " verborgen bleiben... Doch ihr habt bewiesen, dass selbst die tiefsten Rätsel "
        "nicht unlösbar sind, wenn man Mut und Klugheit besitzt.\n"
        "Ihr seid nun Teil einer kleinen Gruppe, "
    )
    pdf.multi_cell(190, 7, closing_text)
    pdf.ln(6)

    # Unterschrift und Stempel
    if os.path.exists(signature_path):
        pdf.image(signature_path, x=140, y=250, w=40)
    if os.path.exists(stamp_path):
        pdf.image(stamp_path, x=30, y=250, w=30)

    # Datum und Uhrzeit zentriert zwischen Stempel und Signatur
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    pdf.set_y(265)
    pdf.set_x(0)
    pdf.set_font("LiberationSans", "", 10)
    pdf.cell(0, 10, f"Abgeschlossen am {current_time}", 0, 1, "C")

    # Speichern des PDFs
    filename = f"certificate_{team_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(tempfile.gettempdir(), filename)
    pdf.output(file_path)

    return file_path
