#!/usr/bin/env python3
"""
Create a base class for cashing
"""
import uuid
import redis
import typing as t


class Cache:
    """
    Base class for cashing
    """
    def __init__(self):
        """
        Initializes the cache class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: t.Union[str, bytes, int, float]) -> str:
        """
        Store a given data to the cache
        """
        uid = str(uuid.uuid4())
        self._redis.set(uid, data)

        return uid
