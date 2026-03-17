"""
Embedding generation using OpenAI API.
"""
import os
from typing import List

from openai import OpenAI


def get_client() -> OpenAI:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def embed_texts(client: OpenAI, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Get embeddings for a list of texts. Returns list of vectors."""
    if not texts:
        return []
    # OpenAI allows batches; 100 is safe
    batch_size = 100
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        resp = client.embeddings.create(input=batch, model=model)
        for e in resp.data:
            all_embeddings.append(e.embedding)
    return all_embeddings
