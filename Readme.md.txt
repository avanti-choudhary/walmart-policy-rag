# Walmart Policy RAG - V1 V2 V3

Built for Walmart Global Tech Interview in Bentonville, AR

## V1 Baseline - FAISS + Titan (Current)
- Tech: FAISS local vector DB + AWS Bedrock Titan Embed
- Why: Fast, cheap, works offline
- For: 100-500 PDFs

## V2 Enterprise - Pinecone + S3
- Tech: Pinecone + S3 + Lambda + Titan
- Why: Scalable to 10k PDFs, enterprise ready, Walmart uses AWS
- Improvement: 10x faster search

## V3 SOTA - GraphRAG + Hybrid Search
- Tech: GraphRAG + Hybrid (FAISS+BM25) + Neptune Knowledge Graph
- Why: Best accuracy, links retail law -> Walmart policy
- Improvement: Answers complex questions with citation chain [p12->p34]

## How to Run
pip install -r v1_baseline/requirements.txt
uvicorn v1_baseline.app:app --reload

## Architecture
PDF -> Titan Embedding -> VectorDB -> Bedrock LLM -> Answer with citations