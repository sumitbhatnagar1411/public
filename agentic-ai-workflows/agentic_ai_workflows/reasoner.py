"""
Reasoner agent: produces final answer using context and chain-of-thought.
"""
import os
from openai import OpenAI


def get_client() -> OpenAI:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=key)


def reason(
    question: str,
    context: str,
    sub_tasks: list,
    model: str = "gpt-4o-mini",
) -> str:
    """
    Generate answer with explicit reasoning steps based on context and sub-tasks.
    """
    client = get_client()
    tasks_str = "\n".join(f"- {t}" for t in sub_tasks)
    prompt = f"""You are a reasoning agent. Use the provided context and sub-tasks to answer the user question.

Context:
{context}

Sub-tasks considered:
{tasks_str}

Instructions:
1. Reason step by step (brief).
2. Cite the context when relevant.
3. Give a clear, concise final answer.

Question: {question}

Answer:"""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""
