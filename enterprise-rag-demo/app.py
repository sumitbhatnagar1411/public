"""
Streamlit UI for Enterprise RAG Demo.
"""
import sys
from pathlib import Path

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from src.embeddings import embed_texts, get_client
from src.ingestion import ingest_directory
from src.retrieval import rag_query
from src.vector_store import build_index, save_store

DATA_DIR = Path("data")
SAMPLE_DOCS = Path("sample_docs")

st.set_page_config(page_title="Enterprise RAG Demo", layout="centered")
st.title("Enterprise RAG Demo")
st.caption("Document ingestion → Embeddings → Vector search → LLM response")

tab1, tab2, tab3 = st.tabs(["Query", "Ingest", "About"])

with tab1:
    question = st.text_area("Ask a question about your documents", height=100, placeholder="e.g. What are the main risks?")
    top_k = st.slider("Number of chunks to retrieve", 1, 10, 5)
    if st.button("Get answer"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching and generating..."):
                answer, chunks = rag_query(question, data_dir=DATA_DIR, top_k=top_k)
            st.markdown("### Answer")
            st.markdown(answer)
            if chunks:
                with st.expander("Retrieved sources"):
                    for i, c in enumerate(chunks, 1):
                        st.markdown(f"**[{i}]** `{c.get('metadata', {}).get('source', '')}`")
                        st.text(c.get("text", "")[:500] + ("..." if len(c.get("text", "")) > 500 else ""))

with tab2:
    st.markdown("Ingest documents from the `sample_docs` folder (or set path).")
    ingest_path = st.text_input("Path to documents", value=str(SAMPLE_DOCS))
    if st.button("Run ingestion"):
        if not Path(ingest_path).is_dir():
            st.error(f"Directory not found: {ingest_path}")
        else:
            with st.spinner("Loading and chunking documents..."):
                chunks = ingest_directory(ingest_path)
            if not chunks:
                st.warning("No supported documents found.")
            else:
                with st.spinner("Generating embeddings and building index..."):
                    client = get_client()
                    texts = [c["text"] for c in chunks]
                    embeddings = embed_texts(client, texts)
                    index = build_index(embeddings)
                    DATA_DIR.mkdir(parents=True, exist_ok=True)
                    save_store(index, chunks, DATA_DIR)
                st.success(f"Indexed {len(chunks)} chunks. You can query in the Query tab.")

with tab3:
    st.markdown("""
    **Enterprise RAG Demo** — Reference architecture for RAG pipelines:
    - Document ingestion (PDF, TXT, MD)
    - OpenAI embeddings and FAISS vector search
    - LLM response with source attribution

    Swap FAISS for **OpenSearch** in production for scale and enterprise features.
    """)
