import pdfplumber
import re
import os
from pathlib import Path
import json

# Percorso del file di configurazione
config_path = "config/config.json"

# Carica la configurazione
def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except Exception as e:
        print(f"Errore durante il caricamento del file di configurazione: {e}")
        return None

config = load_config(config_path)
if config is None:
    print("Errore: Configurazione non caricata. Uscita dal programma.")
    exit(1)

def debug_print(message):
    """Stampa messaggi di debug solo se flag_debug è impostato a 'Y'."""
    if config.get("flag_debug", "N") == "Y":
        print(message)

debug_print(f"Caricamento configurazione da: {config_path}")

# Percorsi delle cartelle dal file di configurazione
cartella_pdf = config.get("preinput_dir", "preinput")
cartella_output = config.get("input_dir", "input")
debug_print(f"Cartella PDF di input: {cartella_pdf}")
debug_print(f"Cartella di output: {cartella_output}")

# Crea la cartella di output se non esiste
os.makedirs(cartella_output, exist_ok=True)
debug_print(f"Cartella di output creata (se non esisteva già): {cartella_output}")

# Modifica il pattern per includere "AGG" opzionale alla fine
pattern_periodo = r"(Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre)\s+\d{4}(?:\s+AGG)?"

# Itera sui file PDF nella cartella di input
for file in Path(cartella_pdf).glob("*.pdf"):
    debug_print(f"Trovato file PDF: {file.name}")
    try:
        with pdfplumber.open(file) as pdf:
            debug_print(f"Aperto file PDF: {file.name}")
            testo_completo = ""
            for pagina_num, pagina in enumerate(pdf.pages, start=1):
                testo = pagina.extract_text()
                debug_print(f"Estratto testo dalla pagina {pagina_num} del file {file.name}")
                if testo:
                    testo_completo += testo + "\n"

        # Cerca il periodo
        match = re.search(pattern_periodo, testo_completo)
        if match:
            periodo = match.group()  # es. Aprile 2021 o Aprile 2021 AGG
            mese, anno = periodo.split()[:2]
            mesi = {
                "Gennaio": "01", "Febbraio": "02", "Marzo": "03", "Aprile": "04", "Maggio": "05", "Giugno": "06",
                "Luglio": "07", "Agosto": "08", "Settembre": "09", "Ottobre": "10", "Novembre": "11", "Dicembre": "12"
            }
            mese_numero = mesi.get(mese, "00")

            # Controlla se il suffisso "AGG" è presente
            suffisso = "_AGG" if "AGG" in periodo else ""
            nuovo_nome = f"{anno}_{mese_numero}{suffisso}.pdf"  # es. 2021_04_AGG.pdf o 2021_04.pdf
            nuovo_percorso = Path(cartella_output) / nuovo_nome
            debug_print(f"Periodo trovato: {periodo}. Nuovo nome: {nuovo_nome}")

            # Evita sovrascritture
            counter = 1
            while nuovo_percorso.exists():
                debug_print(f"Il file {nuovo_percorso.name} esiste già. Incremento il contatore.")
                nuovo_nome = f"{anno}_{mese_numero}{suffisso}_{counter}.pdf"
                nuovo_percorso = Path(cartella_output) / nuovo_nome
                counter += 1

            # Rinominare il file dopo aver chiuso il PDF
            os.rename(file, nuovo_percorso)
            debug_print(f"File rinominato e spostato: {file.name} ➜ {nuovo_percorso.name}")
        else:
            debug_print(f"Periodo non trovato nel file {file.name}")
    except Exception as e:
        debug_print(f"Errore durante l'elaborazione del file {file.name}: {e}")
