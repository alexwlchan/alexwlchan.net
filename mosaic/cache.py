"""
SQLite-based caching for common operations, to speed up the site build.
"""

from collections.abc import Callable
from datetime import datetime, timezone
import functools
import hashlib
from pathlib import Path
import sqlite3
import sys
from typing import cast, Literal


__all__ = ["SQLiteCache", "register", "get_cache", "md5"]


class SQLiteCache:
    """
    A basic SQLite-backed cache which supports reading and writing values.
    """

    conn: sqlite3.Connection

    def __init__(self, database: Path | Literal[":memory:"]):
        """
        Create the initial SQLite connection.
        """
        if database != ":memory:":
            database.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(database)

        cursor = self.conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS "
            "cache_entries("
            "  namespace, key, value, date_saved, "
            "  PRIMARY KEY (namespace, key)"
            ")"
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
            "SELECT 1 FROM cache_entries WHERE namespace=? AND key=?",
            (namespace, key),
        )

        return res.fetchone() is not None

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

    This uses the name of the function as the cache namespace, so you
    can just annotate the function with `@cache.register`.
    """

    @functools.wraps(f)
    def wrapper(key: str) -> str:
        namespace = f.__name__  # type: ignore

        if value := _cache.get(namespace, key):
            return value

        value = f(key)
        _cache.set(namespace, key, value)
        return value

    return wrapper


@functools.cache
def md5(s: str) -> str:
    """
    Return the hex-encoded MD5 hash of a string.
    """
    return hashlib.md5(s.encode("utf8")).hexdigest()


def get_cache(database: str | Path) -> SQLiteCache:
    """
    Return a named cache instance saved to disk, which gets replaced
    by an in-memory database during tests.
    """
    if "pytest" in sys.modules or database == ":memory:":
        return SQLiteCache(database=":memory:")
    else:  # pragma: no cover
        return SQLiteCache(database=Path(database))


_cache = get_cache(".cache/mosaic.db")

set = _cache.set
contains = _cache.contains
get = _cache.get
purge = _cache.purge
