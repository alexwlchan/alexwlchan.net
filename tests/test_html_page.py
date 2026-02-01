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
    TodayILearned,
    read_page_from_markdown,
)


def test_read_page_from_file(src_dir: Path) -> None:
    """
    Read a file from Markdown.
    """
    src_dir.mkdir()
    md_path = src_dir / "example.md"

    md_path.write_text(
        "---\n"
        "layout: page\n"
        "title: Contact\n"
        "nav_section: contact\n"
        "---\n"
        "This is my contact page"
    )

    page = read_page_from_markdown(src_dir, md_path)

    assert page.md_path == md_path
    assert page.layout == "page"
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
        "layout: post\n"
        "title: My first post\n"
        "date: 2001-02-03 04:05:06 +00:00\n"
        "tags:\n"
        "  - writing\n"
        "  - programming\n"
        "---\n"
        "This is my first blog post"
    )

    page = read_page_from_markdown(src_dir, md_path)

    assert isinstance(page, Article)
    assert page.md_path == md_path
    assert page.layout == "post"
    assert page.title == "My first post"
    assert page.date == datetime(2001, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    assert page.tags == ["writing", "programming"]


def test_hidden_article_has_no_tags(src_dir: Path) -> None:
    """
    An article which is excluded from the sitewide index doesn't have tags.
    """
    src_dir.mkdir()
    md_path = src_dir / "hidden.md"

    md_path.write_text(
        "---\n"
        "layout: post\n"
        "title: My first post\n"
        "date: 2001-02-03 04:05:06 +00:00\n"
        "tags:\n"
        "  - writing\n"
        "  - programming\n"
        "index:\n"
        "  exclude: true\n"
        "---\n"
        "This post doesn't appear in the indexes"
    )

    page = read_page_from_markdown(src_dir, md_path)
    assert page.tags == []


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
                layout="page",
                src_dir=Path("src"),
                md_path=Path("src/contact.md"),
                title="Contact",
                content="Contact me",
            ),
            "/contact/",
        ),
        (
            Page(
                layout="page",
                src_dir=Path("src"),
                md_path=Path("src/index.md"),
                title="Homepage",
                content="This is my homepage",
            ),
            "/",
        ),
        (
            Page(
                layout="page",
                src_dir=Path("src"),
                md_path=Path("src/a-plumbers-guide-to-git/index.md"),
                title="A Plumber’s Guide to Git",
                content="This is a workshop about Git",
            ),
            "/a-plumbers-guide-to-git/",
        ),
        (
            Article(
                layout="post",
                src_dir=Path("src"),
                md_path=Path("src/2013/2013-02-13-darwin.md"),
                date=datetime(2013, 2, 13),
                title="Darwin",
                content="This is a post about Darwin",
            ),
            "/2013/darwin/",
        ),
        (
            TodayILearned(
                layout="til",
                src_dir=Path("src"),
                md_path=Path("src/_til/2013/2013-05-11-rss-podcasts-tumblr"),
                date=datetime(2013, 5, 11),
                title="RSS podcasts on Tumblr",
                content="This is a post about Tumblr",
            ),
            "/til/2013/rss-podcasts-tumblr/",
        ),
        (
            Page(
                layout="page", title="Posts tagged with ‘python’", url="/tags/python/"
            ),
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
