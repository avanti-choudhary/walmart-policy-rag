from fastapi import FastAPI
import os, fitz
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

app = FastAPI()
chunks = []
vectorizer = None
chunk_vectors = None

def chunk_text(text, size=500, overlap=80):
    out=[]
    start=0
    while start < len(text):
        out.append(text[start:start+size])
        start+=size-overlap
    return out

def load_pdfs():
    global chunks, vectorizer, chunk_vectors
    folder="data"
    all_text=""
    count=0
    for f in os.listdir(folder):
        if f.lower().endswith(".pdf"):
            path=os.path.join(folder,f)
            try:
                doc=fitz.open(path)
                t=""
                for p in doc:
                    t+=p.get_text() or ""
                print(f"Loaded {f}: {len(t)} chars")
                if len(t)>50:
                    all_text+=t+" "
                    count+=1
            except Exception as e:
                print(f"Failed {f}: {e}")
    print(f"Total valid PDFs: {count}")
    if not all_text.strip():
        all_text="Walmart return policy allows 90 days return. Machine learning rag system for testing."
        print("Using dummy text - PDFs had no extractable text")
    chunks=chunk_text(all_text)
    vectorizer=TfidfVectorizer()
    chunk_vectors=vectorizer.fit_transform(chunks)
    print(f"V2 Ready: {len(chunks)} chunks")

load_pdfs()

@app.get("/")
def health():
    return {"status":"V2 sklearn running","chunks":len(chunks)}

@app.get("/ask")
def ask(q: str):
    q_vec=vectorizer.transform([q])
    scores=(chunk_vectors * q_vec.T).toarray().ravel()
    top_idx=np.argsort(scores)[-3:][::-1]
    best=[chunks[i] for i in top_idx]
    return {"question":q,"answer":"\n---\n".join(best)}