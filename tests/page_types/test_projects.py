"""
Tests for `mosaic.page_types.projects`.
"""

from collections import OrderedDict
from pathlib import Path

from jinja2 import Environment

from mosaic.git import GitFile, GitRepository
from mosaic.page_types import (
    BreadcrumbEntry,
    ProjectCommit,
    ProjectHomepage,
    ProjectAllCommits,
    ProjectSingleFile,
    ProjectTags,
    ProjectTree,
)


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

        p = ProjectHomepage(repo=repo, archive_url="/projects/example-123.tar.gz")

        assert p.url == "/projects/example-project/"
        assert p.breadcrumb == [BreadcrumbEntry(label="projects", href="/projects/")]
        assert p.title == "example-project"

        assert p.write(env, out_dir) == out_dir / "projects/example-project/index.html"

    def test_omits_tags_link_if_no_tags(
        self, env: Environment, repo: GitRepository, out_dir: Path
    ) -> None:
        """
        If the repo doesn't have any tags, there's no tags link on
        the project homepage.
        """
        repo.name = "example-project"

        p = ProjectHomepage(repo=repo, archive_url="/projects/example-123.tar.gz")
        out_path = p.write(env, out_dir)
        html = out_path.read_text()
        assert "<a href=/projects/example-project/tags/>Tags</a>" in html

        repo.tags = OrderedDict()

        p.clear_cache()
        out_path = p.write(env, out_dir)
        html = out_path.read_text()
        print(html)
        assert "<a href=/projects/example-project/tags/>Tags</a>" not in html


def test_log(env: Environment, repo: GitRepository, out_dir: Path) -> None:
    """
    Tests for `ProjectAllCommits`.
    """
    repo.name = "example-project"

    p = ProjectAllCommits(repo=repo)

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
