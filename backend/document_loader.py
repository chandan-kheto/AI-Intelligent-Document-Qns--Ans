
import os, PyPDF2
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text


def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text(file_path: str) -> str:
    """
    Universal extractor for PDF, DOCX, TXT.
    Handles weird filename cases safely.
    """

    # Clean path and detect extension safely
    clean_path = file_path.strip()
    extension = os.path.splitext(clean_path)[1].lower().strip()

    print("📄 Detected file extension:", extension)

    if extension == ".pdf":
        return extract_text_from_pdf(clean_path)

    elif extension == ".docx":
        return extract_text_from_docx(clean_path)

    elif extension == ".txt":
        return extract_text_from_txt(clean_path)

    else:
        raise ValueError(
            f"Unsupported file type '{extension}'. "
            "Please upload PDF, DOCX, or TXT."
        )
