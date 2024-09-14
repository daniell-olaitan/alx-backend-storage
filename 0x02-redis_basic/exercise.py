#!/usr/bin/env python3
"""
Create a base class for cashing
"""
import uuid
import redis
import typing as t
from functools import wraps


def replay(fn: t.Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    cache = fn.__self__._redis
    in_key = f"{fn.__qualname__}:inputs"
    inputs = cache.lrange(in_key, 0, -1)
    outputs = cache.lrange(f"{fn.__qualname__}:outputs", 0, -1)

    print(f"{fn.__qualname__} was called {cache.llen(in_key)} times:")
    for in_val, out_val in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            fn.__qualname__, in_val.decode('UTF-8'), out_val.decode('UTF-8')
        ))


def count_calls(method: t.Callable) -> t.Callable:
    """
    Decorate a method to count the number of times  the method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap a given method
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: t.Callable) -> t.Callable:
    """
    Record the input and output history of a particular method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap a given method
        """
        in_key = f"{method.__qualname__}:inputs"
        out_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(out_key, str(output))

        return output

    return wrapper


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

    @call_history
    @count_calls
    def store(self, data: t.Union[str, bytes, int, float]) -> str:
        """
        Store a given data to the cache
        """
        uid = str(uuid.uuid4())
        self._redis.set(uid, data)

        return uid

    def get(
            self,
            key: str,
            fn: t.Optional[t.Callable] = None
    ) -> t.Union[str, bytes, int, float]:
        """
        Get a value from the cache
        """
        data = self._redis.get(key)
        if data:
            if fn:
                return fn(data)

            return data

        return None

    def get_str(self, key: str) -> str:
        """
        Get a string value from the cache
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Get an int value from the cache
        """
        return self.get(key, fn=int)


cache = Cache()

cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)
