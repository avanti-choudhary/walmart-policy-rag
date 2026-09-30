# Walmart Policy RAG — V1 LIVE ✅ | V2 | V3

> Live RAG system for policy Q&A with citations. Educational project — NOT affiliated with Walmart.

**Author:** Avanti Choudhary (Bentonville, AR) | Applications: Senior/Staff/Director SWE @ Walmart — Under Review
**GitHub:** github.com/avanti-choudhary

### 🔴 LIVE PROOF — Sept 30, 2026 — NOT FAKE
V1 is running locally. See proof in `/assets/proof/`

- Endpoint: `GET /ask?q=What is Walmart return policy?`
- Status: `200 OK`
- Response: `{"citation": "[Walmart_Return_Policy.pdf p.1-2]", "source": "Real PDF"}`
- Docs: `http://127.0.0.1:8001/docs` — Swagger UI live
- Screenshot: `/assets/proof/v1_200_ok.png` + screen recording

### Architecture
- **V1 — policy-rag-baseline [LIVE]:** FAISS-CPU + FastAPI + PyPDF2, baseline retrieval
- **V2 — policy-rag-learning-prototype [IN PROG]:** ChromaDB + Sentence-Transformers
- **V3 — Next:** LLM + RAG chain + guardrails

### How Recruiter Can Verify (2 mins)
1. git clone https://github.com/avanti-choudhary/walmart-policy-rag
2. pip install -r requirements.txt
3. uvicorn app.v1.main:app --port 8001 --reload
4. Open http://127.0.0.1:8001/docs -> Execute /ask
5. Check /assets/proof/ for live screenshots + video

### Tech Stack
Python, FastAPI, FAISS, ChromaDB, Sentence-Transformers, Uvicorn

### Link for Resume & Walmart Careers
https://github.com/avanti-choudhary/walmart-policy-rag
