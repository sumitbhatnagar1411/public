# Knowledge Graph Entity Demo

**Reference implementation for modeling complex entity relationships — aligned with TigerGraph-style graph analytics.**

This repo demonstrates a knowledge graph for entities and relationships: nodes (e.g. Customer, Account, Product), edges (OWNS, TRANSACTED_WITH, REFERRED_BY), and query patterns such as path finding, neighborhood expansion, and relationship analytics. Useful as a conceptual reference for graph-based AI and entity resolution in FinTech.

## Features

- **Entity and relationship model** — Typed nodes and edges
- **Graph operations** — Add/query nodes, edges; path finding; k-hop neighborhood
- **REST API** — FastAPI endpoints for graph CRUD and analytics
- **Sample data** — Customers, accounts, transactions for demo scenarios
- **Designed to map to TigerGraph/Neo4j** — Same concepts translate to production graph DBs

## Tech Stack

- **Python 3.11+**
- **NetworkX** (in-memory graph; swap to TigerGraph/Neo4j for scale)
- **FastAPI** — REST API
- **Pydantic** — Schemas

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Load sample data and start API
python scripts/load_sample.py
uvicorn app:app --reload
```

Then try:
- `GET /entities` — list entity types and counts
- `GET /entities/customer/{id}` — get customer and direct relationships
- `POST /query/path` — find path between two entities
- `GET /query/neighbors?entity_id=...&hops=2` — k-hop neighborhood

## Project Structure

```
knowledge-graph-entity-demo/
├── app.py              # FastAPI app
├── graph/
│   ├── model.py       # Node/edge types and schema
│   ├── store.py       # In-memory graph (NetworkX)
│   └── queries.py    # Path, neighbors, analytics
├── scripts/
│   └── load_sample.py # Load demo data
└── requirements.txt
```

## License

MIT

## Author

Sumit Bhatnagar — [LinkedIn](https://linkedin.com/in/sumitbhatnagar1411) 
