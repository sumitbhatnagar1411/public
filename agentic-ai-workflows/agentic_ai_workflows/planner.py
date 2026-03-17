"""
Planner agent: decomposes a user question into sub-tasks and a retrieval query.
"""
import os
import json
from typing import List
from openai import OpenAI


def get_client() -> OpenAI:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=key)


def plan(question: str, model: str = "gpt-4o-mini") -> dict:
    """
    Returns:
        {
            "sub_tasks": ["task1", "task2"],
            "retrieval_query": "query to use for document search",
            "reasoning": "brief explanation"
        }
    """
    client = get_client()
    prompt = f"""You are a planning agent. Given the user question, output a JSON object with:
- "sub_tasks": list of 1-3 concrete sub-tasks to answer the question
- "retrieval_query": a single search query to find relevant documents (concise, keyword-rich)
- "reasoning": one sentence on your approach

User question: {question}

Output only valid JSON, no markdown."""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    text = resp.choices[0].message.content or "{}"
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(text)
