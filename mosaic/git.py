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


__all__ = ["ChangedFile", "Commit", "CommitNotFoundError", "Repository"]


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


class CommitNotFoundError(FileNotFoundError):
    """
    Thrown when you try to look up a commit that doesn't exist.
    """


class ChangedTextFileHunk(BaseModel):
    """
    Represents a single "hunk" of change in a commit.
    """

    header: str
    lines: list[str]

    @classmethod
    def from_hunk(self, diff_hunk: pygit2.DiffHunk) -> "ChangedTextFileHunk":
        """
        Create a new instance of ChangedFile from a `pygit2.DiffHunk`.
        """
        return ChangedTextFileHunk(
            header=diff_hunk.header.strip(),
            lines=[ln.origin + ln.content for ln in diff_hunk.lines],
        )


class ChangedBinaryFile(BaseModel):
    """
    Represents a changed binary file in a Git commit.
    """

    # The path to the file, relative to the repo root
    old_path: Path | None
    new_path: Path | None

    # The size of the file before/after the diff
    old_size: int
    new_size: int


class ChangedTextFile(BaseModel):
    """
    Represents a changed text file in a Git commit.
    """

    # The path to the file, relative to the repo root
    old_path: Path | None
    new_path: Path | None

    # The size of the file before/after the diff
    old_size: int
    new_size: int

    # A list of changed hunks
    hunks: list[ChangedTextFileHunk]

    # Get the line counts for the patch
    lines_added: int
    lines_deleted: int


ChangedFile = ChangedBinaryFile | ChangedTextFile


def changed_file_from_patch(patch: pygit2.Patch) -> ChangedFile:
    """
    Create a new instance of ChangedFile from a `pygit2.Patch`.
    """
    old_size = patch.delta.old_file.size
    old_path: Path | None = None
    if old_size > 0:
        old_path = Path(patch.delta.old_file.path)

    new_size = patch.delta.new_file.size
    new_path: Path | None = None
    if new_size > 0:
        new_path = Path(patch.delta.new_file.path)

    _, lines_added, lines_deleted = patch.line_stats

    if patch.delta.is_binary:
        return ChangedBinaryFile(
            old_path=old_path,
            new_path=new_path,
            old_size=old_size,
            new_size=new_size,
        )
    else:
        return ChangedTextFile(
            old_path=old_path,
            new_path=new_path,
            old_size=old_size,
            new_size=new_size,
            lines_added=lines_added,
            lines_deleted=lines_deleted,
            hunks=[ChangedTextFileHunk.from_hunk(hk) for hk in patch.hunks],
        )


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

    def changed_files(self, commit_id: str) -> list[ChangedFile]:
        """
        Return a list of changed files for a given commit.
        """
        obj = self.underlying.get(commit_id)
        if not isinstance(obj, pygit2.Commit):
            raise CommitNotFoundError(commit_id)

        # This is the commit ID of an empty tree, which is useful when
        # we're looking at the initial commit.
        empty_tree = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

        if not obj.parents:
            old, new = empty_tree, commit_id
        else:
            old, new = f"{commit_id}^", commit_id

        diff = self.underlying.diff(old, new)
        diff.find_similar()
        return [changed_file_from_patch(d) for d in diff]
