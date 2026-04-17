"""
Tests for `mosaic.page_types.projects`.
"""

from pathlib import Path

from jinja2 import Environment

from mosaic.git import GitRepository
from mosaic.page_types import (
    BreadcrumbEntry,
    ProjectCommit,
    ProjectHomepage,
    ProjectLog,
    ProjectSingleFile,
    ProjectTags,
    ProjectTree,
)


def test_homepage(env: Environment, repo: GitRepository, out_dir: Path) -> None:
    """
    Tests for `ProjectHomepage`.
    """
    repo.name = "example-project"

    p = ProjectHomepage(repo=repo, archive_url="/projects/example-123.tar.gz")

    assert p.url == "/projects/example-project/"
    assert p.breadcrumb == [BreadcrumbEntry(label="projects", href="/projects/")]
    assert p.title == "example-project"

    assert p.write(env, out_dir) == out_dir / "projects/example-project/index.html"


def test_log(env: Environment, repo: GitRepository, out_dir: Path) -> None:
    """
    Tests for `ProjectLog`.
    """
    repo.name = "example-project"

    p = ProjectLog(repo=repo)

    assert p.url == "/projects/example-project/commits/"
    assert p.breadcrumb == [
        BreadcrumbEntry(label="projects", href="/projects/"),
        BreadcrumbEntry(label="example-project", href="/projects/example-project/"),
    ]

    assert (
        p.write(env, out_dir) == out_dir / "projects/example-project/commits/index.html"
    )


def test_commit(env: Environment, repo: GitRepository, out_dir: Path) -> None:
    """
    Tests for `ProjectCommit`.
    """
    repo.name = "example-project"

    commit = list(repo.commits.values())[0]
    commit_id = "cb82565da2bff937855a0c53845e2dc98c58dfeb"
    assert commit.id == commit_id

    p = ProjectCommit(repo=repo, commit=commit)

    assert p.url == f"/projects/example-project/commits/{commit_id}/"
    assert p.breadcrumb == [
        BreadcrumbEntry(label="projects", href="/projects/"),
        BreadcrumbEntry(label="example-project", href="/projects/example-project/"),
        BreadcrumbEntry(label="log", href="/projects/example-project/commits/"),
    ]

    assert (
        p.write(env, out_dir)
        == out_dir / f"projects/example-project/commits/{commit_id}/index.html"
    )


def test_tags(env: Environment, repo: GitRepository, out_dir: Path) -> None:
    """
    Tests for `ProjectTags`.
    """
    repo.name = "example-project"

    p = ProjectTags(repo=repo)

    assert p.url == "/projects/example-project/tags/"
    assert p.breadcrumb == [
        BreadcrumbEntry(label="projects", href="/projects/"),
        BreadcrumbEntry(label="example-project", href="/projects/example-project/"),
    ]

    assert p.write(env, out_dir) == out_dir / "projects/example-project/tags/index.html"


def test_tree(env: Environment, repo: GitRepository, out_dir: Path) -> None:
    """
    Tests for `ProjectTree`.
    """
    repo.name = "example-project"

    p = ProjectTree(repo=repo)

    assert p.url == "/projects/example-project/files/"
    assert p.breadcrumb == [
        BreadcrumbEntry(label="projects", href="/projects/"),
        BreadcrumbEntry(label="example-project", href="/projects/example-project/"),
    ]

    assert (
        p.write(env, out_dir) == out_dir / "projects/example-project/files/index.html"
    )


def test_single_file(env: Environment, repo: GitRepository, out_dir: Path) -> None:
    """
    Tests for `ProjectSingleFile`.
    """
    repo.name = "example-project"

    p = ProjectSingleFile(
        repo=repo, file_path=Path("README.md"), file_contents="This is my README"
    )

    assert p.url == "/projects/example-project/files/README.md"
    assert p.breadcrumb == [
        BreadcrumbEntry(label="projects", href="/projects/"),
        BreadcrumbEntry(label="example-project", href="/projects/example-project/"),
        BreadcrumbEntry(label="files", href="/projects/example-project/files/"),
    ]

    assert (
        p.write(env, out_dir)
        == out_dir / "projects/example-project/files/README.md.html"
    )
