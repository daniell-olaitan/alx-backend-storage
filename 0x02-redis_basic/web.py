#!/usr/bin/env python3
"""
Implement function to obtain the HMTL content of a page
"""
import redis
import requests
import typing as t
from functools import wraps

cache = redis.Redis()


def cache_page(fn: t.Callable) -> t.Callable:
    """
    Decorate a url fetcher function to cache the fetched page
    """
    @wraps(fn)
    def wrapper(
        url: str,
        *args: t.Tuple[t.Any, ...],
        **Kwargs: t.Dict[str, t.Any]
    ) -> str:
        """
        Wrapper function to cache the fetched page
        """
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        cache.incr(count_key)
        page_content = cache.get(cache_key)
        if page_content:
            return page_content

        page_content = fn(url)
        cache.setex(cache_key, 10, page_content)

        return page_content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a given page
    """
    response = requests.get(url)

    return response.text
