"""
CLI to ingest documents and build the vector index.
Usage: python scripts/ingest.py --data-dir ./sample_docs
"""
import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.embeddings import embed_texts, get_client
from src.ingestion import ingest_directory
from src.vector_store import build_index, save_store


def main():
    parser = argparse.ArgumentParser(description="Ingest documents and build RAG index")
    parser.add_argument("--data-dir", default="./sample_docs", help="Directory containing PDF/TXT/MD files")
    parser.add_argument("--output-dir", default="./data", help="Output directory for index and chunks")
    parser.add_argument("--chunk-size", type=int, default=1000)
    parser.add_argument("--overlap", type=int, default=200)
    args = parser.parse_args()

    data_path = Path(args.data_dir)
    if not data_path.is_dir():
        print(f"Error: {data_path} is not a directory")
        sys.exit(1)

    print("Loading and chunking documents...")
    chunks = ingest_directory(data_path, chunk_size=args.chunk_size, overlap=args.overlap)
    if not chunks:
        print("No documents found. Add PDF, TXT, or MD files to", data_path)
        sys.exit(0)

    print(f"Found {len(chunks)} chunks. Generating embeddings...")
    client = get_client()
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(client, texts)
    index = build_index(embeddings)

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    save_store(index, chunks, out)
    print(f"Index saved to {out}. Run: streamlit run app.py")


if __name__ == "__main__":
    main()
