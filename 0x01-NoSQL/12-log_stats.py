#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB
"""

if __name__ == '__main__':
    from pymongo import MongoClient

    client = MongoClient()
    db = client.logs
    collection = db.nginx
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    number_of_logs = collection.count_documents({})
    number_of_each_methods = {
        method: collection.count_documents({'method': method})
        for method in methods
    }

    number_of_status_check = collection.count_documents(
        {'method': 'GET', 'path': '/status'}
    )

    print(f"{number_of_logs} logs")
    print('Methods:')
    [
        print(f"\tmethod {method}: {number_of_each_methods[method]}")
        for method in methods
    ]

    print(f"{number_of_status_check} status check")
