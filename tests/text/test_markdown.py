"""
Tests for `mosaic.text.markdown`.
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
        # Test that block elements like <table> aren't wrapped in <p>
        # when nested inside a list
        (
            "*   This is a list item\n\n"
            "    <table><tr><td>Hello</td><td>World</td></tr></table>\n\n"
            "*   This is another list item",
            "<ul>\n<li><p>This is a list item</p>\n"
            "<table><tr><td>Hello</td><td>World</td></tr></table>\n\n</li>\n"
            "<li><p>This is another list item</p>\n</li>\n</ul>",
        ),
        # Test that smart quotes and dashes are applied.
        ("Isn't it delightful -- she said", "<p>Isn’t it delightful – she said</p>"),
        (
            "## Isn't it delightful?",
            '<h2 id="isn-t-it-delightful">Isn’t it delightful?</h2>',
        ),
        (
            "* Isn't it delightful?",
            "<ul>\n<li>Isn’t it delightful?</li>\n</ul>",
        ),
        (
            "look for any `<img>` tags",
            "<p>look for any <code>&lt;img&gt;</code> tags</p>",
        ),
        ('"It looks lovely", she said', "<p>“It looks lovely”, she said</p>"),
        # Test that contents inside <style> tags is left as-is.
        (
            "<style>p { color: red; }\n\nspan { color: blue; }</style>\n\nhello world",
            "<style>p { color: red; }\n\nspan { color: blue; }</style>\n\n"
            "<p>hello world</p>",
        ),
    ],
)
def test_markdownify(md: str, expected: str) -> None:
    """
    Test markdownify().
    """
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
    "md",
    [
        (
            "<style>\n"
            "  p { color: red; }\n"
            "\n"
            "  @media (prefers-color-scheme: dark) {\n"
            "    p { color: yellow; }\n"
            "\n"
            "    span { color: green; }\n"
            "\n"
            "    div { color: blue; }\n"
            "  }"
            "</style>"
        ),
        (
            "<figure>\n"
            '  <svg xmlns="http://www.w3.org/2000/svg">\n'
            "    <defs>\n"
            '      <symbol id="truchetSquare">…</symbol>\n'
            "\n"
            '      <symbol id="truchetSquare90">…</symbol>\n'
            "\n"
            '      <symbol id="truchetSquare180">…</symbol>\n'
            "    </defs>\n"
            "  </svg>\n"
            "</figure>"
        ),
        (
            '<svg aria-labelledby="svg_example" role="img" viewBox="0 0 200 200" '
            'xmlns="http://www.w3.org/2000/svg">'
            '<title id="svg_example">Figure with nested svg tags</title>\n'
            '<svg x="10" y="10">\n<text x="10" y="10">some text</text>\n</svg>\n'
            '<text x="10" y="10">more text</text>\n'
            '<svg x="20" y="20">\n<text x="20" y="20">some text</text>\n</svg>\n'
            '<text x="20" y="20">more text</text>\n</svg>'
        ),
        (
            '<svg aria-labelledby="svg_example" role="img" viewBox="0 0 200 200" '
            'xmlns="http://www.w3.org/2000/svg">'
            '<title id="svg_example">Figure with nested svg tags</title>\n'
            '<svg x="10" y="10">\n'
            '  <svg x="10" y="10">\n'
            '    <text x="10" y="10">some text</text>\n'
            "  </svg>\n"
            "</svg>\n"
            '<text x="10" y="10">more text</text>\n'
            '<svg x="20" y="20">\n<text x="20" y="20">some text</text>\n</svg>\n'
            '<text x="20" y="20">more text</text>\n</svg>'
        ),
    ],
)
def test_block_elements_are_preserved(md: str) -> None:
    """
    Block elements like <style> and <figure> are preserved in the
    final file, even if they have whitespace that could be interpreted
    as paragraph breaks or indented code blocks.
    """
    assert md == t.markdownify(md)
