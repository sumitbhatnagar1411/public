"""
Entity and relationship types for the knowledge graph.
TigerGraph/Neo4j use similar concepts: vertex types, edge types, attributes.
"""
from enum import Enum
from typing import Any


class EntityType(str, Enum):
    CUSTOMER = "customer"
    ACCOUNT = "account"
    PRODUCT = "product"
    TRANSACTION = "transaction"


class RelationType(str, Enum):
    OWNS = "owns"           # customer -> account
    HOLDS = "holds"         # account -> product
    TRANSACTED = "transacted"  # transaction links account/product/customer
    REFERRED_BY = "referred_by"  # customer -> customer
    BELONGS_TO = "belongs_to"  # transaction -> account


def entity_id(etype: EntityType, key: str) -> str:
    return f"{etype.value}:{key}"


def parse_entity_id(eid: str) -> tuple[str, str]:
    if ":" in eid:
        t, k = eid.split(":", 1)
        return t, k
    return "unknown", eid
