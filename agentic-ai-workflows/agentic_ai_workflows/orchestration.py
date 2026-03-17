"""
Orchestration: run planner → retriever → reasoner workflow.
"""
from typing import Any

from .planner import plan
from .retriever import retrieve, format_context
from .reasoner import reason


def run_workflow(question: str, top_k: int = 3) -> dict[str, Any]:
    """
    Execute: plan → retrieve → reason. Returns full state for inspection.
    """
    # 1. Plan
    plan_out = plan(question)
    sub_tasks = plan_out.get("sub_tasks", [])
    retrieval_query = plan_out.get("retrieval_query", question)
    reasoning_plan = plan_out.get("reasoning", "")

    # 2. Retrieve
    docs = retrieve(retrieval_query, top_k=top_k)
    context = format_context(docs)

    # 3. Reason
    answer = reason(question=question, context=context, sub_tasks=sub_tasks)

    return {
        "question": question,
        "plan": {
            "sub_tasks": sub_tasks,
            "retrieval_query": retrieval_query,
            "reasoning": reasoning_plan,
        },
        "retrieved_docs": docs,
        "answer": answer,
    }
