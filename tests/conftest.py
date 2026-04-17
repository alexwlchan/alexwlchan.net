"""
Shared test fixtures and helpers.
"""

from collections.abc import Callable
from pathlib import Path
import subprocess
from typing import TypeAlias

from jinja2 import Environment
import pytest

from mosaic import templates as t
from mosaic.git import GitRepository


@pytest.fixture
def src_dir(tmp_path: Path) -> Path:
    """
    Return a source directory for the site.
    """
    return tmp_path / "src"


@pytest.fixture
def out_dir(tmp_path: Path) -> Path:
    """
    Return an output directory for the site.
    """
    return tmp_path / "out"


@pytest.fixture
def env(src_dir: Path, out_dir: Path) -> Environment:
    """
    Create a basic instance of the Jinja2 environment.
    """
    ev = t.get_jinja_environment(src_dir, out_dir)
    ev.globals.update({"css_url": "/test/style.test.css"})
    return ev


@pytest.fixture
def repo_root(tmp_path: Path) -> Path:
    """
    Return the root of a temporary Git repository, which will only exist
    for the duration of a single test.
    """
    p = tmp_path / "repo"
    p.mkdir()
    return p


GitFn: TypeAlias = Callable[..., None]


@pytest.fixture
def git(repo_root: Path) -> GitFn:
    """
    Return a wrapper function for running Git commands in the temp repo.
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
def repo(git: GitFn, repo_root: Path) -> GitRepository:
    """
    Create a basic Git history and repository.
    """
    # History:
    #
    #       "hello"
    #          ^
    #          |
    #    "hello world"
    #          ^
    #          |
    #   "bonjour monde"
    #
    (repo_root / "greeting.en.txt").write_text("hello")
    git("add", "greeting.en.txt")
    git("commit", "-m", "initial commit", "--date", "Sat 2 Feb 2002 02:02:02 GMT")
    git("tag", "v1")

    (repo_root / "greeting.en.txt").write_text("hello world")
    git("add", "greeting.en.txt")
    git("commit", "-m", "add 'world'", "--date", "Mon 3 Mar 2003 03:03:03 GMT")
    git("tag", "v2")

    (repo_root / "greeting.fr.txt").write_text("bonjour monde")
    git("add", "greeting.fr.txt")
    git("commit", "-m", "convert to French", "--date", "Sun 4 Apr 2004 04:04:04 GMT")
    git("tag", "v10")

    (repo_root / "README.md").write_text("this is an example repo")
    git("add", "README.md")
    git("commit", "-m", "add a README file", "--date", "Thu 5 May 2005 05:05:05 GMT")

    return GitRepository(
        name="example", description="example repo", repo_root=repo_root
    )
