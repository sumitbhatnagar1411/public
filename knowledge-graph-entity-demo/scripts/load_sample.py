"""
Load sample entities and relationships for demo.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from graph.store import store
from graph.model import EntityType, RelationType, entity_id

def main():
    # Customers
    store.add_entity(entity_id(EntityType.CUSTOMER, "C1"), "customer", {"name": "Alice", "segment": "premium"})
    store.add_entity(entity_id(EntityType.CUSTOMER, "C2"), "customer", {"name": "Bob", "segment": "standard"})
    store.add_entity(entity_id(EntityType.CUSTOMER, "C3"), "customer", {"name": "Carol", "segment": "premium"})

    # Accounts
    for i in range(1, 5):
        store.add_entity(entity_id(EntityType.ACCOUNT, f"A{i}"), "account", {"balance": 1000 * i})

    # Products
    store.add_entity(entity_id(EntityType.PRODUCT, "P1"), "product", {"name": "Savings", "category": "deposit"})
    store.add_entity(entity_id(EntityType.PRODUCT, "P2"), "product", {"name": "Checking", "category": "deposit"})

    # Relationships
    store.add_relation(entity_id(EntityType.CUSTOMER, "C1"), entity_id(EntityType.ACCOUNT, "A1"), "owns")
    store.add_relation(entity_id(EntityType.CUSTOMER, "C1"), entity_id(EntityType.ACCOUNT, "A2"), "owns")
    store.add_relation(entity_id(EntityType.CUSTOMER, "C2"), entity_id(EntityType.ACCOUNT, "A3"), "owns")
    store.add_relation(entity_id(EntityType.CUSTOMER, "C3"), entity_id(EntityType.ACCOUNT, "A4"), "owns")
    store.add_relation(entity_id(EntityType.ACCOUNT, "A1"), entity_id(EntityType.PRODUCT, "P1"), "holds")
    store.add_relation(entity_id(EntityType.ACCOUNT, "A2"), entity_id(EntityType.PRODUCT, "P2"), "holds")
    store.add_relation(entity_id(EntityType.CUSTOMER, "C3"), entity_id(EntityType.CUSTOMER, "C1"), "referred_by")

    print("Sample graph loaded. Nodes:", store._g.number_of_nodes(), "Edges:", store._g.number_of_edges())
    print("Run: uvicorn app:app --reload")

if __name__ == "__main__":
    main()
