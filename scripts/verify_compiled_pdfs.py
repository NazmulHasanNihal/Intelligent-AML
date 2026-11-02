import pypdf
from pathlib import Path

def inspect_pdf(pdf_path):
    if not pdf_path.exists():
        print(f"Error: {pdf_path} does not exist.")
        return
    reader = pypdf.PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    print(f"=== {pdf_path.name} ({num_pages} pages) ===")
    question_marks = []
    garbled_pages = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if "??" in text:
            question_marks.append(idx + 1)
        if "1 1 1 1 1 1 1" in text or "1111111111" in text:
            garbled_pages.append(idx + 1)
    
    qm_msg = question_marks if question_marks else "None (Clean!)"
    gp_msg = garbled_pages if garbled_pages else "None (Clean!)"
    print(f"  Unresolved ?? references on pages: {qm_msg}")
    print(f"  Garbled pages: {gp_msg}")

if __name__ == "__main__":
    base = Path(".")
    inspect_pdf(base / "papers" / "EAAI_Research_Paper" / "Anonymized_Manuscript.pdf")
    inspect_pdf(base / "papers" / "EAAI_Research_Paper" / "Anonymized_Supplementary.pdf")
    inspect_pdf(base / "papers" / "University_CSE_Thesis" / "main.pdf")

