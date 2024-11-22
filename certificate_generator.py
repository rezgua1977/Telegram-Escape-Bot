#certificate_generator.py
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
    signature_path = os.path.join(os.path.dirname(__file__), "Bilder", "Signatur.png")
    stamp_path = os.path.join(os.path.dirname(__file__), "Bilder", "Stempel.png")

    # Titelkarte hinzufügen und Abstand nach unten schaffen
    if os.path.exists(image_path):
        pdf.image(image_path, x=10, y=10, w=190)
        pdf.ln(93)

    # Standard-Schriftarten hinzufügen
    pdf.add_font("Arial", "", os.path.join(os.path.dirname(__file__), "Schriftarten", "arial.ttf"), uni=True)
    pdf.add_font("Arial", "B", os.path.join(os.path.dirname(__file__), "Schriftarten", "arialbd.ttf"), uni=True)

    # Rahmen
    pdf.set_draw_color(100, 50, 30)
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, 190, 277)

    # Titel weiter unterhalb des Bildes platzieren
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(212, 175, 55)  # Goldton
    pdf.cell(0, 40, "Zertifikat", 0, 1, "C")
    pdf.ln(8)

    # Einführungstext im "Blocksatz"
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(34, 34, 34)
    intro_text = (
        "Herzlichen Glückwunsch! Sie haben das Spiel erfolgreich abgeschlossen.\n"
        "Wir gratulieren Ihnen zu Ihrer herausragenden Leistung und Ihrem scharfsinnigen Denken.\n"
    )
    pdf.multi_cell(190, 7, intro_text)
    pdf.ln(3)

    # Teamname und Dauer
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Herzlichen Glückwunsch, Team {team_name}!", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Sie haben das Spiel in {game_duration} abgeschlossen.", 0, 1, "C")
    pdf.ln(6)

    # Abschlussnachricht im "Blocksatz"
    closing_text = (
        "Vielen Dank für die Teilnahme an diesem Spiel.\n"
        "Wir hoffen, dass Sie viel Spaß hatten und freuen uns darauf, Sie bei zukünftigen Abenteuern wiederzusehen.\n"
        "Möge Ihr Erfolg Sie weiterhin begleiten.\n"
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
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Abgeschlossen am {current_time}", 0, 1, "C")

    # Speichern des PDFs
    filename = f"certificate_{team_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(tempfile.gettempdir(), filename)
    pdf.output(file_path)

    return file_path

