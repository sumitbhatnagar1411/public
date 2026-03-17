# Enterprise RAG Demo

**Reference architecture for enterprise RAG (Retrieval-Augmented Generation) pipelines using vector search and semantic document retrieval.**

This repository demonstrates a production-style RAG pipeline suitable for financial services and regulated environments: document ingestion, embedding generation, vector storage, and LLM-powered response generation with source attribution.

## Features

- **Document ingestion** — PDF, TXT, and Markdown support with chunking strategies
- **Embeddings** — OpenAI embeddings with configurable chunk size and overlap
- **Vector search** — FAISS for local dev; designed to swap to OpenSearch for production
- **LLM response generation** — GPT-4 with retrieved context and citation
- **Simple UI** — Streamlit app for upload, query, and answer with sources

## Tech Stack

- **Python 3.11+**
- **OpenAI API** (embeddings + chat)
- **FAISS** (vector index) / OpenSearch-ready interface
- **Streamlit** (UI)
- **LangChain** (optional orchestration; this demo uses minimal deps for clarity)

## Quick Start

```bash
# Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
set OPENAI_API_KEY=your-key-here   # Windows
# export OPENAI_API_KEY=your-key-here   # Linux/Mac

# Ingest sample documents (optional)
python scripts/ingest.py --data-dir ./sample_docs

# Run the UI
streamlit run app.py
```

Open http://localhost:8501 to query your knowledge base.

## Project Structure

```
enterprise-rag-demo/
├── app.py                 # Streamlit UI
├── src/
│   ├── ingestion.py       # Document loaders and chunking
│   ├── embeddings.py       # Embedding generation
│   ├── vector_store.py     # FAISS vector store wrapper
│   └── retrieval.py        # Retrieve + generate (RAG chain)
├── scripts/
│   └── ingest.py          # CLI for bulk ingestion
├── sample_docs/           # Example documents
├── data/                  # Persisted index and chunks (gitignored)
└── requirements.txt
```

## Configuration

- **Chunk size / overlap**: Edit `src/ingestion.py` (default 1000 chars, 200 overlap).
- **Model**: Set in `src/retrieval.py` (e.g. `gpt-4o-mini` for cost, `gpt-4o` for quality).
- **Top-K**: Number of retrieved chunks in `src/retrieval.py`.

## License

MIT

## Author

Sumit Bhatnagar — [LinkedIn](https://linkedin.com/in/sumitbhatnagar1411) Chase
