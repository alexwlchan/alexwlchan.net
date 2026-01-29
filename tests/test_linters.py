"""
Tests for `mosaic.linters`.
"""

from pathlib import Path

import bs4
import pytest

from mosaic.linters import (
    check_no_broken_html,
    check_no_localhost_links,
    check_redirects,
)


class TestCheckNoBrokenHtml:
    """
    Tests for `check_no_broken_html`.
    """

    @pytest.mark.parametrize(
        "html", ["<p><table>", "<p>&lt;pre&gt;", "<p><p>", "<picture>&lt;/picture>"]
    )
    def test_spots_bad_tag_after_p(self, html: str) -> None:
        """
        The lint catches examples of malformed HTML.
        """
        assert check_no_broken_html(html)

    @pytest.mark.parametrize("html", ["<p><em>", "<p>Abc"])
    def test_allows_inline_tag_after_p(self, html: str) -> None:
        """
        The lint catches a <p> tag followed by a block element.
        """
        assert check_no_broken_html(html) == []


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


@pytest.fixture
def redirects_path(tmp_path: Path) -> Path:
    """
    Returns the path to a redirects Caddyfile.
    """
    return tmp_path / "redirects.Caddyfile"


class TestCheckRedirects:
    """
    Tests for `check_redirects`.
    """

    def create_html_files(self, *paths: Path) -> None:
        """
        Create a set of HTML files.
        """
        for p in paths:
            p.parent.mkdir(exist_ok=True, parents=True)
            p.write_text("example html page")

    def test_happy_path(self, redirects_path: Path, out_dir: Path) -> None:
        """
        Test the case where redirects are consistent.
        """
        redirects_path.write_text(
            "redir /oldpage1 /newpage1 permanent\n"
            "redir /oldpage2/ /newpage2/ permanent\n"
        )

        self.create_html_files(
            out_dir / "newpage1/index.html", out_dir / "newpage2/index.html"
        )

        assert check_redirects(redirects_path, out_dir) == []

    def test_ignores_mastodon_pages(self, redirects_path: Path, out_dir: Path) -> None:
        """
        Parsing the redirects file ignores my Mastodon redirects.
        """
        redirects_path.write_text(
            "redir /.well-known/host-meta* "
            "https://social.alexwlchan.net/.well-known/host-meta permanent\n"
            "redir /oldpage1 /newpage1 permanent\n"
        )

        self.create_html_files(out_dir / "newpage1/index.html")

        assert check_redirects(redirects_path, out_dir) == []

    def test_redirect_from_existing_file_is_err(
        self, redirects_path: Path, out_dir: Path
    ) -> None:
        """
        Redirecting from a file that exists is an error.
        """
        redirects_path.write_text("redir /newpage1 /newpage2 permanent\n")

        self.create_html_files(
            out_dir / "newpage1/index.html", out_dir / "newpage2/index.html"
        )

        assert check_redirects(redirects_path, out_dir) == [
            "L1: redirect from file that exists (/newpage1)"
        ]

    def test_duplicate_sources_are_err(
        self, redirects_path: Path, out_dir: Path
    ) -> None:
        """
        Multiple entries for the same redirect source are an error.
        """
        redirects_path.write_text(
            "redir /oldpage1 /newpage1 permanent\n"
            "redir /oldpage2 /newpage2 permanent\n"
            "redir /oldpage1 /newpage2 permanent\n"
        )

        self.create_html_files(
            out_dir / "newpage1/index.html", out_dir / "newpage2/index.html"
        )

        assert check_redirects(redirects_path, out_dir) == [
            "duplicate source on lines L1, L3 (/oldpage1)"
        ]

    def test_redirect_to_missing_file_is_err(
        self, redirects_path: Path, out_dir: Path
    ) -> None:
        """
        Redirecting to a file that doesn't exist is an error.
        """
        redirects_path.write_text(
            "redir /oldpage1 /newpage1 permanent\nredir /oldpage2 /newpage2 permanent\n"
        )

        self.create_html_files(out_dir / "newpage1/index.html")

        assert check_redirects(redirects_path, out_dir) == [
            "L2: redirect to a page that does not exist (/newpage2)"
        ]
