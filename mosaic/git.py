"""
Read-only operations on Git repos. This is used in my code browser to get
information about bare repositories.
"""

import codecs
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel
import pygit2
from pygit2.enums import SortMode


__all__ = ["Commit", "Repository"]


def as_hex(oid: pygit2.Oid) -> str:
    """
    Converts a Git object ID to a human-readable hex string.
    """
    return codecs.encode(oid.raw, "hex").decode("ascii")


class Commit(BaseModel):
    """
    Represents a single Git commit.
    """

    id: str
    message: str
    author: str
    date: datetime
    parent_ids: list[str]


class Repository(BaseModel):
    """
    Wrapper around a Git repository.
    """

    root: Path

    @property
    def underlying(self) -> pygit2.Repository:
        """
        Returns a `pygit2.Repository` instance for this repo.
        """
        return pygit2.Repository(self.root)

    def history(self) -> list[Commit]:
        """
        Returns a list of commits starting from HEAD, newest first.

        Note: this method will throw an error if caused on an empty repo
        which doesn't have any commits.
        """
        walker = self.underlying.walk(self.underlying.head.target, SortMode.TOPOLOGICAL)

        return [
            Commit(
                id=as_hex(commit.id),
                message=commit.message,
                author=f"{commit.author.name} <{commit.author.email}>",
                date=datetime.fromtimestamp(commit.author.time, tz=timezone.utc),
                parent_ids=[as_hex(pid) for pid in commit.parent_ids],
            )
            for commit in walker
        ]
