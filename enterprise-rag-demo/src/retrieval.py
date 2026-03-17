"""
RAG: retrieve relevant chunks and generate answer with LLM.
"""
import os
from pathlib import Path
from typing import List

from openai import OpenAI

from .embeddings import embed_texts, get_client
from .vector_store import load_store, search


SYSTEM_PROMPT = """You are an expert assistant that answers questions based only on the provided context.
If the context does not contain enough information, say so. Always cite the source (e.g. "According to [source]") when using a specific passage."""


def build_context(chunks: List[dict]) -> str:
    """Format retrieved chunks as context for the LLM."""
    parts = []
    for i, c in enumerate(chunks, 1):
        src = c.get("metadata", {}).get("source", "unknown")
        parts.append(f"[{i}] (Source: {src})\n{c.get('text', '')}")
    return "\n\n---\n\n".join(parts)


def rag_query(
    question: str,
    data_dir: str | Path = "data",
    top_k: int = 5,
    model: str = "gpt-4o-mini",
) -> tuple[str, List[dict]]:
    """
    Run RAG: embed question, search index, then generate answer.
    Returns (answer_text, retrieved_chunks).
    """
    data_path = Path(data_dir)
    if not (data_path / "index.faiss").exists():
        return "No index found. Please run ingestion first (see README).", []

    index, chunks = load_store(data_path)
    client = get_client()
    q_emb = embed_texts(client, [question])[0]
    retrieved = search(index, chunks, q_emb, top_k=top_k)
    if not retrieved:
        return "No relevant passages found.", []

    context = build_context(retrieved)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    resp = client.chat.completions.create(model=model, messages=messages)
    answer = resp.choices[0].message.content or ""
    return answer, retrieved
