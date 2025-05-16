import os
import json
import pandas as pd

def merge_csv_files(input_folder, output_file):
    # Lista per memorizzare i DataFrame
    dataframes = []

    # Itera attraverso i file nella cartella
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            # Legge il file CSV
            df = pd.read_csv(file_path)
            # Aggiunge una colonna 'FILENAME' come primo campo con il nome del file senza estensione
            df.insert(0, 'FILENAME', '' + os.path.splitext(filename)[0] + '')
            # Aggiunge il DataFrame alla lista
            dataframes.append(df)

    # Concatena tutti i DataFrame in uno solo
    merged_df = pd.concat(dataframes, ignore_index=True)
    # Salva il DataFrame unito in un nuovo file CSV
    merged_df.to_csv(output_file, index=False)
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

    # Leggi i percorsi delle cartelle dal file di configurazione
    output_dir = config.get("output_dir", "output")
    output_file = output_dir + "/" + config.get("output_file", "output_file")

    # Cancella il file di output se esiste
    if os.path.exists(output_file):
        os.remove(output_file)
merge_csv_files(output_dir, output_file)