"""
Tests for `mosaic.html_page`.
"""

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mosaic.page_types import (
    Article,
    BaseHtmlPage,
    Page,
    read_page_from_markdown,
)


def test_read_page_from_file(src_dir: Path) -> None:
    """
    Read a file from Markdown.
    """
    src_dir.mkdir()
    md_path = src_dir / "example.md"

    md_path.write_text(
        "---\nlayout: page\ntitle: Contact\n---\nThis is my contact page"
    )

    page = read_page_from_markdown(src_dir, md_path)

    assert page.md_path == md_path
    assert page.title == "Contact"
    assert page.content == "This is my contact page"


def test_read_article(src_dir: Path) -> None:
    """
    Read an article from Markdown.
    """
    src_dir.mkdir()
    md_path = src_dir / "example.md"

    md_path.write_text(
        "---\n"
        "layout: article\n"
        "title: My first post\n"
        "date: 2001-02-03 04:05:06 +00:00\n"
        "---\n"
        "This is my first blog post"
    )

    page = read_page_from_markdown(src_dir, md_path)

    assert isinstance(page, Article)
    assert page.md_path == md_path
    assert page.title == "My first post"
    assert page.date == datetime(2001, 2, 3, 4, 5, 6, tzinfo=timezone.utc)


def test_read_error_includes_filename(src_dir: Path) -> None:
    """
    An error reading the Markdown file includes the filename.
    """
    md_path = src_dir / "example.md"

    with pytest.raises(RuntimeError, match=str(md_path)):
        read_page_from_markdown(src_dir, md_path)


@pytest.mark.parametrize(
    "page, url",
    [
        (
            Page(
                src_dir=Path("src"),
                md_path=Path("src/contact.md"),
                title="Contact",
                content="Contact me",
            ),
            "/contact/",
        ),
        (
            Page(
                src_dir=Path("src"),
                md_path=Path("src/index.md"),
                title="Homepage",
                content="This is my homepage",
            ),
            "/",
        ),
        (
            Page(
                src_dir=Path("src"),
                md_path=Path("src/a-plumbers-guide-to-git/index.md"),
                title="A Plumber’s Guide to Git",
                content="This is a workshop about Git",
            ),
            "/a-plumbers-guide-to-git/",
        ),
        (
            Article(
                src_dir=Path("src"),
                md_path=Path("src/2013/2013-02-13-darwin.md"),
                date=datetime(2013, 2, 13),
                title="Darwin",
                content="This is a post about Darwin",
            ),
            "/2013/darwin/",
        ),
        (
            Page(title="Posts tagged with ‘python’", url="/tags/python/"),
            "/tags/python/",
        ),
    ],
)
def test_url(page: BaseHtmlPage, url: str) -> None:
    """
    Check the URL for every page.
    """
    assert page.url == url


def test_out_path() -> None:
    """
    Check the output path for a page.
    """
    page = Page(
        layout="page",
        src_dir=Path("src"),
        md_path=Path("src/contact.md"),
        title="Contact",
        content="Contact me",
    )
    assert page.out_path(out_dir=Path("_out")) == Path("_out/contact/index.html")
