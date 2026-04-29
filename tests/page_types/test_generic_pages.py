"""
Tests for `mosaic.page_types.generic_pages`.
"""

from pathlib import Path

import pytest

from mosaic.page_types import BreadcrumbEntry, Page


def test_page_properties(src_dir: Path) -> None:
    """
    Test the basic properties of a page.
    """
    p = Page(
        md_path=src_dir / "subtopic/example-page.md",
        src_dir=src_dir,
    )

    assert p.template_name == "page.html"
    assert p.url == "/subtopic/example-page/"
    assert p.breadcrumb == []


@pytest.mark.parametrize(
    "filename, url, expected_url",
    [
        ("subtopic/example-page.md", None, "/subtopic/example-page/"),
        ("subtopic/example-page/index.md", None, "/subtopic/example-page/"),
        ("subtopic/example-page/index.md", "/override/", "/override/"),
    ],
)
def test_page_url(
    src_dir: Path, filename: str, url: str | None, expected_url: str
) -> None:
    """
    Test the URL of a page.
    """
    p = Page(md_path=src_dir / filename, src_dir=src_dir, url=url)
    assert p.url == expected_url


def test_custom_breadcrumb(src_dir: Path) -> None:
    """
    Test setting the custom breadcrumb for a page.
    """
    breadcrumb = [BreadcrumbEntry(label="projects", href="/projects/")]
    p = Page(
        md_path=src_dir / "projects/help.md", src_dir=src_dir, breadcrumb=breadcrumb
    )
    assert p.breadcrumb == breadcrumb
