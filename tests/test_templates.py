"""
Tests for `mosaic.templates`.
"""

import pytest

from mosaic import templates as t


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
    "html, parsed_styles",
    [
        ("<p>Hello world!</p>", {"html": "<p>Hello world!</p>", "styles": ""}),
        (
            "<p>Hello world!</p>\n"
            "<style>p { color: red; }</style>\n"
            "<span>Greetings friends!</span>\n"
            "<style>span { color: blue; }</style>\n"
            "<style>p { color: red; }</style>\n",
            {
                "html": "<p>Hello world!</p><span>Greetings friends!</span>",
                "styles": "p { color: red; }span { color: blue; }",
            },
        ),
        (
            "<p>Hello world!</p>\n<defs><style>p { color: red; }</style></defs>",
            {
                "html": "<p>Hello world!</p>",
                "styles": "p { color: red; }",
            },
        ),
    ],
)
def test_get_inline_styles(html: str, parsed_styles: t.ParsedStyles) -> None:
    """
    Tests for get_inline_styles().
    """
    assert t.get_inline_styles(html) == parsed_styles
