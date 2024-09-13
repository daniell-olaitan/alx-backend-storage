#!/usr/bin/env python3
"""
Implement function that returns the list of school having a specific topic
"""

def schools_by_topic(mongo_collection, topic):
    """
    Return the list of scholl having specific topic
    """
    return list(mongo_collection.find({'topics': topic}))
