"""
Tests for `mosaic.page_types.notes`.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from mosaic.page_types import Article, BreadcrumbEntry


def test_article_properties(src_dir: Path) -> None:
    """
    Test the basic properties of an article.
    """
    a = Article(
        md_path=src_dir / "_articles/2026/2026-02-03-example-article.md",
        src_dir=src_dir,
        date=datetime(2026, 2, 3),
        topics=["Python"],
    )

    assert a.template_name == "article.html"
    assert a.url == "/2026/example-article/"
    assert a.breadcrumb() == [
        BreadcrumbEntry(label="Computers and code", href="/computers-and-code/"),
        BreadcrumbEntry(label="Python", href="/python/"),
    ]


def test_article_with_no_topics_has_bare_breadcrumb(src_dir: Path) -> None:
    """
    Test the basic properties of an article.
    """
    a = Article(
        md_path=src_dir / "_articles/2026/2026-02-03-example-article.md",
        src_dir=src_dir,
        date=datetime(2026, 2, 3),
        topics=[],
    )

    assert a.breadcrumb() == [
        BreadcrumbEntry(label="articles", href="/articles/"),
    ]


@pytest.mark.parametrize(
    "date",
    [
        datetime.now(tz=timezone.utc),
        datetime.now(tz=timezone.utc) - timedelta(days=1),
        datetime.now(tz=timezone.utc) - timedelta(days=13),
        datetime.now(tz=timezone.utc) - timedelta(days=21),
    ],
)
def test_recent_days_are_new(src_dir: Path, date: datetime) -> None:
    """
    An article published in the last 21 days is new.
    """
    a = Article(md_path=src_dir / "_articles/example.md", src_dir=src_dir, date=date)
    assert a.is_new


@pytest.mark.parametrize(
    "date",
    [
        datetime.now(tz=timezone.utc) - timedelta(days=22),
        datetime.now(tz=timezone.utc) - timedelta(days=28),
        datetime.now(tz=timezone.utc) - timedelta(days=365),
    ],
)
def test_older_days_are_new(src_dir: Path, date: datetime) -> None:
    """
    An article published more than 14 days ago is not new.
    """
    a = Article(md_path=src_dir / "_articles/example.md", src_dir=src_dir, date=date)
    assert not a.is_new
