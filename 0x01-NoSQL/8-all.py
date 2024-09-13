#!/usr/bin/env python3
"""
Implement a function that lists all documents in a collection
"""
from pymongo.collection import Collection
import typing as t

def list_all(
        mongo_collection: Collection
    ) -> t.Optional[t.List[t.Dict[str, t.Any]]]:
    """
    List all documents in a collection
    """
    return list(mongo_collection.find({}))
