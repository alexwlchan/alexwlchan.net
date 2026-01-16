"""
Code for dealing with HTML and XML templates.
"""

import re

from markdown import markdown


def markdownify(text: str) -> str:
    """
    Format text using Markdown.
    """
    return markdown(text, extensions=["codehilite", "fenced_code", "smarty"])


def markdownify_oneline(text: str) -> str:
    """
    Format a single line of text using Markdown, but without <p> tags.
    """
    return markdownify(text).replace("<p>", "").replace("</p>", "")


def cleanup_text(text: str) -> str:
    """
    Apply all my cleanup rules to text.
    """
    text = add_non_breaking_characters(text)
    text = add_latex_css_classes(text)
    text = force_text_footnote_markers(text)
    return text


# Words which often appear before a number
PREFIX_WORDS = [
    "Apollo",
    "Artemis",
    "chapter",
    "HTTP",
    "ImageMagick",
    "ISO/IEC",
    "Issue",
    "issue",
    "iPres",
    "Mr.",
    "Mrs.",
    "No.",
    "Part",
    "part",
    "Python",
    "RFC",
    "Safari",
    "Season",
    "season",
    "SQLite",
]

# Construct a regex like `(issue|part|season) (\d+)`.
PREFIX_RE = re.compile("(" + "|".join(PREFIX_WORDS) + r") (\d+)")

# Words which can be counted, which often follow a number
COUNTABLE_WORDS = [
    "bookmark",
    "byte",
    "character",
    "count",
    "GB",
    "GiB",
    "hour",
    "inch",
    "kilometre",
    "line",
    "MiB",
    "million",
    "minute",
    "second",
    "tags",
    "unit",
    "vote",
    "year",
]

# Construct a regex like `(\d+) (byte|hour|inch)`
COUNTABLE_RE = re.compile(r"(\d+) (" + "|".join(COUNTABLE_WORDS) + ")")

NON_BREAKING_PHRASES = [
    "<em>k</em>-means",
    "26k items",
    "Algorithm L",
    "Algorithm R",
    "Amazon S3",
    "Apple TV+",
    "CC0 1.0",
    "CC BY 2.0",
    "CC BY 3.0",
    "CC BY 4.0",
    "CC BY-NC 2.0",
    "CC BY-NC 4.0",
    "CC BY-ND 2.0",
    "CC BY-NC-ND",
    "CC BY-SA 2.0",
    "CC BY-SA 3.0",
    "CC BY-SA 4.0",
    "CC BY-NC-SA 4.0",
    "CC BY",
    "C.S. Lewis",
    "DjangoCon US",
    "Dr. Drang",
    "ECMA-404",
    "e.g. ",
    "Face ID",
    "Git LFS",
    "HTTP 200 OK",
    "iMac G3",
    "iPhone X",
    "IP address",
    "JPEG 2000",
    "Latin-1",
    "Mac OS 9",
    "Mac OS X",
    "Monki Gras",
    "MS Paint",
    "Objective-C",
    "P-215",
    "PDF 1.6",
    "PDF 1.7",
    "PyCon ",
    "Route 53",
    "Silo 49",
    "System 1",
    "Touch ID",
    "VS Code",
    "Windows-1252",
    "z-axis",
]


def add_non_breaking_characters(text: str) -> str:
    """
    Add non-breaking spaces and characters to my text.

    See https://alexwlchan.net/2020/adding-non-breaking-spaces-with-jekyll/
    """
    # Add a non-breaking space after words which are followed by a number,
    # like "part 5" or "issue 123".
    text = PREFIX_RE.sub(r"\1&nbsp;\2", text)

    # Add a non-breaking space before words which are preceded by a number,
    # like "1 byte" or "4 inches".
    text = COUNTABLE_RE.sub(r"\1&nbsp;\2", text)

    # Add a non-breaking space after words if they're the first word
    # in a sentence.
    short_words = ["A", "An", "I"]

    for w in short_words:
        text = text.replace(f". {w} ", f". {w}&nbsp;")
        text = text.replace(f".\n{w} ", f".\n{w}&nbsp;")

    # Handle other phrases which need non-breaking spaces or dashes.
    for phrase in NON_BREAKING_PHRASES:
        if phrase not in text:
            continue

        replacement = phrase.replace(" ", "&nbsp;").replace("-", "&#8209;")
        text = text.replace(phrase, replacement)

    return text


def add_latex_css_classes(html: str) -> str:
    """
    Make the words TeX and LaTeX display nicely in my HTML.
    """
    html = html.replace(
        " LaTeX",
        '<style type="x-text/scss">@use "components/latex";</style> '
        '<span class="visually-hidden">LaTeK</span>'
        '<span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span>',
    )

    html = html.replace(
        " TeX",
        '<style type="x-text/scss">@use "components/latex";</style> '
        '<span class="visually-hidden">TeK</span>'
        '<span class="latex" aria-hidden="true">T<sub>e</sub>X</span>',
    )

    return html


def force_text_footnote_markers(html: str) -> str:
    """
    Force footnote markers to render as text on iOS devices, not emoji.
    """
    # See https://mts.io/2015/04/21/unicode-symbol-render-text-emoji/
    return html.replace("&#8617;", "&#8617;&#xFE0E;").replace("↩", "&#8617;&#xFE0E;")
