"""
Tests for `mosaic.html_page`.
"""

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mosaic.page_types import (
    Article,
    BaseHtmlPage,
    BookReview,
    IndexInfo,
    Note,
    Page,
    TopicPage,
    read_page_from_markdown,
    read_markdown_files,
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


@pytest.mark.parametrize("topics_yml", ["topic: Python\n", "topics:\n- Python\n"])
def test_single_topic_can_be_str_or_list(src_dir: Path, topics_yml: str) -> None:
    """
    If there's only one topic, it can be expressed as a `topic` string
    or a one-item list `topics`.
    """
    src_dir.mkdir()
    md_path = src_dir / "example.md"

    md_path.write_text(
        "---\nlayout: page\n"
        "title: Example\n" + topics_yml + "---\n" + "This is an example page"
    )

    page = read_page_from_markdown(src_dir, md_path)
    assert page.topics == ["Python"]


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


def test_read_note(src_dir: Path) -> None:
    """
    Read a note from Markdown.
    """
    src_dir.mkdir()
    md_path = src_dir / "note.md"

    md_path.write_text(
        "---\n"
        "layout: note\n"
        "title: My first post\n"
        "date: 2001-02-03 04:05:06 +00:00\n"
        "---\n"
        "This is my first note"
    )

    page = read_page_from_markdown(src_dir, md_path)

    assert isinstance(page, Note)
    assert page.md_path == md_path
    assert page.title == "My first post"
    assert page.date == datetime(2001, 2, 3, 4, 5, 6, tzinfo=timezone.utc)


def test_read_book_review(src_dir: Path) -> None:
    """
    Read a book review from Markdown.
    """
    src_dir.mkdir()
    md_path = src_dir / "review.md"

    md_path.write_text(
        "---\n"
        "layout: book_review\n"
        "date: 2001-02-03 04:05:06 +00:00\n"
        "book:\n"
        "  title: Example Book\n"
        "  contributors:\n"
        "    - name: Jane Smith\n"
        "  genres:\n"
        "    - fiction\n"
        "  publication_year: 2000\n"
        "review:\n"
        "  date_read: 2001-02-03\n"
        "  format: paperback\n"
        "  rating: 4\n"
        "---\n"
        "Some thoughts on the book"
    )

    page = read_page_from_markdown(src_dir, md_path)

    assert isinstance(page, BookReview)
    assert page.md_path == md_path
    assert page.book.title == "Example Book"


def test_read_topic(src_dir: Path) -> None:
    """
    Read a topic page from Markdown.
    """
    src_dir.mkdir()
    md_path = src_dir / "topic.md"

    md_path.write_text(
        "---\nlayout: topic\ntitle: Python\n---\nIntro to the Python topic"
    )

    page = read_page_from_markdown(src_dir, md_path)

    assert isinstance(page, TopicPage)
    assert page.md_path == md_path
    assert page.title == "Python"


def test_read_unrecognised_layout(src_dir: Path) -> None:
    """
    Read an unrecognised layout from Markdown.
    """
    src_dir.mkdir()
    md_path = src_dir / "unrecognised.md"

    md_path.write_text(
        "---\n"
        "layout: unrecognised\n"
        "title: What is this page?\n"
        "---\n"
        "This page has an unecognised layout"
    )

    with pytest.raises(ValueError, match="unrecognised layout"):
        read_page_from_markdown(src_dir, md_path)


def test_read_multiple_markdown_files(src_dir: Path) -> None:
    """
    Read multiple Markdown files.
    """
    path1 = src_dir / "dir1/example1.md"
    path2 = src_dir / "example2.md"
    path3 = src_dir / "dir3/example3.md"

    for p in [path1, path2, path3]:
        p.parent.mkdir(exist_ok=True, parents=True)
        p.write_text(
            "---\n"
            "layout: article\n"
            "title: This is an article\n"
            "date: 2001-02-03 04:05:06 +00:00\n"
            "topic: Python\n"
            "---\n"
            "This is an example article"
        )

    articles = read_markdown_files(src_dir)

    assert len(articles) == 3
    assert all(isinstance(a, Article) for a in articles)
    assert {a.md_path for a in articles} == {path1, path2, path3}


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


@pytest.mark.parametrize("is_featured", [True, False])
def test_is_featured(is_featured: bool) -> None:
    """
    Test the is_featured convenience attribute.
    """
    p = Page(index=IndexInfo(feature=is_featured))
    assert p.is_featured == is_featured


@pytest.mark.parametrize("is_excluded", [True, False])
def test_is_excluded(is_excluded: bool) -> None:
    """
    Test the is_excluded convenience attribute.
    """
    p = Page(index=IndexInfo(exclude=is_excluded))
    assert p.is_excluded == is_excluded
