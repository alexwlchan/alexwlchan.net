"""
Functions for interacting with Git.
"""

from pathlib import Path

import pygit2


__all__ = ["git_root"]


def git_root() -> Path:
    """
    Return the root of the current Git checkout.

    This expects to be run in a non-bare checkout, and returns the root
    of the checkout -- so `.git` is a subdirectory.
    """
    p = pygit2.discover_repository(Path.cwd())
    assert p is not None
    git_dir = Path(p)
    assert git_dir.name == ".git"
    return git_dir.parent
