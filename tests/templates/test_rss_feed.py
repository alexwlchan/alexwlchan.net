"""
Tests for `mosaic.templates.rss_feed`.
"""

from jinja2 import Environment
import pytest

from mosaic.templates.rss_feed import fix_youtube_iframes, xml_escape


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


def test_fix_youtube_iframes(env: Environment) -> None:
    """
    Test that my YouTube embeds are replaced with inline links.
    """
    md = '{% youtube "https://www.youtube.com/watch?v=Ej2EJVMkTKw" %}'

    html = env.from_string(md).render()

    assert fix_youtube_iframes(html).strip() == (
        '<p><a href="https://www.youtube.com/watch?v=Ej2EJVMkTKw">'
        "https://www.youtube.com/watch?v=Ej2EJVMkTKw</a></p>"
    )
