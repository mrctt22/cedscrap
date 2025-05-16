import pdfplumber
import csv
import json
import os

def extract_data_from_pdf(pdf_path, csv_path):
    try:
        # Apri il file PDF
        with pdfplumber.open(pdf_path) as pdf:
            data = []

            # Estrai testo da ogni pagina
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Dividi il testo in righe e aggiungilo ai dati
                    lines = text.split('\n')
                    data.extend(lines)

        # Scrivi i dati estratti in un file CSV
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for row in data:
                writer.writerow([row])

        print(f"Dati estratti e salvati in {csv_path}")

    except Exception as e:
        print(f"Errore durante l'elaborazione: {e}")

def load_config(config_path):
    """Carica i parametri di configurazione da un file JSON."""
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except Exception as e:
        print(f"Errore durante il caricamento del file di configurazione: {e}")
        return None

def process_all_pdfs_in_directory(input_dir, output_dir):
    """Elabora tutti i file PDF nella cartella di input e salva i risultati nella cartella di output."""
    try:
        # Crea la cartella di output se non esiste
        os.makedirs(output_dir, exist_ok=True)

        # Itera su tutti i file nella cartella di input
        for filename in os.listdir(input_dir):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(input_dir, filename)
                csv_filename = os.path.splitext(filename)[0] + ".csv"
                csv_path = os.path.join(output_dir, csv_filename)

                # Elabora il file PDF e salva il risultato in CSV
                print(f"Elaborazione di {pdf_path}...")
                extract_data_from_pdf(pdf_path, csv_path)

    except Exception as e:
        print(f"Errore durante l'elaborazione della directory: {e}")

if __name__ == "__main__":
    # Percorso del file di configurazione
    config_path = "config.json"

    # Carica la configurazione
    config = load_config(config_path)
    if config is None:
        exit(1)

    # Leggi i percorsi delle cartelle dal file di configurazione
    input_dir = config.get("input_dir", "input")
    output_dir = config.get("output_dir", "output")

    # Elabora tutti i file PDF nella cartella di input
    process_all_pdfs_in_directory(input_dir, output_dir)