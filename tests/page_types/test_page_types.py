"""
Tests for `mosaic.page_types`.
"""

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment
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
    (src_dir / "_articles/2001").mkdir(parents=True)
    md_path = src_dir / "_articles/2001/2001-02-03-example.md"

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
    (src_dir / "notes/2001").mkdir(parents=True)
    md_path = src_dir / "notes/2001/2001-02-03-note.md"

    md_path.write_text(
        "---\n"
        "layout: note\n"
        "title: My first post\n"
        "date: 2001-02-03 04:05:06 +00:00\n"
        "topic: My topic\n"
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
    (src_dir / "_articles/2001").mkdir(parents=True)
    path1 = src_dir / "_articles/2001/2001-02-03-example1.md"
    path2 = src_dir / "_articles/2001/2001-02-03-example2.md"
    path3 = src_dir / "_articles/2001/2001-02-03-example3.md"

    for p in [path1, path2, path3]:
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


PAGE_EXAMPLES = [
    {
        "page": Page(
            src_dir=Path("src"),
            md_path=Path("src/contact.md"),
            title="Contact",
            content="Contact me",
        ),
        "url": "/contact/",
        "out_path": Path("contact/index.html"),
    },
    {
        "page": Page(
            src_dir=Path("src"),
            md_path=Path("src/index.md"),
            title="Homepage",
            content="This is my homepage",
        ),
        "url": "/",
        "out_path": Path("index.html"),
    },
    {
        "page": Page(
            src_dir=Path("src"),
            md_path=Path("src/a-plumbers-guide-to-git/index.md"),
            title="A Plumber’s Guide to Git",
            content="This is a workshop about Git",
        ),
        "url": "/a-plumbers-guide-to-git/",
        "out_path": Path("a-plumbers-guide-to-git/index.html"),
    },
    {
        "page": Article(
            src_dir=Path("src"),
            md_path=Path("src/_articles/2013/2013-02-13-darwin.md"),
            date=datetime(2013, 2, 13),
            title="Darwin",
            content="This is a post about Darwin",
        ),
        "url": "/2013/darwin/",
        "out_path": Path("2013/darwin/index.html"),
    },
    {
        "page": Page(title="Posts tagged with ‘python’", url="/tags/python/"),
        "url": "/tags/python/",
        "out_path": Path("tags/python/index.html"),
    },
]


@pytest.mark.parametrize("page, url", [(p["page"], p["url"]) for p in PAGE_EXAMPLES])
def test_url(page: BaseHtmlPage, url: str) -> None:
    """
    Check the URL for every page.
    """
    assert page.url == url


@pytest.mark.parametrize(
    "page, out_path", [(p["page"], p["out_path"]) for p in PAGE_EXAMPLES]
)
def test_writes_page(
    page: BaseHtmlPage, env: Environment, out_dir: Path, out_path: Path
) -> None:
    """
    Check the correct path gets written for every page.
    """
    p = page.write(env, out_dir)
    assert p == out_dir / out_path
    assert p.exists()
    assert page.title in p.read_text()


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


def test_sort_date() -> None:
    """
    The sort date is the date of the post, unless it's been updated,
    in which case it's the date updated.
    """
    p = Page(date=datetime(2001, 1, 1))
    assert p.sort_date == datetime(2001, 1, 1)

    p.date_updated = datetime(2002, 2, 2)
    assert p.sort_date == datetime(2002, 2, 2)
