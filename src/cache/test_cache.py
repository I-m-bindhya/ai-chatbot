import time

from src.cache.memory_cache import MemoryCache
from src.cache.cache_key import make_cache_key


def test_cache():

    cache = MemoryCache()

    key = make_cache_key(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": "What is Python?"
            }
        ]
    )

    print("KEY:", key)

    # 1. Cache miss
    result = cache.get(key)

    print("Initial:", result)

    assert result is None

    # 2. Store value
    cache.set(
        key,
        "Python is a programming language.",
        ttl=5
    )

    # 3. Cache hit
    result = cache.get(key)

    print("After set:", result)

    assert result == "Python is a programming language."

    # 4. Wait for expiration
    time.sleep(6)

    result = cache.get(key)

    print("After TTL:", result)

    assert result is None

    print("Cache test passed!")