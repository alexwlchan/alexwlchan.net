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
    make_article = functools.partial(
        Article, src_dir=src_dir, md_path=src_dir / "article.md"
    )
    article1 = make_article(date=datetime(2001, 1, 1))
    article2 = make_article(date=datetime(2002, 2, 2))
    article3 = make_article(date=datetime(2003, 3, 3))

    def make_book_review(date_read: datetime) -> BookReview:
        return BookReview(
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

    make_note = functools.partial(Note, src_dir=src_dir, md_path=src_dir / "note.md")
    note7 = make_note(date=datetime(2007, 7, 7))
    note8 = make_note(date=datetime(2008, 8, 8))
    note9 = make_note(date=datetime(2009, 9, 9))

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
        Article(src_dir=src_dir, md_path=src_dir / "article.md", date=datetime.now())
        for _ in range(3)
    ] + [
        Note(src_dir=src_dir, md_path=src_dir / "article.md", date=datetime.now())
        for _ in range(3)
    ]

    site = Site(src_dir=src_dir, out_dir=out_dir, all_pages=all_pages)
    env.globals.update({"site": site})
    site.generate_rss_feeds(env)

    assert (out_dir / "atom.xml").exists()
    assert (out_dir / "notes/atom.xml").exists()
