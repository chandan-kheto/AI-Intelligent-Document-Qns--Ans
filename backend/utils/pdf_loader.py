

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract full text from PDF"""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text
