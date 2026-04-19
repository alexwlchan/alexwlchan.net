"""
Tests for `mosaic.site`.
"""

from datetime import datetime
import functools
from pathlib import Path
import random
import time

from jinja2 import Environment
import pytest

from mosaic.page_types import (
    Article,
    BaseHtmlPage,
    BookContributor,
    BookInfo,
    BookReview,
    Note,
    ReviewInfo,
    TopicPage,
)
from mosaic.site import Site
from mosaic.templates import get_jinja_environment
from mosaic.tint_colours import TintColours


def test_page_properties(src_dir: Path) -> None:
    """
    Tests for the per-page type properties of `Site`.
    """
    article1 = Article(
        src_dir=src_dir,
        date=datetime(2001, 1, 1),
        md_path=src_dir / "_articles/2001/2001-01-01-article.md",
    )
    article2 = Article(
        src_dir=src_dir,
        date=datetime(2002, 2, 2),
        md_path=src_dir / "_articles/2002/2002-02-02-article.md",
    )
    article3 = Article(
        src_dir=src_dir,
        date=datetime(2003, 3, 3),
        md_path=src_dir / "_articles/2003/2003-03-03-article.md",
    )

    def make_book_review(date_read: datetime) -> BookReview:
        return BookReview(
            date=date_read,
            src_dir=src_dir,
            md_path=src_dir / f"book_review_{date_read.day}.md",
            book=BookInfo(
                title="Example book",
                contributors=[BookContributor(name="Jane Smith")],
                genres=[],
                publication_year=2020,
            ),
            review=ReviewInfo(date_read=date_read, format="paperback", rating=3),
        )

    book_review4 = make_book_review(date_read=datetime(2004, 4, 4))
    book_review5 = make_book_review(date_read=datetime(2005, 5, 5))
    book_review6 = make_book_review(date_read=datetime(2006, 6, 6))

    note7 = Note(
        src_dir=src_dir,
        date=datetime(2007, 7, 7),
        md_path=src_dir / "notes/2007/2007-07-07-note.md",
        topics=["Topic 7"],
    )
    note8 = Note(
        src_dir=src_dir,
        date=datetime(2008, 8, 8),
        md_path=src_dir / "notes/2008/2008-08-08-note.md",
        topics=["Topic 8"],
    )
    note9 = Note(
        src_dir=src_dir,
        date=datetime(2009, 9, 9),
        md_path=src_dir / "notes/2009/2009-09-09-note.md",
        topics=["Topic 9"],
    )

    make_topic = functools.partial(
        TopicPage, src_dir=src_dir, md_path=src_dir / "topic.md"
    )
    page_sqlite = make_topic(title="SQLite")
    page_docker = make_topic(title="Docker")
    page_python = make_topic(title="Python")

    all_pages = [
        article1,
        article2,
        article3,
        book_review4,
        book_review5,
        book_review6,
        note7,
        note8,
        note9,
        page_sqlite,
        page_python,
        page_docker,
    ]
    random.shuffle(all_pages)

    site = Site(all_pages=all_pages)

    assert site.articles == [article3, article2, article1]
    assert site.book_reviews == [book_review6, book_review5, book_review4]
    assert site.notes == [note9, note8, note7]

    assert len(site.pages) == 3
    assert page_sqlite in site.pages
    assert page_docker in site.pages
    assert page_python in site.pages


def test_generate_rss_feeds(env: Environment, src_dir: Path, out_dir: Path) -> None:
    """
    Tests generating the RSS feeds for the site.
    """
    (out_dir / "notes").mkdir(parents=True)

    all_pages: list[BaseHtmlPage] = [
        Article(
            src_dir=src_dir,
            md_path=src_dir / f"_articles/{year}/{year}-01-01-article.md",
            date=datetime(year, 1, 1),
            content=f"Article posted in {year}",
        )
        for year in range(2000, 2051)
    ] + [
        Note(
            src_dir=src_dir,
            md_path=src_dir / f"notes/{year}/{year}-02-02-note.md",
            date=datetime(year, 2, 2),
            topics=["Topic 1", "Topic 2", "Topic 3"],
            content=f"Note posted in {year}",
        )
        for year in range(2000, 2051)
    ]

    site = Site(src_dir=src_dir, out_dir=out_dir, all_pages=all_pages)
    env.globals.update({"site": site})
    site.generate_rss_feeds(env)

    assert (out_dir / "atom.xml").exists()
    assert (out_dir / "notes/atom.xml").exists()

    articles_rss = (out_dir / "atom.xml").read_text()
    notes_rss = (out_dir / "notes/atom.xml").read_text()

    # Check they both contain the most recent 25 posts
    assert "Article posted in 2050" in articles_rss
    assert "Article posted in 2026" in articles_rss
    assert "Article posted in 2025" not in articles_rss

    assert "Note posted in 2050" in notes_rss
    assert "Note posted in 2026" in notes_rss
    assert "Note posted in 2025" not in notes_rss


def test_writing_page_repeatedly(
    env: Environment, src_dir: Path, out_dir: Path
) -> None:
    """
    Test writing a page multiple times.

    This tests the caching logic for generating the page HTML; rather than
    generating it fresh every time, it's cached in the database and only
    regenerated when the page content or template changes.
    """
    a = Article(
        src_dir=src_dir,
        md_path=src_dir / "_articles/2001/2001-01-01-article.md",
        date=datetime(2001, 1, 1),
        content="An example article",
    )

    env = get_jinja_environment(src_dir, out_dir)
    env.globals.update({"css_url": "/static/style.css"})

    out_path1 = a.write(env, out_dir)
    out_body1 = a.render_body_html(env)
    out_text1 = out_path1.read_text()
    assert out_path1 == out_dir / "2001/article/index.html"

    out_path2 = a.write(env, out_dir)
    out_body2 = a.render_body_html(env)
    out_text2 = out_path2.read_text()
    assert out_path1 == out_path2
    assert out_body1 == out_body2
    assert out_text1 == out_text2


