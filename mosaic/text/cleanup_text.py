"""
Utilities for dealing with text.
"""

import os
import re


from mosaic import cache


__all__ = ["cleanup_text"]


# Use the mtime of this file as part of the cache key, to ensure that
# when the definitions in this file change, the calues are recalculated
CLEANUP_TEXT_CACHE_ID = str(os.stat(__file__).st_mtime)


def cleanup_text(text: str) -> str:
    """
    Apply all my cleanup rules to text.
    """
    cache_ns = "cleanup_text"
    cache_key = f"{CLEANUP_TEXT_CACHE_ID}:{cache.md5(text)}"

    if value := cache.get(cache_ns, cache_key):
        return value

    text = add_non_breaking_characters(text)
    text = add_latex_css_classes(text)
    text = force_text_footnote_markers(text)
    text = text.strip()

    cache.set(cache_ns, cache_key, text)
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
    "Thunderbolt",
    "Xcode",
]

# Construct a regex like `(issue|part|season) (\d+)`.
PREFIX_RE = re.compile("(" + "|".join(PREFIX_WORDS) + r") (\d+)")

# Words which can be counted, which often follow a number
COUNTABLE_WORDS = [
    "AD",
    "BC",
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
    "millisecond",
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
    "200 OK",
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
    "Flickr API",
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
    "New York",
    "Objective-C",
    "P-215",
    "PDF 1.6",
    "PDF 1.7",
    "PyCon ",
    "Route 53",
    "Silo 49",
    "System 1",
    "Touch ID",
    "UTF-8",
    "UTF-16",
    "UTF-32",
    "VS Code",
    "Windows-1252",
    "z-axis",
]

PROPER_NAME_RE = re.compile(r"(?P<initials>[A-Z]\.[A-Z]\.) (?P<surname>[A-Z])")

# CODE_FLAG_RE matches <code> snippets that are short.
#
# The limit of 15 characters is arbitrary. In longer code snippets,
# wrapping is preferable to avoid leaving excessive whitespace on
# the previous line.
CODE_FLAG_RE = re.compile(r"<code>(?P<contents>[^<]{1,15})</code>")


def add_nowrap(match: re.Match[str]) -> str:
    """
    Add the `nowrap` class to a `<code>` element if it contains line
    breaking characters.
    """
    contents = match.group("contents")
    if "-" in contents or " " in contents:
        return f'<code class="nowrap">{contents}</code>'
    return match.group(0)


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

    # Add a non-breaking space in phrases that look like names.
    text = PROPER_NAME_RE.sub(r"\g<initials>&nbsp;\g<surname>", text)

    # Handle other phrases which need non-breaking spaces or dashes.
    for phrase in NON_BREAKING_PHRASES:
        if phrase not in text:
            continue

        replacement = phrase.replace(" ", "&nbsp;").replace("-", "&#8209;")
        text = text.replace(phrase, replacement)

    # Add a `nowrap` class to short <code> snippets which contain
    # potential line-break characters, so they don't wrap.
    text = CODE_FLAG_RE.sub(add_nowrap, text)

    return text


def add_latex_css_classes(html: str) -> str:
    """
    Make the words TeX and LaTeX display nicely in my HTML.
    """
    latex_css = '<link href="css/components/latex.css" rel="stylesheet"/>'
    latex_hidden = '<span class="visually-hidden">LaTeK</span>'
    latex_visual = (
        '<span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span>'
    )

    if html == "LaTeX":
        return f"{latex_css}{latex_hidden}{latex_visual}"

    html = html.replace(
        " LaTeX",
        f"{latex_css}{latex_hidden} {latex_visual}",
    )
    html = html.replace(">LaTeX<", f">{latex_css}{latex_hidden}{latex_visual}<")
    html = html.replace(">LaTeX ", f">{latex_css}{latex_hidden}{latex_visual} ")

    html = html.replace(
        " TeX",
        latex_css + '<span class="visually-hidden">TeK</span>'
        ' <span class="latex" aria-hidden="true">T<sub>e</sub>X</span>',
    )

    return html


def force_text_footnote_markers(html: str) -> str:
    """
    Force footnote markers to render as text on iOS devices, not emoji.
    """
    # See https://mts.io/2015/04/21/unicode-symbol-render-text-emoji/
    return html.replace("&#8617;", "&#8617;&#xFE0E;").replace("↩", "&#8617;&#xFE0E;")
