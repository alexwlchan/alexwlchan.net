# ruff: noqa: E501
"""
Tests for `mosaic.linters`.
"""

from pathlib import Path

from bs4 import BeautifulSoup
import pytest

from mosaic.linters import (
    check_all_urls_are_hackable,
    check_images_have_alt_text,
    check_links_are_consistent,
    check_no_broken_html,
    check_no_localhost_links,
    check_redirects,
    get_all_hackable_urls,
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
        The lint ignores examples of valid HTML.
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
        soup = BeautifulSoup(html, "html.parser")
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
        soup = BeautifulSoup(html, "html.parser")
        assert check_no_localhost_links(soup) == []


class TestCheckImagesHaveAltText:
    """
    Tests for `check_images_have_alt_text`.
    """

    @pytest.mark.parametrize(
        "html",
        ["<img src='cat.jpg'>", "<img alt='dog' src='dog.png'><img src='fish.gif'>"],
    )
    def test_spots_bad_tag_after_p(self, html: str) -> None:
        """
        Images without alt text are blocked.
        """
        soup = BeautifulSoup(html, "html.parser")
        assert check_images_have_alt_text(soup)

    @pytest.mark.parametrize(
        "html",
        [
            "<p></p>",
            "<img alt='ocelot' src='ocelot.png'>",
            "<img data-proofer-ignore src='hippo.tif'>",
        ],
    )
    def test_allows_inline_tag_after_p(self, html: str) -> None:
        """
        No images or images with alt text are allowed.
        """
        soup = BeautifulSoup(html, "html.parser")
        assert check_images_have_alt_text(soup) == []


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


def test_get_all_hackable_urls() -> None:
    """
    Test `get_all_hackable_urls`.
    """
    assert list(get_all_hackable_urls("/til/2024/block-specific-ip-addresses/")) == [
        "/til/2024/block-specific-ip-addresses/",
        "/til/2024/",
        "/til/",
        "/",
    ]


class TestCheckAllUrlsAreHackable:
    """
    Tests for `check_all_urls_are_hackable`.
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
        Test the case where all URLs are hackable.
        """
        redirects_path.write_text("redir /old-notes/ /notes/ permanent\n")

        self.create_html_files(
            out_dir / "index.html",
            out_dir / "notes/index.html",
            out_dir / "notes/my-first-note/index.html",
            out_dir / "notes/my-second-note/index.html",
            out_dir / "old-notes/my-third-note/index.html",
        )

        assert check_all_urls_are_hackable(redirects_path, out_dir) == []

    def test_spots_unhackable_url(self, redirects_path: Path, out_dir: Path) -> None:
        """
        A URL which can't be "hacked" is an error.
        """
        redirects_path.write_text("redir /alt-notes/ /notes/ permanent\n")

        self.create_html_files(
            out_dir / "index.html",
            out_dir / "notes/my-first-note/index.html",
            out_dir / "notes/my-second-note/index.html",
            out_dir / "old-notes/my-third-note/index.html",
        )

        assert check_all_urls_are_hackable(redirects_path, out_dir) == [
            "url can be hacked but won’t resolve: '/notes/'",
            "url can be hacked but won’t resolve: '/old-notes/'",
        ]


class TestCheckLinksAreConsistent:
    """
    Tests for `check_links_are_consistent`.
    """

    def test_empty_case(self, out_dir: Path) -> None:
        """
        No pages means no errors.
        """
        assert check_links_are_consistent(out_dir, pages={}) == {}

    @pytest.mark.parametrize(
        "html",
        [
            "<a>no href</a>",
            '<a href="#">bare hash</a>',
            '<a href="?query=1">query parameters</a>',
            '<a href="/other_page/index.html">other page (file)</a>',
            '<a href="/other_page/">other page (URL)</a>',
            '<a href="/other_page/index.html?query=1">other page (file, query)</a>',
            '<a href="/other_page/?query=1">other page (URL, query)</a>',
            '<a href="/other_page/index.html#heading1">other page (file, fragment)</a>',
            '<a href="/other_page/#heading1">other page (URL, fragment)</a>',
            '<a href="/other_page/index.html?query=1#heading1">other page (file, fragment, query)</a>',
            '<a href="/other_page/?query=1#heading1">other page (URL, fragment, query)</a>',
            "<script>inline JS; no src attribute</script>",
            '<source srcset="/cat.jpg">',
            '<source srcset="/cat.jpg 1x">',
            '<source srcset="/cat.jpg 1x, /dog.png 2x">',
            '<meta name="twitter:image" content="https://alexwlchan.net/cat.jpg">',
            '<meta name="og:image" content="https://alexwlchan.net/dog.png">',
            '<a href="tel:0123456789">phone call</a>',
            '<a href="#main">go to main</a><div id="main">main section</div>',
            '<a href="../cat.jpg">relative URL</a>',
        ],
    )
    def test_good_page(self, out_dir: Path, html: str) -> None:
        """
        HTML with internally consistent links is allowed.
        """
        (out_dir / "example").mkdir(parents=True)
        (out_dir / "other_page").mkdir(parents=True)
        (out_dir / "cat.jpg").write_text("JPEG;cat")
        (out_dir / "dog.png").write_text("PNG;dog")

        html_path = out_dir / "example/index.html"
        html_path.write_text(html)
        html_soup = BeautifulSoup(html, "html.parser")

        other_html = (
            '<h1 id="heading1">heading1</h1>\n\n<h2 id="heading2">heading2</h2>'
        )
        other_path = out_dir / "other_page/index.html"
        other_path.write_text(other_html)
        other_soup = BeautifulSoup(other_html, "html.parser")

        pages = {html_path: html_soup, other_path: other_soup}

        assert check_links_are_consistent(out_dir, pages) == {}

    @pytest.mark.parametrize(
        "html, tag, url",
        [
            (
                '<a href="/f/17823e-32x32.svg">static file</a>',
                "a",
                "/f/17823e-32x32.svg",
            ),
            ('<a href="#main">fragment</a>', "a", "#main"),
            ('<img src="/doesnotexist.jpg">', "img", "/doesnotexist.jpg"),
            ('<a href="/doesnotexist/">', "a", "/doesnotexist/"),
            ('<a href="relativepath.gif">', "a", "relativepath.gif"),
            ('<a href="/doesnotexist.html">', "a", "/doesnotexist.html"),
            (
                '<a href="/other/index.html#heading1">',
                "a",
                "/other/index.html#heading1",
            ),
            ('<a href="/other/#heading1">', "a", "/other/#heading1"),
        ],
    )
    def test_link_to_bad_page(
        self, out_dir: Path, html: str, tag: str, url: str
    ) -> None:
        """
        Linking to a non-existent resource gets flagged as an error.
        """
        out_dir.mkdir()
        html_path = out_dir / "example.html"
        html_path.write_text(html)

        other_path = out_dir / "other/index.html"
        other_path.parent.mkdir()
        other_html = "<p>another html file</p>"
        other_path.write_text(other_html)

        pages = {
            html_path: BeautifulSoup(html, "html.parser"),
            other_path: BeautifulSoup(other_html, "html.parser"),
        }

        actual = check_links_are_consistent(out_dir, pages)
        expected = {html_path: [f"broken url in <{tag}>: {url}"]}

        assert actual == expected
