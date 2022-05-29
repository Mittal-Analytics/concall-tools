import fitz


def get_text(pdf_path):
    doc = fitz.open(pdf_path)
    return doc
