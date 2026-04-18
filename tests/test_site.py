"""
Tests for `mosaic.site`.
"""

from datetime import datetime
import functools
from pathlib import Path
import random

from jinja2 import Environment

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
            md_path=src_dir / "book_review.md",
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
    page_crafts = make_topic(title="Crafts")
    page_github = make_topic(title="GitHub")
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
        page_crafts,
        page_python,
        page_github,
    ]
    random.shuffle(all_pages)

    site = Site(all_pages=all_pages)

    assert site.articles == [article3, article2, article1]
    assert site.book_reviews == [book_review6, book_review5, book_review4]
    assert site.notes == [note9, note8, note7]

    assert len(site.pages) == 3
    assert page_crafts in site.pages
    assert page_github in site.pages
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
            html_content=f"Article posted in {year}",
        )
        for year in range(2000, 2051)
    ] + [
        Note(
            src_dir=src_dir,
            md_path=src_dir / f"notes/{year}/{year}-02-02-note.md",
            date=datetime(year, 2, 2),
            topics=["Topic 1", "Topic 2", "Topic 3"],
            html_content=f"Note posted in {year}",
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
