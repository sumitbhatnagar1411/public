"""
FastAPI app for Agentic AI Workflows.
"""
from fastapi import FastAPI
from pydantic import BaseModel

from agentic_ai_workflows.orchestration import run_workflow

app = FastAPI(title="Agentic AI Workflows", version="1.0.0")


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


class QueryResponse(BaseModel):
    question: str
    answer: str
    plan: dict
    retrieved_docs: list


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    result = run_workflow(req.question, top_k=req.top_k)
    return QueryResponse(
        question=result["question"],
        answer=result["answer"],
        plan=result["plan"],
        retrieved_docs=result["retrieved_docs"],
    )


@app.get("/health")
def health():
    return {"status": "ok"}
