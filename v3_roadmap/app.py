import pathlib
import streamlit as st

DATA_DIR = pathlib.Path(__file__).parent / "data"

@st.cache_resource
def load_pdfs():
    docs = []
    for p in DATA_DIR.glob("*"):
        if p.suffix.lower() == ".pdf":
            try:
                import fitz # PyMuPDF - V2 Fix #6
                doc = fitz.open(p)
                text = ""
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
                if text.strip():
                    docs.append(text)
            except:
                pass
        elif p.suffix.lower() == ".txt":
            docs.append(p.read_text(encoding="utf-8", errors="ignore"))

    # fallback to policy.txt from V2 if V3 data empty - your smart fix
    if not docs:
        fallback = pathlib.Path(__file__).parent.parent / "v2_explored" / "data"
        if fallback.exists():
            for p in fallback.glob("*"):
                if p.suffix.lower() in [".pdf", ".txt"]:
                    try:
                        if p.suffix.lower() == ".pdf":
                            import fitz
                            doc = fitz.open(p)
                            text = ""
                            for page in doc:
                                text += page.get_text() + "\n"
                            doc.close()
                            if text.strip():
                                docs.append(text)
                        else:
                            docs.append(p.read_text(encoding="utf-8", errors="ignore"))
                    except:
                        pass
    return docs

@st.cache_resource
def build_index():
    from sentence_transformers import SentenceTransformer
    import faiss
    docs = load_pdfs()
    # V2 Fix #1 OOM - batch_size=32 for T420 4GB RAM
    # V2 Fix #2 FAISS Dimension Mismatch - 384 dim
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs, batch_size=32, show_progress_bar=True)
    index = faiss.IndexFlatL2(384)
    index.add(embeddings)
    return index, docs, model

def retrieve(query, k=5):
    # V2 Fix #5 Slow Retrieval 12s -> top-k 5
    index, docs, model = build_index()
    q_emb = model.encode([query])
    scores, ids = index.search(q_emb, k)
    # V2 Fix #4 Hallucination - score < 0.32 guard
    results = []
    for score, idx in zip(scores[0], ids[0]):
        if score < 0.32:
            results.append(docs[idx])
    return results

def main():
    st.title("Walmart Policy RAG - V3 Roadmap")
    query = st.text_input("Ask policy question:")
    if query:
        results = retrieve(query)
        for r in results:
            st.write(r[:500])

if __name__ == "__main__":
    main()