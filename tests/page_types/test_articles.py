"""
Tests for `mosaic.page_types.notes`.
"""

from datetime import datetime
from pathlib import Path


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

    assert a.template_name == "post.html"
    assert a.url == "/2026/example-article/"
    assert a.breadcrumb() == [
        BreadcrumbEntry(label="Systems and software", href="/systems/"),
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
