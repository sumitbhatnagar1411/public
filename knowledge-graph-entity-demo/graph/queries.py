"""
Graph query helpers — path, neighbors, analytics.
"""
from typing import List, Optional

from .store import store


def get_entity(eid: str):
    return store.get_entity(eid)


def get_neighbors(eid: str, direction: str = "out", relation_type: Optional[str] = None, limit: int = 50):
    return store.get_neighbors(eid, direction=direction, relation_type=relation_type, limit=limit)


def k_hop(eid: str, k: int = 2, limit: int = 100):
    return store.get_k_hop(eid, k=k, limit=limit)


def path(source: str, target: str, max_depth: int = 10) -> Optional[List[str]]:
    return store.find_path(source, target, max_depth=max_depth)


def stats():
    return store.stats()
