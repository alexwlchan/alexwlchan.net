"""
Tests for `mosaic.templates`.
"""

import pytest

from mosaic.templates import text as t


def test_markdownify() -> None:
    """
    Test markdownify().
    """
    md = "This is some text.\n\nThis is *emphasised* text."
    expected = "<p>This is some text.</p>\n<p>This is <em>emphasised</em> text.</p>"
    actual = t.markdownify(md)

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
