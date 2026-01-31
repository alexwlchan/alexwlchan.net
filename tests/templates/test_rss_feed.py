"""
Tests for `mosaic.templates.rss_feed`.
"""

import pytest

from mosaic.templates.rss_feed import xml_escape


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
