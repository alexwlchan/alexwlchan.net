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


class TestChooseSharingCard:
    """
    Tests for a sharing card for a post.
    """

    def test_no_card_dir(self, src_dir: Path) -> None:
        """
        If there's no per-year card directory for this post, there's no
        sharing card.
        """
        a = Article(
            md_path=src_dir / "_articles/3030/3030-03-03-article.md",
            src_dir=src_dir,
            date=datetime(3030, 3, 3),
        )
        assert a.card_path is None

    def test_matching_card(self, src_dir: Path) -> None:
        """
        If we look in the card directory and there's a single matching
        card for this post, use that as the sharing card.
        """
        (src_dir / "_images/cards/2001").mkdir(parents=True)
        (src_dir / "_images/cards/2001/article.jpg").write_text("JPEG")

        a = Article(
            md_path=src_dir / "_articles/2001/2001-01-01-article.md",
            src_dir=src_dir,
            date=datetime(2001, 1, 1),
        )
        assert a.card_path == Path("_images/cards/2001/article.jpg")

    def test_no_matching_card(self, src_dir: Path) -> None:
        """
        If we look in the card directory and there are no matching cards,
        there's no sharing card.
        """
        (src_dir / "_images/cards/2001").mkdir(parents=True)
        (src_dir / "_images/cards/2001/different-article.jpg").write_text("JPEG")

        a = Article(
            md_path=src_dir / "_articles/2001/2001-01-01-article.md",
            src_dir=src_dir,
            date=datetime(2001, 1, 1),
        )
        assert a.card_path is None

    def test_ambiguous_matching_cards(self, src_dir: Path) -> None:
        """
        If we look in the card directory and there are multiple matching
        cards, we get a ValueError.
        """
        (src_dir / "_images/cards/2001").mkdir(parents=True)
        (src_dir / "_images/cards/2001/article.jpg").write_text("JPEG")
        (src_dir / "_images/cards/2001/article.png").write_text("PNG")

        with pytest.raises(ValueError, match="multiple matching cards"):
            Article(
                md_path=src_dir / "2001-01-01-article.md",
                src_dir=src_dir,
                date=datetime(2001, 1, 1),
            )
