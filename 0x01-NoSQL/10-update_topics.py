#!/usr/bin/env python3
"""
Implement function that changes all topics of
a school document based on the name
"""

def update_topics(mongo_collection, name, topics):
    """
    Change all topics of a school document based on the name
    """
    mongo_collection.update_one(
        {'name': name},
        {'topics': topics}
    )
