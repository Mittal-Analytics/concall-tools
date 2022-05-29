import pdftotext


def get_text(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)
        pages = [page for page in pdf]
    return pages
