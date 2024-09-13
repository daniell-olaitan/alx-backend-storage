#!/usr/bin/env python3
"""
Implement function that returns all students sorted by average score
"""
import pymongo

def top_students(mongo_collection):
    """
    Return all students sorted by average score
    """
    result = mongo_collection.aggregate([
        {
            '$addFields': {
                'original_id': '$_id'
            }
        },
        {
            '$unwind': '$topics'
        },
        {
            '$group': {
                '_id': '$name',
                'averageScore': {
                    '$avg': '$topics.score'
                },
                'original_id': {
                    '$first': '$original_id'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        },
        {
            '$project': {
                'name': '$_id',
                'averageScore': 1,
                '_id': '$original_id'
            }
        }
    ])

    return list(result)
