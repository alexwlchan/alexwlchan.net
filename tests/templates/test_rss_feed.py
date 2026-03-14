"""
Tests for `mosaic.templates.rss_feed`.
"""

from jinja2 import Environment
import pytest

from mosaic.templates.rss_feed import (
    fix_html_for_feed_readers,
    fix_youtube_iframes,
    xml_escape,
)


@pytest.mark.parametrize(
    "text, escaped_xml",
    [
        ("Hello world!", "Hello world!"),
        (
            'This is text with &ampersand& and "quotes"',
            "This is text with &amp;ampersand&amp; and &quot;quotes&quot;",
        ),
        ('The "MCP" in Archivematica', "The &quot;MCP&quot; in Archivematica"),
    ],
)
def test_xml_escape(text: str, escaped_xml: str) -> None:
    """
    Text in XML is escaped correctly.
    """
    assert xml_escape(text) == escaped_xml


@pytest.mark.parametrize(
    "md, cleaned_html",
    [
        (
            '{% youtube "https://www.youtube.com/watch?v=Ej2EJVMkTKw" %}',
            '<p><a href="https://www.youtube.com/watch?v=Ej2EJVMkTKw">'
            "https://www.youtube.com/watch?v=Ej2EJVMkTKw</a></p>",
        ),
        ("Hello world", "Hello world"),
    ],
)
def test_fix_youtube_iframes(env: Environment, md: str, cleaned_html: str) -> None:
    """
    Test that my YouTube embeds are replaced with inline links.
    """
    html = env.from_string(md).render()

    assert fix_youtube_iframes(html).strip() == cleaned_html


class TestFixHtmlForFeedReaders:
    """
    Tests for `fix_html_for_feed_readers`.
    """

    @pytest.mark.parametrize(
        "html",
        [
            "<p>Hello world</p>",
            '<a href="https://alexwlchan.net/2026/example/">Example link</a>',
            '<a data-has-href="false">No href attribute</a>',
        ],
    )
    def test_html_left_as_is(self, html: str) -> None:
        """
        These HTML strings are unmodified by the RSS feed fixer.
        """
        assert fix_html_for_feed_readers(html) == html

    @pytest.mark.parametrize(
        "tag",
        [
            '<link rel="stylesheet" href="style.css"/>',
            '<script>console.log("hello world");</script>',
            "<style>p { color: orange; }</style>",
            "<!-- This is a comment -->",
        ],
    )
    def test_tags_removed(self, tag: str) -> None:
        """
        Certain tags are removed.
        """
        html = f"<p>Red</p>{tag}<p>Blue</p>"
        assert fix_html_for_feed_readers(html) == "<p>Red</p><p>Blue</p>"

    @pytest.mark.parametrize(
        "attrs",
        [
            'style="color: red;"',
            "controls",
            "aria-hidden=true",
            'title="greeting"',
            "onchange=updatePage()",
            "onclick=clickHandler()",
        ],
    )
    def test_attributes_removed(self, attrs: str) -> None:
        """
        Certain attributes are removed.
        """
        html = f'<p {attrs} data-is-greeting="true">Hello world!</p>'
        assert (
            fix_html_for_feed_readers(html)
            == '<p data-is-greeting="true">Hello world!</p>'
        )

    def test_social_embed_tidies(self, env: Environment) -> None:
        """
        Images and avatars in social media embeds get tidied up.
        """
        url = "https://twitter.com/alexwlchan/status/1188721070234394626"
        md = '{% tweet "' + url + '" %}'

        html = env.from_string(md).render()
        fixed_html = fix_html_for_feed_readers(html)

        assert '<img alt="" class="avatar"' not in fixed_html
        assert '<svg class="logo"' not in fixed_html

        assert '<img alt="🐦" class="twemoji"' not in fixed_html
        assert "🐦" in fixed_html

    @pytest.mark.parametrize(
        "html, expected_url",
        [
            ('<img src="/images/cat.jpg">', "https://alexwlchan.net/images/cat.jpg"),
            (
                '<a href="/2026/example/">Example link</a>',
                "https://alexwlchan.net/2026/example/",
            ),
            (
                '<img src="/images/dog_1x.png, /images/dog_2x.png">',
                "https://alexwlchan.net/images/dog_1x.png, https://alexwlchan.net/images/dog_2x.png",
            ),
        ],
    )
    def test_relative_urls_fixed(self, html: str, expected_url: str) -> None:
        """
        Relative URLs are replaced with their absolute counterparts.
        """
        assert expected_url in fix_html_for_feed_readers(html)
