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
            "cache_entries("
            "  namespace, key, value, date_saved, "
            "  UNIQUE (namespace, key) ON CONFLICT REPLACE"
            ")"
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
        self.conn.execute(
            "INSERT OR REPLACE INTO cache_entries VALUES (?,?,?,?)",
            (namespace, key, value, datetime.now(tz=timezone.utc).isoformat()),
        )
        self.conn.commit()

    def contains(self, namespace: str, key: str) -> bool:
        """
        Return True if a key is in the cache, or False if not.
        """
        res = self.conn.execute(
            "SELECT EXISTS(SELECT 1 FROM cache_entries WHERE namespace=? AND key=?)",
            (namespace, key),
        )

        return bool(res.fetchone() == (1,))

    def get(self, namespace: str, key: str) -> str | None:
        """
        Retrieve a key from the cache, or return None if it's not present.
        """
        res = self.conn.execute(
            "SELECT value FROM cache_entries WHERE namespace=? AND key=?",
            (namespace, key),
        )

        try:
            (value,) = res.fetchone()
            return cast(str, value)
        except TypeError:
            return None

    def purge(self, namespace: str, prefix: str = "") -> None:
        """
        Purge any keys matching this prefix from the cache.
        """
        if prefix:
            self.conn.execute(
                "DELETE FROM cache_entries WHERE namespace=? AND key LIKE ?",
                (namespace, f"{prefix}%"),
            )
        else:
            self.conn.execute(
                "DELETE FROM cache_entries WHERE namespace=?",
                (namespace,),
            )


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
contains = _cache.contains
get = _cache.get
purge = _cache.purge
