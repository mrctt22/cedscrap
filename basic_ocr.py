from pytesseract import pytesseract

# Configura manualmente il percorso di Tesseract
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image

def perform_ocr(image_path):
    """Esegue OCR su un'immagine e stampa il testo riconosciuto."""
    try:
        # Configura il percorso di Tesseract se necessario
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Carica l'immagine
        image = Image.open(image_path)

        # Esegui OCR
        text = pytesseract.image_to_string(image, lang='eng', config='--psm 7')

        # Stampa il testo riconosciuto
        print("Testo riconosciuto:")
        print(text)

    except Exception as e:
        print(f"Errore durante l'esecuzione dell'OCR: {e}")

if __name__ == "__main__":
    # Percorso dell'immagine da analizzare
    image_path = "C:\\Users\\mrctt\\Desktop\\ocrtest.jpg"  # Modifica con il percorso della tua immagine

    # Esegui OCR sull'immagine
    perform_ocr(image_path)