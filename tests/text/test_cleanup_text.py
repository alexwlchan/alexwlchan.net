"""
Tests for `mosaic.text.cleanup_text`.
"""

import pytest

from mosaic import text as t


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
        ("A.B. Charles", "A.B.&nbsp;Charles"),
        (
            "<h1>LaTeX</h1>",
            "<h1>"
            '<link href="css/components/latex.css" rel="stylesheet"/>'
            '<span class="visually-hidden">LaTeK</span>'
            '<span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span>'
            "</h1>",
        ),
        (
            "<p>LaTeX is a tool</p>",
            "<p>"
            '<link href="css/components/latex.css" rel="stylesheet"/>'
            '<span class="visually-hidden">LaTeK</span>'
            '<span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span> '
            "is a tool"
            "</p>",
        ),
        (
            "LaTeX",
            '<link href="css/components/latex.css" rel="stylesheet"/>'
            '<span class="visually-hidden">LaTeK</span>'
            '<span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span>',
        ),
        # Short <code> snippets get the `nowrap` class, but only if they
        # contain a hyphen or space.
        (
            "The <code>--multiline</code> flag",
            'The <code class="nowrap">--multiline</code> flag',
        ),
        (
            "The <code>EF BB BF</code> byte order mark",
            'The <code class="nowrap">EF BB BF</code> byte order mark',
        ),
        (
            "The <code>U+FEFF</code> character",
            "The <code>U+FEFF</code> character",
        ),
        (
            "The <code>long, long text in a code</code> font",
            "The <code>long, long text in a code</code> font",
        ),
        # Check for repetitions of the same <code> element
        (
            "The <code>a b</code> flag and the <code>a b</code> flag",
            'The <code class="nowrap">a b</code> flag and the '
            '<code class="nowrap">a b</code> flag',
        ),
    ],
)
def test_cleanup_text(text: str, cleaned_text: str) -> None:
    """
    Tests for cleanup_text().
    """
    assert t.cleanup_text(text) == cleaned_text
