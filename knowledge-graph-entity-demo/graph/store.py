"""
In-memory graph store using NetworkX. Replace with TigerGraph/Neo4j for production.
"""
from typing import Any, List, Optional

import networkx as nx

from .model import EntityType, RelationType, entity_id


class GraphStore:
    def __init__(self):
        self._g = nx.MultiDiGraph()

    def add_entity(self, eid: str, entity_type: str, attributes: Optional[dict] = None) -> None:
        self._g.add_node(eid, type=entity_type, **(attributes or {}))

    def add_relation(self, source: str, target: str, relation_type: str, attributes: Optional[dict] = None) -> None:
        self._g.add_edge(source, target, type=relation_type, **(attributes or {}))

    def get_entity(self, eid: str) -> Optional[dict]:
        if not self._g.has_node(eid):
            return None
        data = dict(self._g.nodes[eid])
        data["id"] = eid
        return data

    def get_neighbors(
        self,
        eid: str,
        direction: str = "out",
        relation_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[dict]:
        if not self._g.has_node(eid):
            return []
        neighbors = []
        if direction == "out":
            edges = self._g.out_edges(eid, data=True)
        else:
            edges = self._g.in_edges(eid, data=True)
        for u, v, d in edges:
            if relation_type and d.get("type") != relation_type:
                continue
            node_data = dict(self._g.nodes[v])
            node_data["id"] = v
            node_data["_relation"] = d.get("type")
            neighbors.append(node_data)
            if len(neighbors) >= limit:
                break
        return neighbors

    def get_k_hop(self, eid: str, k: int = 2, limit: int = 100) -> List[dict]:
        """Return nodes within k hops (BFS)."""
        if not self._g.has_node(eid):
            return []
        seen = {eid}
        result = []
        frontier = [eid]
        for _ in range(k):
            next_frontier = []
            for n in frontier:
                for _, v in self._g.out_edges(n):
                    if v not in seen:
                        seen.add(v)
                        next_frontier.append(v)
                        result.append(dict(self._g.nodes[v], id=v))
                    if len(result) >= limit:
                        return result
                for u, _ in self._g.in_edges(n):
                    if u not in seen:
                        seen.add(u)
                        next_frontier.append(u)
                        result.append(dict(self._g.nodes[u], id=u))
                    if len(result) >= limit:
                        return result
            frontier = next_frontier
        return result

    def find_path(self, source: str, target: str, max_depth: int = 10) -> Optional[List[str]]:
        """Shortest path (list of node ids)."""
        if not self._g.has_node(source) or not self._g.has_node(target):
            return None
        try:
            path = nx.shortest_path(self._g.to_undirected(), source, target)
            return path[: max_depth + 1]
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def stats(self) -> dict:
        return {
            "nodes": self._g.number_of_nodes(),
            "edges": self._g.number_of_edges(),
        }


# Global store for demo; use DI in production
store = GraphStore()
