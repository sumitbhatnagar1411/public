"""
FastAPI app for Knowledge Graph Entity Demo.
"""
from typing import List, Optional

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from graph.store import store
from graph.model import EntityType, RelationType, entity_id
from graph import queries

app = FastAPI(title="Knowledge Graph Entity Demo", version="1.0.0")


class EntityCreate(BaseModel):
    id: Optional[str] = None
    type: str
    attributes: Optional[dict] = None


class RelationCreate(BaseModel):
    source: str
    target: str
    type: str
    attributes: Optional[dict] = None


@app.get("/entities")
def list_entity_types():
    """Return node counts by type."""
    counts = {}
    for n in store._g.nodes():
        t = store._g.nodes[n].get("type", "unknown")
        counts[t] = counts.get(t, 0) + 1
    return {"entity_counts": counts, "total": store._g.number_of_nodes()}


@app.get("/entities/{etype}/{eid}")
def get_entity(etype: str, eid: str):
    eid_full = f"{etype}:{eid}" if ":" not in eid else eid
    entity = queries.get_entity(eid_full)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    neighbors = queries.get_neighbors(eid_full, limit=20)
    return {"entity": entity, "neighbors": neighbors}


@app.post("/entities")
def create_entity(body: EntityCreate):
    key = (body.attributes or {}).get("key", "gen")
    try:
        etype = EntityType(body.type)
    except ValueError:
        etype = body.type
    eid = body.id or (f"{etype.value}:{key}" if isinstance(etype, EntityType) else f"{etype}:{key}")
    store.add_entity(eid, body.type, body.attributes)
    return {"id": eid, "type": body.type}


@app.post("/relations")
def create_relation(body: RelationCreate):
    store.add_relation(body.source, body.target, body.type, body.attributes)
    return {"source": body.source, "target": body.target, "type": body.type}


@app.get("/query/path")
def query_path(source: str = Query(...), target: str = Query(...), max_depth: int = Query(10, le=20)):
    path_ids = queries.path(source, target, max_depth=max_depth)
    if path_ids is None:
        return {"path": None, "message": "No path found"}
    nodes = [queries.get_entity(n) for n in path_ids]
    return {"path": path_ids, "nodes": nodes}


@app.get("/query/neighbors")
def query_neighbors(entity_id: str = Query(..., alias="entity_id"), hops: int = Query(1, ge=1, le=3)):
    if hops == 1:
        out = queries.get_neighbors(entity_id, limit=50)
        return {"entity_id": entity_id, "hops": 1, "neighbors": out}
    out = queries.k_hop(entity_id, k=hops, limit=100)
    return {"entity_id": entity_id, "hops": hops, "neighbors": out}


@app.get("/stats")
def get_stats():
    return queries.stats()


@app.get("/health")
def health():
    return {"status": "ok"}
