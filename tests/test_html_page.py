"""
Tests for `mosaic.html_page`.
"""

from datetime import datetime
from pathlib import Path

import pytest

from mosaic.html_page import HtmlPage


def test_read_error_includes_filename(tmp_path: Path) -> None:
    """
    An error reading the Markdown file includes the filename.
    """
    src_dir = tmp_path / "src"
    md_path = src_dir / "example.md"

    with pytest.raises(RuntimeError, match=str(md_path)):
        HtmlPage.from_path(src_dir, md_path)


@pytest.mark.parametrize(
    "page, url",
    [
        (
            HtmlPage(
                layout="page",
                src_dir=Path("src"),
                md_path=Path("src/contact.md"),
                title="Contact",
                content="Contact me",
            ),
            "/contact/",
        ),
        (
            HtmlPage(
                layout="page",
                src_dir=Path("src"),
                md_path=Path("src/index.md"),
                title="Homepage",
                content="This is my homepage",
            ),
            "/",
        ),
        (
            HtmlPage(
                layout="post",
                src_dir=Path("src"),
                md_path=Path("src/2013/2013-02-13-darwin.md"),
                date=datetime(2013, 2, 13),
                title="Darwin",
                content="This is a post about Darwin",
            ),
            "/2013/darwin/",
        ),
        (
            HtmlPage(
                layout="til",
                src_dir=Path("src"),
                md_path=Path("src/_til/2013/2013-05-11-rss-podcasts-tumblr"),
                date=datetime(2013, 5, 11),
                title="RSS podcasts on Tumblr",
                content="This is a post about Tumblr",
            ),
            "/til/2013/rss-podcasts-tumblr/",
        ),
    ],
)
def test_url(page: HtmlPage, url: str) -> None:
    """
    Check the URL for every page.
    """
    assert page.url == url


def test_out_path() -> None:
    """
    Check the output path for a page.
    """
    page = HtmlPage(
        layout="page",
        src_dir=Path("src"),
        md_path=Path("src/contact.md"),
        title="Contact",
        content="Contact me",
    )
    assert page.out_path(out_dir=Path("_out")) == Path("_out/contact/index.html")
