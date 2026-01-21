"""
Tests for `mosaic.css`.
"""

from pathlib import Path

import pytest

from mosaic.css import create_base_css, get_inline_styles, ParsedStyles


def test_css_has_no_imports() -> None:
    """
    The generated CSS has resolved all the @import statements.
    """
    assert "@import" not in create_base_css("css/style.css")


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
        (
            '<p>Hello world!</p>\n<style type="x-text/scss">@use "components/dot_list";</style>',
            {
                "html": "<p>Hello world!</p>",
                "styles": Path("css/components/dot_list.css").read_text(),
            },
        ),
    ],
)
def test_get_inline_styles(html: str, parsed_styles: ParsedStyles) -> None:
    """
    Tests for get_inline_styles().
    """
    assert get_inline_styles(html) == parsed_styles
