"""
Tests for `mosaic.cache`.
"""

from collections.abc import Iterator

import pytest

from mosaic import cache as c
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
    assert not cache.contains(namespace="fibonacci", key="10")

    cache.set(namespace="fibonacci", key="10", value="55")

    assert cache.get(namespace="fibonacci", key="10") == "55"
    assert cache.contains(namespace="fibonacci", key="10")
    assert cache.get(namespace="fibonacci", key="11") is None
    assert not cache.contains(namespace="fibonacci", key="11")


def test_register() -> None:
    """
    Test the register wrapper.
    """

    @c.register
    def upper(s: str) -> str:
        return s.upper()

    @c.register
    def lower(s: str) -> str:
        return s.lower()

    assert c.get("upper", "aBcDe") is None
    assert c.get("lower", "aBcDe") is None

    assert upper("aBcDe") == "ABCDE"

    assert c.get("upper", "aBcDe") == "ABCDE"
    assert c.get("lower", "aBcDe") is None

    assert upper("aBcDe") == "ABCDE"
