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
    _, css = create_base_css()
    assert "@import" not in css


@pytest.mark.parametrize(
    "html, parsed_styles",
    [
        pytest.param(
            "<p>Hello world!</p>",
            ParsedStyles(html="<p>Hello world!</p>", styles=""),
            id="no_css",
        ),
        pytest.param(
            "<p>Hello world!</p>\n"
            "<style>p { color: red; }</style>\n"
            "<span>Greetings friends!</span>\n"
            "<style>span { color: blue; }</style>\n"
            "<style>p { color: red; }</style>\n",
            ParsedStyles(
                html="<p>Hello world!</p><span>Greetings friends!</span>",
                styles="p { color: red; }span { color: blue; }",
            ),
            id="inline_styles_with_duplicates",
        ),
        pytest.param(
            "<p>Hello world!</p>\n<defs><style>p { color: red; }</style></defs>",
            ParsedStyles(
                html="<p>Hello world!</p>",
                styles="p { color: red; }",
            ),
            id="inline_styles_which_leave_empty_defs",
        ),
        pytest.param(
            (
                "<p>Hello world!</p>\n"
                '<link href="css/components/dot_list.css" rel="stylesheet"/>'
            ),
            ParsedStyles(
                html="<p>Hello world!</p>",
                styles=Path("css/components/dot_list.css").read_text(),
            ),
            id="link_tag",
        ),
        pytest.param(
            '<link as="image" href="/static/2025/truchet-header-light.svg" '
            'media="(prefers-color-scheme: light)" rel="preload" type="image/svg"/>',
            ParsedStyles(
                html=(
                    '<link as="image" href="/static/2025/truchet-header-light.svg" '
                    'media="(prefers-color-scheme: light)" rel="preload" '
                    'type="image/svg"/>'
                ),
                styles="",
            ),
            id="link_tag_non_stylesheet",
        ),
    ],
)
def test_get_inline_styles(html: str, parsed_styles: ParsedStyles) -> None:
    """
    Tests for get_inline_styles().
    """
    assert get_inline_styles(html) == parsed_styles


def test_inline_style_with_invalid_link() -> None:
    """
    A <link> tag which points to a non-existent CSS file is an error.
    """
    html = (
        "<p>Hello world!</p>\n"
        '<link href="css/components/does_not_exist.css" rel="stylesheet"/>'
    )

    with pytest.raises(ValueError, match="missing file"):
        get_inline_styles(html)
