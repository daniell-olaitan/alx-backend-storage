#!/usr/bin/env python3
"""
Create a base class for cashing
"""
from __future__ import annotations
import uuid
import redis
import typing as t


class Cache:
    """
    Base class for cashing
    """
    BaseType = t.Union[str, bytes, int, float]
    def __init__(self):
        """
        Initializes the cache class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Cache.BaseType) -> str:
        """
        Store a given data to the cache
        """
        uid = str(uuid.uuid4())
        self._redis.set(uid, data)

        return uid
