# Agentic AI Workflows

**Demo of multi-agent orchestration with retrieval and reasoning chains for enterprise use cases.**

This repository illustrates agentic AI patterns: a **planner** that decomposes tasks, a **retriever** that fetches context, and a **reasoner** that produces answers — orchestrated in a simple workflow. Suitable as a reference for building autonomous multi-step AI agents that reason, plan, and act.

## Features

- **Multi-agent orchestration** — Planner → Retriever → Reasoner pipeline
- **Retrieval** — Document search (in-memory or FAISS) feeding context to the reasoner
- **Reasoning chains** — Step-by-step reasoning with tool use (search, summarize)
- **Simple CLI and API** — Run workflows from command line or FastAPI

## Tech Stack

- **Python 3.11+**
- **OpenAI API** (GPT-4 for planner and reasoner)
- **LangGraph** (optional) or custom state machine
- **FAISS** / in-memory store for retrieval demo
- **FastAPI** (optional API server)

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
set OPENAI_API_KEY=your-key

# Run a single workflow (plan → retrieve → reason)
python -m agentic_ai_workflows.run "What are the main risks in project X?"

# Or start the API
uvicorn app:app --reload
```

## Project Structure

```
agentic-ai-workflows/
├── agentic_ai_workflows/
│   ├── planner.py      # Task decomposition
│   ├── retriever.py    # Context retrieval
│   ├── reasoner.py     # Answer generation with chain-of-thought
│   ├── orchestration.py # Workflow runner
│   └── run.py         # CLI entry
├── app.py             # FastAPI server (optional)
├── data/              # Sample docs for retrieval
└── requirements.txt
```

## License

MIT

## Author

Sumit Bhatnagar — [LinkedIn](https://linkedin.com/in/sumitbhatnagar1411)