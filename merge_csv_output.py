import os
import json
import pandas as pd

def debug_print(message, debug=False):
    if debug:
        print(f"DEBUG: {message}")

def merge_csv_files(input_folder, output_file, debug=False):
    # Lista per memorizzare i DataFrame
    dataframes = []
    # Ordina i file per nome per unione ordinata
    csv_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.csv')])
    if not csv_files:
        print("Nessun file CSV trovato nella cartella di input.")
        return
    # Itera attraverso i file CSV ordinati
    for filename in csv_files:
        file_path = os.path.join(input_folder, filename)
        try:
            # Legge il file CSV
            df = pd.read_csv(file_path)
            # Aggiunge una colonna 'FILENAME' come primo campo con il nome del file senza estensione
            df.insert(0, 'FILENAME', os.path.splitext(filename)[0])
            # Aggiunge il DataFrame alla lista
            dataframes.append(df)
            debug_print(f"File aggiunto: {filename}", debug)
        except Exception as e:
            print(f"Errore nella lettura di {filename}: {e}")
    if not dataframes:
        print("Nessun file CSV valido da unire.")
        return
    try:
        # Concatena tutti i DataFrame in uno solo
        merged_df = pd.concat(dataframes, ignore_index=True, join='outer')
        # Salva il DataFrame unito in un nuovo file CSV
        merged_df.to_csv(output_file, index=False)
        print(f"File CSV unito creato: {output_file}")
    except Exception as e:
        print(f"Errore durante la scrittura del file CSV unito: {e}")

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
    output_file = os.path.join(output_dir, config.get("output_file", "output_file.csv"))
    debug = config.get("flag_debug", "N") == "Y"
    # Cancella il file di output se esiste
    if os.path.exists(output_file):
        os.remove(output_file)
    merge_csv_files(output_dir, output_file, debug)