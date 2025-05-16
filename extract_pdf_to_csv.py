import pdfplumber
import csv
import json

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

if __name__ == "__main__":
    # Percorso del file di configurazione
    config_path = "config/config.json"

    # Carica la configurazione
    config = load_config(config_path)
    if config is None:
        exit(1)

    # Leggi i percorsi dal file di configurazione
    pdf_path = config.get("pdf_path", "input.pdf")
    csv_path = config.get("csv_path", "output.csv")

    # Esegui l'estrazione dei dati
    extract_data_from_pdf(pdf_path, csv_path)