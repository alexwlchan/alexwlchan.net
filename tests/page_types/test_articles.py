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
    assert a.breadcrumb == [
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

    assert a.breadcrumb == [
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
    a = Article(
        md_path=src_dir
        / f"_articles/{date.year}/{date.strftime('%Y-%m-%d')}-example.md",
        src_dir=src_dir,
        date=date,
    )
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
    a = Article(
        md_path=src_dir
        / f"_articles/{date.year}/{date.strftime('%Y-%m-%d')}-example.md",
        src_dir=src_dir,
        date=date,
    )
    assert not a.is_new


def test_articles_can_be_hashed(src_dir: Path) -> None:
    """
    Articles can be hashed.
    """
    a = Article(
        md_path=src_dir / "_articles/2001/2001-01-01-example.md",
        src_dir=src_dir,
        date=datetime(2001, 1, 1),
    )
    hash(a)


@pytest.mark.parametrize(
    "path",
    [
        "articles/2001/2001-01-01-example.md",
        "_articles/2010/2001-01-01-example.md",
        "_articles/2001/2010-01-01-example.md",
        "_articles/2001/example.md",
        "2001/2001-01-01-example.md",
    ],
)
def test_invalid_article_path(src_dir: Path, path: str) -> None:
    """
    Article paths that don't match the metadata are rejected.
    """
    with pytest.raises(ValueError, match="wrong path"):
        Article(md_path=src_dir / path, src_dir=src_dir, date=datetime(2001, 1, 1))
