import fitz  # PyMuPDF
from pytesseract import pytesseract
from PIL import Image
import csv
import json
import os
import re

# Funzione per caricare la configurazione
def load_config(config_path):
    """Carica i parametri di configurazione da un file JSON."""
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except Exception as e:
        print(f"Errore durante il caricamento del file di configurazione: {e}")
        return None

# Funzione centralizzata per la stampa di debug
DEBUG_MODE = False

def debug_print(message):
    if DEBUG_MODE:
        print(f"DEBUG: {message}")

# Funzione centralizzata per la stampa degli errori
def error_print(message):
    print(f"ERRORE: {message}")
    debug_print(message)

# Funzione per mostrare l'immagine ritagliata durante il debug
SHOW_IMAGE_DEBUG = False

def show_cropped_image(image, key):
    if SHOW_IMAGE_DEBUG:
        image.show(title=f"Cropped Image for {key}")

def extract_structured_data_from_pdf(pdf_path, csv_path, config):
    """Estrae dati strutturati da un PDF utilizzando OCR e li salva in un file CSV."""
    try:
        debug_print(f"Apertura del file PDF: {pdf_path}")
        pdf_document = fitz.open(pdf_path)
        structured_data = []

        # Leggi le coordinate dal file di configurazione
        coordinates = config.get("ocr_coordinates")

        # Carica solo l'ultima pagina del PDF
        last_page_number = len(pdf_document) - 1
        debug_print(f"Estrazione dell'ultima pagina: {last_page_number + 1}")
        page = pdf_document.load_page(last_page_number)
        zoom_level = config.get("ocr_zoom_level", 1.0)
        mat = fitz.Matrix(zoom_level, zoom_level)
        pix = page.get_pixmap(matrix=mat)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        page_data = {}
        for key, (x1, y1, x2, y2) in coordinates.items():
            cropped_image = image.crop((x1*zoom_level, y1*zoom_level, x2*zoom_level, y2*zoom_level))
            cropped_image = cropped_image.convert("L")
            show_cropped_image(cropped_image, key)
            debug_print(f"Esecuzione OCR per {key} nella pagina {last_page_number + 1}")
            text = pytesseract.image_to_string(cropped_image, config='--psm 7')
            debug_print(f"Testo riconosciuto per {key}: {text.strip()}")
            if text.strip():
                page_data[key] = text.strip()

        if page_data:
            structured_data.append(page_data)

        pdf_document.close()

        # Scrivi i dati strutturati in un file CSV
        debug_print(f"Scrittura dei dati strutturati nel file CSV: {csv_path}")
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=coordinates.keys())
            writer.writeheader()
            writer.writerows(structured_data)

        print(f"Dati strutturati estratti e salvati in {csv_path}")

    except Exception as e:
        error_print(f"Errore durante l'elaborazione del file PDF: {e}")

def process_all_pdfs_in_directory(input_dir, output_dir, config):
    """Elabora tutti i file PDF nella cartella di input e salva i risultati nella cartella di output."""
    try:
        debug_print(f"Creazione della cartella di output: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

        for filename in os.listdir(input_dir):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(input_dir, filename)
                csv_filename = os.path.splitext(filename)[0] + ".csv"
                csv_path = os.path.join(output_dir, csv_filename)
                debug_print(f"Elaborazione del file PDF: {pdf_path}")
                extract_structured_data_from_pdf(pdf_path, csv_path, config)
                #extract_table_data_from_pdf(pdf_path, csv_path, config)

    except Exception as e:
        error_print(f"Errore durante l'elaborazione della directory: {e}")

# Funzione disattivata: estrazione tabella da PDF tramite OCR
# def extract_table_data_from_pdf(pdf_path, csv_path, config):
#     """Estrae i dati di una tabella da un PDF utilizzando OCR su aree configurate e li salva in un file CSV."""
#     try:
#         debug_print(f"Apertura del file PDF per tabella: {pdf_path}")
#         pdf_document = fitz.open(pdf_path)
#         last_page_number = len(pdf_document) - 1
#         page = pdf_document.load_page(last_page_number)
#         zoom_level = config.get("ocr_zoom_level", 1.0)
#         mat = fitz.Matrix(zoom_level, zoom_level)
#         pix = page.get_pixmap(matrix=mat)
#         image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#
#         coordinates = config.get("ocr_table_coordinates", {})
#         if not coordinates:
#             error_print("Nessuna area tabella configurata in ocr_table_coordinates.")
#             return
#
#         table_data = []
#         header = list(coordinates.keys())
#         row = {}
#         for key, (x1, y1, x2, y2) in coordinates.items():
#             cropped_image = image.crop((x1*zoom_level, y1*zoom_level, x2*zoom_level, y2*zoom_level))
#             cropped_image = cropped_image.convert("L")
#             show_cropped_image(cropped_image, key)
#             debug_print(f"Esecuzione OCR per area tabella {key}")
#             text = pytesseract.image_to_string(cropped_image, config='--psm 6')
#             debug_print(f"Testo riconosciuto per {key}: {text.strip()}")
#             row[key] = text.strip()
#         table_data.append(row)
#
#         pdf_document.close()
#
#         # Scrivi i dati estratti in un file CSV
#         debug_print(f"Scrittura dati tabella in {csv_path}")
#         write_header = not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0
#         with open(csv_path, mode='a', newline='', encoding='utf-8') as csv_file:
#             writer = csv.DictWriter(csv_file, fieldnames=header)
#             if write_header:
#                 writer.writeheader()
#             writer.writerows(table_data)
#         print(f"Dati tabella estratti e aggiunti in {csv_path}")
#     except Exception as e:
#         error_print(f"Errore durante l'estrazione tabella: {e}")

if __name__ == "__main__":
    # Percorso del file di configurazione
    config_path = "config/config.json"

    # Carica la configurazione
    config = load_config(config_path)
    if config is None:
        exit(1)

    # Imposta il path di tesseract da config, se presente
    pytesseract.tesseract_cmd = config.get("tesseract_path")

    # Imposta le variabili di debug globali
    DEBUG_MODE = config.get("flag_debug", "N") == "Y"
    SHOW_IMAGE_DEBUG = DEBUG_MODE

    # Leggi i percorsi delle cartelle dal file di configurazione
    input_dir = config.get("input_dir", "input")
    output_dir = config.get("output_dir", "output")

    # Elabora tutti i file PDF nella cartella di input
    process_all_pdfs_in_directory(input_dir, output_dir, config)