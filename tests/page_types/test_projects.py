"""
Tests for `mosaic.page_types.projects`.
"""

from collections.abc import Callable
from pathlib import Path
from typing import TypeAlias

from jinja2 import Environment

from mosaic.git import GitFile, GitRepository
from mosaic.models import BreadcrumbEntry
from mosaic.page_types import (
    ProjectCommit,
    ProjectHomepage,
    ProjectLog,
    ProjectSingleFile,
    ProjectTree,
)

GitFn: TypeAlias = Callable[..., None]


class TestProjectHomepage:
    """
    Tests for `ProjectHomepage`.
    """

    def test_homepage(
        self, env: Environment, repo: GitRepository, out_dir: Path
    ) -> None:
        """
        Test the basic behaviour of a homepage.
        """
        repo.name = "example-project"

        p = ProjectHomepage(
            repo=repo, download_url="/projects/example-123.tar.gz", download_size=456
        )

        assert p.url == "/projects/example-project/"
        assert p.breadcrumb == [BreadcrumbEntry(label="projects", href="/projects/")]
        assert p.title == "example-project"

        assert p.write(env, out_dir) == out_dir / "projects/example-project/index.html"

    def test_has_clone_url(
        self, env: Environment, repo: GitRepository, out_dir: Path
    ) -> None:
        """
        The page has the correct clone instructions.
        """
        repo.name = "example-project"

        p = ProjectHomepage(
            repo=repo, download_url="/projects/example-123.tar.gz", download_size=456
        )
        html = p.render_full_html(env)

        assert "git clone git://alexwlchan.net/projects/example-project.git" in html


class TestProjectLog:
    """
    Tests for `ProjectLog`.
    """

    def test_log(self, env: Environment, repo: GitRepository, out_dir: Path) -> None:
        """
        Test a basic rendering of the page.
        """
        repo.name = "example-project"

        p = ProjectLog(repo=repo)

        assert p.url == "/projects/example-project/commits/"
        assert p.breadcrumb == [
            BreadcrumbEntry(label="projects", href="/projects/"),
            BreadcrumbEntry(label="example-project", href="/projects/example-project/"),
        ]

        assert (
            p.write(env, out_dir)
            == out_dir / "projects/example-project/commits/index.html"
        )

    def test_commit_summary_escaped(
        self, env: Environment, repo_root: Path, git: GitFn
    ) -> None:
        """
        Test that angle brackets are escaped in the commit message.
        """
        (repo_root / "chives-video.js").write_text("Hello world")
        git("add", "chives-video.js")
        git("commit", "-m", "add the file <chives-video> to the repo")

        repo = GitRepository(name="example", description="example", repo_root=repo_root)

        p = ProjectLog(repo=repo)

        html = p.render_full_html(env)
        assert "add the file &lt;chives-video> to the repo" in html


class TestProjectCommit:
    """
    Tests for `ProjectCommit`.
    """

    def test_commit(self, env: Environment, repo: GitRepository, out_dir: Path) -> None:
        """
        Basic tests for the page type.
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

    def test_commit_summary_escaped(
        self, env: Environment, repo_root: Path, git: GitFn
    ) -> None:
        """
        Test that angle brackets are escaped in the commit summary.
        """
        (repo_root / "chives-video.js").write_text("Hello world")
        git("add", "chives-video.js")
        git("commit", "-m", "add the <chives-video> component")

        repo = GitRepository(name="example", description="example", repo_root=repo_root)

        commit = list(repo.commits.values())[0]

        p = ProjectCommit(repo=repo, commit=commit)

        html = p.render_full_html(env)
        assert "<h2>add the &lt;chives-video> component</h2>" in html

    def test_commit_message_escaped(
        self, env: Environment, repo_root: Path, git: GitFn
    ) -> None:
        """
        Test that angle brackets are escaped in the commit message.
        """
        (repo_root / "greeting.txt").write_text("Hello world")
        git("add", "greeting.txt")
        git(
            "commit",
            "-m",
            "add greeting.txt\n\nSigned-off-by: Alex Chan <alex@alexwlchan.net>",
        )

        repo = GitRepository(name="example", description="example", repo_root=repo_root)

        commit = list(repo.commits.values())[0]

        p = ProjectCommit(repo=repo, commit=commit)

        html = p.render_full_html(env)
        assert "Signed-off-by: Alex Chan &lt;alex@alexwlchan.net>" in html


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


class TestSingleFile:
    """
    Tests for `ProjectSingleFile`.
    """

    def test_single_file(
        self, env: Environment, repo: GitRepository, out_dir: Path
    ) -> None:
        """
        Test the basic properties of a ProjectSingleFile.
        """
        repo.name = "example-project"

        p = ProjectSingleFile(
            repo=repo,
            file=GitFile(
                path=Path("README.md"), blob_id="123", size=17, is_binary=False
            ),
            file_contents="This is my README",
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

    def test_markdown_file(
        self, env: Environment, repo: GitRepository, out_dir: Path
    ) -> None:
        """
        Test a Markdown file which includes backticks.
        """
        file_contents = (
            "This is some code\n"
            "\n"
            "```\n"
            "def greet():\n"
            "    print('hello world')\n"
            "```\n"
            "\n"
            "This is some text after the code."
        )

        p = ProjectSingleFile(
            repo=repo,
            file=GitFile(
                path=Path("README.md"),
                blob_id="123",
                size=len(file_contents),
                is_binary=False,
            ),
            file_contents=file_contents,
        )

        html = p.render_full_html(env)

        # Check there's only one closing </pre> tag on the page, and that
        # the code in the block is formatted properly.
        assert html.count("</pre>") == 1
        assert "<p>def greet():" not in html

    def test_empty_file(
        self, env: Environment, repo: GitRepository, out_dir: Path
    ) -> None:
        """
        Test an empty file doesn't render a "<pre>" block.
        """
        p = ProjectSingleFile(
            repo=repo,
            file=GitFile(
                path=Path("README.md"), blob_id="123", size=0, is_binary=False
            ),
            file_contents="",
        )

        html = p.render_full_html(env)

        assert "<pre>" not in html
        assert "<p>(File is empty)</p>" in html
