import fitz  # PyMuPDF

def extract_text_with_coordinates(pdf_path, page_number):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number)
    for block in page.get_text("dict")["blocks"]:
        for line in block["lines"]:
            for span in line["spans"]:
                print(f"Testo: {span['text']}, Coordinate: {span['bbox']}")
    pdf_document.close()

# Specifica il file PDF e il numero di pagina (0-based)
pdf_path = "input/2021_04.pdf"
page_number = 0
extract_text_with_coordinates(pdf_path, page_number)