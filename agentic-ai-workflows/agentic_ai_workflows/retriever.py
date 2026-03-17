"""
Retriever: fetches relevant context for a query (in-memory store for demo).
"""
from typing import List


# In-memory demo store. Replace with FAISS/OpenSearch in production.
DEMO_DOCS = [
    {"id": "1", "text": "Project X risks include budget overruns and timeline delays. Mitigation: phased delivery and weekly reviews.", "metadata": {"source": "risk_report.md"}},
    {"id": "2", "text": "Enterprise AI systems require compliance with data residency and audit trails. Use OpenSearch for vector search in regulated environments.", "metadata": {"source": "ai_guidelines.md"}},
    {"id": "3", "text": "RAG pipelines combine retrieval and generation. Best practices: chunk size 500-1000, overlap 200, and source attribution in answers.", "metadata": {"source": "rag_playbook.md"}},
]


def retrieve(query: str, top_k: int = 3) -> List[dict]:
    """
    Simple keyword-style retrieval over DEMO_DOCS.
    For production, use embedding similarity (FAISS/OpenSearch).
    """
    query_lower = query.lower()
    scored = []
    for doc in DEMO_DOCS:
        text = doc.get("text", "").lower()
        score = sum(1 for w in query_lower.split() if w in text)
        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda x: -x[0])
    return [d for _, d in scored[:top_k]]


def format_context(docs: List[dict]) -> str:
    """Format retrieved docs as a single context string."""
    parts = []
    for i, d in enumerate(docs, 1):
        parts.append(f"[{i}] {d.get('text', '')}")
    return "\n\n".join(parts)