def test_writing_page_checks_for_deletion(
    env: Environment, src_dir: Path, out_dir: Path
) -> None:
    """
    If a page was written previously but no longer exists, it gets re-written.
    """
    a = Article(
        src_dir=src_dir,
        md_path=src_dir / "_articles/2001/2001-01-01-article.md",
        date=datetime(2001, 1, 1),
        content="An example article",
    )

    env = get_jinja_environment(src_dir, out_dir)
    env.globals.update({"css_url": "/static/style.css"})

    out_path1 = a.write(env, out_dir)
    assert out_path1.exists()
    out_path1.unlink()

    out_path2 = a.write(env, out_dir)
    assert out_path2.exists()


def test_copy_static_files(src_dir: Path, out_dir: Path) -> None:
    """
    Test copying static files between the two directories.
    """
    site = Site(src_dir=src_dir, out_dir=out_dir, all_pages=[])

    # Create three images in the source directory, and check that the
    # two binary files are copied but the Markdown file is not.
    files = [
        ("my-article.md", b"this article should not be copied"),
        ("images/123.bin", b"this image should be copied"),
        ("files/2017/456.bin", b"this file should also be copied"),
    ]

    for path, contents in files:
        (src_dir / path).parent.mkdir(parents=True, exist_ok=True)
        (src_dir / path).write_bytes(contents)

    site.copy_static_files()

    assert not (out_dir / "my-article.md").exists()
    assert (out_dir / "images/123.bin").read_bytes() == b"this image should be copied"
    assert (
        out_dir / "files/2017/456.bin"
    ).read_bytes() == b"this file should also be copied"

    # Update one of the binary files, and check the updated version is
    # copied to the out_dir.
    time.sleep(2)
    (src_dir / "images/123.bin").write_bytes(b"this image has been updated")
    site.copy_static_files()
    assert (out_dir / "images/123.bin").read_bytes() == b"this image has been updated"

    # Remove one of the files from the output directory, and check it's
    # replaced on the next run.
    (out_dir / "files/2017/456.bin").unlink()
    site.copy_static_files()
    assert (
        out_dir / "files/2017/456.bin"
    ).read_bytes() == b"this file should also be copied"


class TestSite:
    """
    Tests for methods on Site.
    """

    @pytest.fixture
    def pages(self, src_dir: Path) -> list[BaseHtmlPage]:
        """
        Return a set of three pages to use in the site.
        """
        article = Article(
            src_dir=src_dir,
            date=datetime(2001, 1, 1),
            md_path=src_dir / "_articles/2001/2001-01-01-article.md",
        )
        note = Note(
            src_dir=src_dir,
            date=datetime(2002, 2, 2),
            md_path=src_dir / "notes/2002/2002-02-02-note.md",
            topics=["Python"],
        )
        page = TopicPage(src_dir=src_dir, md_path=src_dir / "topic.md", title="Python")

        return [article, note, page]

    def test_check_for_duplicate_urls(
        self, src_dir: Path, out_dir: Path, pages: list[BaseHtmlPage]
    ) -> None:
        """
        Duplicate URLs are detected and rejected.
        """
        # Check that the initial list is fine
        site = Site(src_dir=src_dir, out_dir=out_dir, all_pages=pages)
        site.check_for_duplicate_urls()

        # Now send every item in the list twice, and check the site fails
        # validation.
        site.all_pages = pages + pages
        with pytest.raises(RuntimeError, match="multiple pages write to the same URL"):
            site.check_for_duplicate_urls()

    def test_create_tint_colour_assets(
        self, src_dir: Path, out_dir: Path, pages: list[BaseHtmlPage]
    ) -> None:
        """
        Tint colour assets are created for every page's tint colour.
        """
        pages[0].colors = TintColours(css_light="#ab5326", css_dark="#f49d61")
        pages[1].colors = TintColours(css_light="#4d27A8", css_dark="#955df4")

        site = Site(src_dir=src_dir, out_dir=out_dir, all_pages=pages)
        site.create_all_tint_colour_assets()

        headers_dir = out_dir / "h"
        assert set(headers_dir.iterdir()) == {
            headers_dir / "ab5326.png",
            headers_dir / "f49d61.png",
            headers_dir / "4d27a8.png",
            headers_dir / "955df4.png",
            headers_dir / "d01c11.png",
            headers_dir / "ff4a4a.png",
        }

        favicons_dir = out_dir / "f"
        for name in [
            "ab5326.ico",
            "f49d61.ico",
            "4d27a8.ico",
            "955df4.ico",
            "d01c11.ico",
            "ff4a4a.ico",
        ]:
            assert (favicons_dir / name).exists()

    def test_write_html_files(
        self, src_dir: Path, out_dir: Path, env: Environment, pages: list[BaseHtmlPage]
    ) -> None:
        """
        Test for the write_html_files function.
        """
        site = Site(src_dir=src_dir, out_dir=out_dir, all_pages=pages)
        site.write_html_files(env)

        assert (out_dir / "2001/article/index.html").exists()
        assert (out_dir / "notes/2002/note/index.html").exists()
        assert (out_dir / "python/index.html").exists()
