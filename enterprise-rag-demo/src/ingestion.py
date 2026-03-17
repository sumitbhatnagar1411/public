"""
Document ingestion: load PDF/TXT/MD, chunk with overlap for RAG.
"""
import os
from pathlib import Path
from typing import List

from pypdf import PdfReader


def load_text_file(path: Path) -> str:
    """Load a single text or markdown file."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def load_pdf(path: Path) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def load_document(path: Path) -> str:
    """Dispatch by extension."""
    suf = path.suffix.lower()
    if suf == ".pdf":
        return load_pdf(path)
    if suf in (".txt", ".md", ".markdown"):
        return load_text_file(path)
    raise ValueError(f"Unsupported format: {suf}")


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> List[dict]:
    """
    Split text into overlapping chunks. Each chunk is a dict with 'text' and 'metadata'.
    """
    if not text or not text.strip():
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        piece = text[start:end]
        if not piece.strip():
            start = end - overlap
            continue
        chunks.append({
            "text": piece.strip(),
            "metadata": {"start": start, "end": end},
        })
        start = end - overlap
    return chunks


def ingest_directory(
    data_dir: str | Path,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> List[dict]:
    """
    Load all supported documents from a directory and return list of chunks.
    Each item: { "text": str, "metadata": { "source": path, ... } }
    """
    data_path = Path(data_dir)
    if not data_path.is_dir():
        return []

    all_chunks = []
    for path in data_path.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in (".pdf", ".txt", ".md", ".markdown"):
            continue
        try:
            raw = load_document(path)
            for c in chunk_text(raw, chunk_size=chunk_size, overlap=overlap):
                c["metadata"] = {**c["metadata"], "source": str(path)}
                all_chunks.append(c)
        except Exception as e:
            print(f"Skip {path}: {e}")
    return all_chunks
