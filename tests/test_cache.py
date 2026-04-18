"""
Tests for `mosaic.cache`.
"""

from collections.abc import Iterator

import pytest

from mosaic.cache import SQLiteCache


@pytest.fixture
def cache() -> Iterator[SQLiteCache]:
    """
    Create an empty SQLiteCache which only exists for the duration
    of this test.
    """
    c = SQLiteCache(":memory:")
    yield c
    c.close()


def test_basic_cache(cache: SQLiteCache) -> None:
    """
    Basic cache usage for SQLiteCache.
    """
    assert cache.get(namespace="fibonacci", key="10") is None

    cache.set(namespace="fibonacci", key="10", value="55")

    assert cache.get(namespace="fibonacci", key="10") == "55"
    assert cache.get(namespace="fibonacci", key="11") is None
