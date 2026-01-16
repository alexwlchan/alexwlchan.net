"""
Tests for `mosaic.linters`.
"""

import bs4
import pytest

from mosaic.linters import check_no_localhost_links


class TestCheckNoLocalhostLinks:
    """
    Tests for `check_no_localhost_links`.
    """

    @pytest.mark.parametrize(
        "html",
        [
            '<p>This is some text</p><a href="http://localhost:5757/example">example</a>',
            '<a href="http://localhost:5757/">localhost</a>',
        ],
    )
    def test_blocks_localhost_links(self, html: str) -> None:
        """
        Links to a localhost URL are blocked.
        """
        soup = bs4.BeautifulSoup(html, "html.parser")
        assert check_no_localhost_links(soup)

    @pytest.mark.parametrize(
        "html",
        [
            "<p>This text has no links</p>",
            '<p>This is some text</p><a href="https://example.com">example</a>',
            '<a href="http://example.com/post-about-localhost">a post</a>',
            '<a onclick="script:toggleAllAnimations()">toggle animations</a>',
            '<a href="http://localhost:8080/example">example</a>',
            '<a href="http://example-localhost.com/">example</a>',
        ],
    )
    def test_allows_non_localhost_links(self, html: str) -> None:
        """
        Links to non-localhost URLs are allowed.
        """
        soup = bs4.BeautifulSoup(html, "html.parser")
        assert check_no_localhost_links(soup) == []
