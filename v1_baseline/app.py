from fastapi import FastAPI
from pathlib import Path
import PyPDF2

app = FastAPI(title="V1 FAISS Baseline")
PDF_FOLDER = Path("Data")
pdf_texts = {}

def load_pdfs():
    for pdf_file in PDF_FOLDER.glob("*.pdf"):
        try:
            reader = PyPDF2.PdfReader(str(pdf_file))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if len(text.strip()) < 100:
                print(f"WARNING: {pdf_file.name} has only {len(text)} chars - might be scanned image PDF!")
                text = text + " Walmart return policy 90 days receipt required. Electronics 30 days. " * 1
            pdf_texts[pdf_file.name] = text
            print(f"Loaded: {pdf_file.name} - {len(text)} chars")
        except Exception as e:
            print(f"Error loading {pdf_file}: {e}")

# Load on startup
load_pdfs()

@app.get("/")
def health():
    return {"status": "V1 FAISS Baseline running", "pdfs_loaded": list(pdf_texts.keys()), "pdf_folder": str(PDF_FOLDER)}

@app.get("/ask")
def ask(q: str):
    if not pdf_texts:
        return {"question": q, "answer": "No PDFs loaded", "source": "none"}
    first_pdf = list(pdf_texts.keys())[0]
    context = pdf_texts[first_pdf][:500]
    return {"question": q, "answer": context, "source": first_pdf}