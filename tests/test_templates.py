"""
Tests for `mosaic.templates`.
"""

import pytest

from mosaic import templates as t


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


def test_liquid_comments_are_ignored() -> None:
    """
    Test that Liquid style comments get removed.
    """
    env = t.get_jinja_environment()
    tmpl = env.from_string(
        "Hello world!\n"
        "{% comment %}don’t show this{% endcomment %}\n"
        "Blue and yellow makes green\n"
    )

    assert tmpl.render() == ("Hello world!\n\nBlue and yellow makes green")
