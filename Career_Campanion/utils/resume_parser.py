
from pypdf import PdfReader
from io import BytesIO


def extract_resume_text(uploaded_file):

    pdf_bytes = BytesIO(uploaded_file.getvalue())

    reader = PdfReader(pdf_bytes)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    if not resume_text.strip():
        raise ValueError(
            "No readable text found. Please upload a text-based PDF."
        )

    return resume_text
