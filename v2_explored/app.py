import os, pymupdf
import numpy as np
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()
chunks = []
vectorizer = None
chunk_vectors = None

def chunk_text(text, size=300):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

def load_pdfs():
    global chunks, vectorizer, chunk_vectors
    folder="data"
    all_text=""
    for file in os.listdir(folder):
        path=os.path.join(folder,file)
        if file.endswith(".pdf"):
            try:
                doc=pymupdf.open(path)
                t=""
                for page in doc:
                    t+=page.get_text()
                print(f"Loaded {file}: {len(t)} chars")
                if len(t.strip())>20:
                    all_text+=t+"\n"
            except Exception as e:
                print(f"Error {file}: {e}")
        elif file.endswith(".txt"):
            with open(path,"r",encoding="utf-8") as f:
                txt=f.read()
                print(f"Loaded {file}: {len(txt)} chars")
                all_text+=txt+"\n"
    print(f"Total: {len(all_text)} chars")
    if len(all_text.strip())<20:
        all_text="Walmart Return Policy. General 90 days. Electronics TVs computers 30 days. Groceries non-returnable. Without receipt under $10 cash else gift card."
    chunks=chunk_text(all_text)
    vectorizer=TfidfVectorizer()
    chunk_vectors=vectorizer.fit_transform(chunks)
    print(f"V2 Ready: {len(chunks)} chunks")

# Load immediately on start
load_pdfs()

@app.get("/")
def health():
    return {"status":"V2 sklearn running","chunks":len(chunks)}

@app.get("/ask")
def ask(q: str):
    global vectorizer, chunk_vectors, chunks
    if vectorizer is None or len(chunks)==0:
        load_pdfs()
    q_vec=vectorizer.transform([q])
    scores=(chunk_vectors * q_vec.T).toarray().ravel()
    top_idx=np.argsort(scores)[-3:][::-1]
    best=[chunks[i] for i in top_idx]
    return {"question":q,"answer":"\n---\n".join(best)}