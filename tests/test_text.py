"""
Tests for `mosaic.templates`.
"""

import pytest

from mosaic import text as t


@pytest.mark.parametrize(
    "md, expected",
    [
        (
            "This is some text.\n\nThis is *emphasised* text.",
            "<p>This is some text.</p>\n<p>This is <em>emphasised</em> text.</p>",
        ),
        (
            "*   This is a list item\n\n"
            "    <table><tr><td>Hello</td><td>World</td></tr></table>\n\n"
            "*   This is another list item",
            "<ul>\n<li>\n<p>This is a list item</p>\n"
            "<table><tr><td>Hello</td><td>World</td></tr></table>\n</li>\n"
            "<li>\n<p>This is another list item</p>\n</li>\n</ul>",
        ),
    ],
)
def test_markdownify(md: str, expected: str) -> None:
    """
    Test markdownify().
    """
    actual = t.markdownify(md)
    print(repr(actual))
    assert actual == expected


def test_markdownify_oneline() -> None:
    """
    Test markdownify_oneline().
    """
    md = "This is *emphasised* text."
    expected = "This is <em>emphasised</em> text."
    actual = t.markdownify_oneline(md)

    assert actual == expected


@pytest.mark.parametrize(
    "text, cleaned_text",
    [
        ("Hello world!", "Hello world!"),
        ("Apollo 11", "Apollo&nbsp;11"),
        ("5 seconds", "5&nbsp;seconds"),
        (
            "My first sentence. A new sentence.",
            "My first sentence. A&nbsp;new sentence.",
        ),
        (
            "My first sentence.\nA new sentence.",
            "My first sentence.\nA&nbsp;new sentence.",
        ),
        ("After x and y is the z-axis", "After x and y is the z&#8209;axis"),
    ],
)
def test_cleanup_text(text: str, cleaned_text: str) -> None:
    """
    Tests for cleanup_text().
    """
    assert t.cleanup_text(text) == cleaned_text


@pytest.mark.parametrize(
    "html, cleaned_html",
    [
        ("Hello world!", "Hello world!"),
        ("Hello <em>world</em>!", "Hello world!"),
    ],
)
def test_strip_html(html: str, cleaned_html: str) -> None:
    """
    Tests for strip_html().
    """
    assert t.strip_html(html) == cleaned_html


def test_find_unique_prefixes() -> None:
    """
    Test the example given for `find_unique_prefixes`.
    """
    actual = t.find_unique_prefixes({"amber", "application", "banana"})
    expected = {"amber": "am", "application": "ap", "banana": "b"}
    assert actual == expected
