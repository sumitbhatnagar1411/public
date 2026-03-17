"""
Vector store using FAISS. Persists index and metadata for reuse.
"""
import json
import pickle
from pathlib import Path
from typing import List

import faiss
import numpy as np


def build_index(embeddings: List[List[float]]) -> faiss.IndexFlatL2:
    """Build a FAISS index from list of embedding vectors."""
    dim = len(embeddings[0]) if embeddings else 0
    index = faiss.IndexFlatL2(dim)
    matrix = np.array(embeddings, dtype=np.float32)
    index.add(matrix)
    return index


def save_store(index: faiss.IndexFlatL2, chunks: List[dict], base_path: str | Path) -> None:
    """Save FAISS index and chunk metadata to disk."""
    base = Path(base_path)
    base.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(base / "index.faiss"))
    with open(base / "chunks.json", "w", encoding="utf-8") as f:
        # Store only text and metadata for each chunk
        json.dump([{"text": c["text"], "metadata": c.get("metadata", {})} for c in chunks], f, indent=2)


def load_store(base_path: str | Path) -> tuple[faiss.IndexFlatL2, List[dict]]:
    """Load FAISS index and chunks from disk."""
    base = Path(base_path)
    index = faiss.read_index(str(base / "index.faiss"))
    with open(base / "chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return index, chunks


def search(index: faiss.IndexFlatL2, chunks: List[dict], query_embedding: List[float], top_k: int = 5) -> List[dict]:
    """Return top_k chunks nearest to query_embedding."""
    if top_k <= 0:
        return []
    vec = np.array([query_embedding], dtype=np.float32)
    distances, indices = index.search(vec, min(top_k, len(chunks)))
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        chunk = chunks[idx].copy()
        chunk["score"] = float(distances[0][i])
        results.append(chunk)
    return results
