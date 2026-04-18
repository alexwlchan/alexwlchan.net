"""
SQLite-based caching for common operations, to speed up the site build.
"""

from collections.abc import Callable
from datetime import datetime, timezone
import functools
from pathlib import Path
import sqlite3
import sys
from typing import cast, Literal

from .git import git_root


__all__ = ["SQLiteCache", "register"]


class SQLiteCache:
    """
    A basic SQLite-backed cache which supports reading and writing values.
    """

    conn: sqlite3.Connection

    def __init__(self, database: Path | Literal[":memory:"]):
        """
        Create the initial SQLite connection.
        """
        self.conn = sqlite3.connect(database)

        cursor = self.conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS "
            "cache_entries(namespace, key, value, date_saved)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS cache_entries_idx "
            "ON cache_entries(namespace, key)"
        )
        self.conn.commit()

    def close(self) -> None:
        """
        Close the SQLite connection.
        """
        self.conn.close()

    def set(self, namespace: str, key: str, value: str | bool = "true") -> None:
        """
        Save a key in the cache.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO cache_entries VALUES (?,?,?,?)",
            (namespace, key, value, datetime.now(tz=timezone.utc).isoformat()),
        )
        self.conn.commit()

    def get(self, namespace: str, key: str) -> str | None:
        """
        Retrieve a key from the cache, or return None if it's not present.
        """
        cursor = self.conn.cursor()
        res = cursor.execute(
            "SELECT value FROM cache_entries WHERE namespace=? AND key=?",
            (namespace, key),
        )

        try:
            (value,) = res.fetchone()
            return cast(str, value)
        except TypeError:
            return None


def register(f: Callable[[str], str]) -> Callable[[str], str]:
    """
    Wrap a function so its return values are stored in the default cache.
    """

    @functools.wraps(f)
    def wrapper(key: str) -> str:
        namespace = f.__name__

        if value := _cache.get(namespace, key):
            return value

        value = f(key)
        _cache.set(namespace, key, value)
        return value

    return wrapper


if "pytest" in sys.modules:
    _cache = SQLiteCache(database=":memory:")
else:  # pragma: no cover
    _cache = SQLiteCache(database=git_root() / ".mosaic_cache.db")

set = _cache.set
get = _cache.get
