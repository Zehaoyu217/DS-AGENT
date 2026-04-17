from functools import lru_cache


@lru_cache
def cached_value():
    return 42


def caller():
    return cached_value()
