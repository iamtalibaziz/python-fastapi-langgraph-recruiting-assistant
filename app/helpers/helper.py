import pdfplumber
import docx2txt
import os

def search_candidate_web(name: str) -> dict:
    # Simulate search results
    return {
        "github": f"https://github.com/{name.lower().replace(' ', '')}",
        "blog": f"https://medium.com/@{name.lower().replace(' ', '')}"
    }

def extract_text_from_resume(file) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    contents = file.file.read()
    
    if ext == ".pdf":
        temp_path = "temp.pdf"
        with open(temp_path, "wb") as f:
            f.write(contents)
        try:
            with pdfplumber.open(temp_path) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        finally:
            os.remove(temp_path)
    
    elif ext == ".docx":
        temp_path = "temp.docx"
        with open(temp_path, "wb") as f:
            f.write(contents)
        try:
            return docx2txt.process(temp_path)
        finally:
            os.remove(temp_path)

    return ""
