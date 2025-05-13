import pdfplumber
import docx2txt
import os
from io import BytesIO

def search_candidate_web(name: str) -> dict:
    # Simulate search results
    return {
        "github": f"https://github.com/{name.lower().replace(' ', '')}",
        "blog": f"https://medium.com/@{name.lower().replace(' ', '')}"
    }

def extract_text_from_resume(file) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    contents = file.file.read()  # Read file content into memory

    if ext == ".pdf":
        with pdfplumber.open(BytesIO(contents)) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    elif ext == ".docx":
        return docx2txt.process(BytesIO(contents))

    return ""
