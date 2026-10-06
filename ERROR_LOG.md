# V2 Error Log - 8 Errors Fixed on ThinkPad T14
Date: Oct 1, 2026 - Avanti - Bentonville

1. OOM Error - Fixed with batch_size=32
2. FAISS Dimension Mismatch - Fixed with 384 dim
3. Streamlit Rerun - Fixed with @st.cache_resource
4. Hallucination - Fixed with score < 0.32 guard
5. Slow Retrieval 12s - Fixed top-k 5
6. PDF Corruption - Fixed with PyMuPDF
7. Windows Path Error - Fixed with pathlib
8. Git Not a Repo - Fixed with Web Upload
All fixed Oct 1, 2026 - V2 Production Ready
