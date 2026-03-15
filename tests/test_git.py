"""
Tests for `mosaic.git`.
"""

from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
import subprocess
from typing import TypeAlias

import pytest

from mosaic.git import Commit, CommitNotFoundError, Repository


@pytest.fixture
def repo_root(tmp_path: Path) -> Path:
    """
    Returns the root of a temporary Git repository, which will only exist
    for the duration of a single test.
    """
    return tmp_path


GitFn: TypeAlias = Callable[..., None]


@pytest.fixture
def git(repo_root: Path) -> GitFn:
    """
    Returns a wrapper function for running Git commands in the temp repo.
    """

    def inner(*args: str) -> None:
        subprocess.check_call(
            ["git"] + list(args),
            cwd=repo_root,
            env={"GIT_COMMITTER_DATE": "Mon 1 Jan 2001 01:01:01 GMT"},
        )

    inner("init", ".")
    inner("config", "user.name", "E. X. Ample")
    inner("config", "user.email", "me@example.com")

    return inner


@pytest.fixture
def repo(repo_root: Path, git: GitFn) -> Repository:
    """
    Returns an instance of `Repository` rooted in the temp repo.
    """
    return Repository(root=repo_root)


def test_history(git: GitFn, repo: Repository, repo_root: Path) -> None:
    """
    Test getting the history of a repository.
    """
    # Create a basic Git history:
    #
    #       "hello"
    #          ^
    #          |
    #    "hello world"
    #          ^
    #          |
    #   "bonjour monde"
    #
    (repo_root / "greeting.txt").write_text("hello")
    git("add", "greeting.txt")
    git("commit", "-m", "initial commit", "--date", "Sat 2 Feb 2002 02:02:02 GMT")

    (repo_root / "greeting.txt").write_text("hello world")
    git("add", "greeting.txt")
    git("commit", "-m", "add 'world'", "--date", "Mon 3 Mar 2003 03:03:03 GMT")

    (repo_root / "greeting.txt").write_text("bonjour monde")
    git("add", "greeting.txt")
    git("commit", "-m", "convert to French", "--date", "Sun 4 Apr 2004 04:04:04 GMT")

    assert repo.history() == [
        Commit(
            id="839cc3b6e949250e6e05aed6609834ec2493ac74",
            message="convert to French\n",
            author="E. X. Ample <me@example.com>",
            date=datetime(2004, 4, 4, 4, 4, 4, tzinfo=timezone.utc),
            parent_ids=["5e378f64de872be9e537331697e18a88ac2c9425"],
        ),
        Commit(
            id="5e378f64de872be9e537331697e18a88ac2c9425",
            message="add 'world'\n",
            author="E. X. Ample <me@example.com>",
            date=datetime(2003, 3, 3, 3, 3, 3, tzinfo=timezone.utc),
            parent_ids=["3ec2ee0a7c71e4b72faf7213c0e2a50b9477d37d"],
        ),
        Commit(
            id="3ec2ee0a7c71e4b72faf7213c0e2a50b9477d37d",
            message="initial commit\n",
            author="E. X. Ample <me@example.com>",
            date=datetime(2002, 2, 2, 2, 2, 2, tzinfo=timezone.utc),
            parent_ids=[],
        ),
    ]


def test_changed_files_of_bad_commit(repo: Repository) -> None:
    """
    Looking up the changed files of a non-existent commit is an error.
    """
    with pytest.raises(CommitNotFoundError):
        repo.changed_files(commit_id="123456890abcdef123456890abcdef123456890a")
