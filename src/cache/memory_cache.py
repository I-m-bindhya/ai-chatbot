import time

from src.cache.cache import Cache


class MemoryCache(Cache):

    def __init__(self):
        self._cache = {}

    def get(self, key):

        item = self._cache.get(key)

        if not item:
            return None

        value, expires_at = item

        if expires_at and time.time() > expires_at:
            del self._cache[key]
            return None

        return value

    def set(self, key, value, ttl=None):

        expires_at = None

        if ttl:
            expires_at = time.time() + ttl

        self._cache[key] = (
            value,
            expires_at
        )

    def delete(self, key):

        self._cache.pop(key, None)