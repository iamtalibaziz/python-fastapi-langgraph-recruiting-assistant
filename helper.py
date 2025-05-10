import pdfplumber
import docx2txt
import os

def search_candidate_web(name: str) -> dict:
    # Simulate search results
    return {
        "github": f"https://github.com/{name.lower().replace(' ', '')}",
        "blog": f"https://medium.com/@{name.lower().replace(' ', '')}"
    }


# def extract_text_from_resume(file) -> str:
#     ext = os.path.splitext(file.filename)[1].lower()
#     contents = file.file.read()
#     if ext == ".pdf":
#         with open("temp.pdf", "wb") as f:
#             f.write(contents)
#         with pdfplumber.open("temp.pdf") as pdf:
#             return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
#     elif ext == ".docx":
#         with open("temp.docx", "wb") as f:
#             f.write(contents)
#         return docx2txt.process("temp.docx")
#     else:
#         return ""

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

def compare_profile_to_jd(profile: dict, jd_summary: str) -> tuple:
    skills_match = list(set(profile["skills"]).intersection(set(["Python", "ML", "FastAPI"])))
    matrix = {
        "skills_matched": skills_match,
        "experience": profile["experience"],
    }
    score = "Strong Fit" if len(skills_match) >= 2 else "Moderate Fit"
    explanation = f"Matched skills: {skills_match}. Based on experience and certifications, candidate is a {score}."
    return score, matrix, explanation