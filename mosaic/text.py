"""
Utilities for dealing with text.
"""

import collections
import functools
import json
import re
from typing import Any, Match

import minify_html
import mistune
from mistune.core import BlockState
import smartypants

from .syntax_highlighting import apply_syntax_highlighting


STRIP_HTML_RE = re.compile(r"<[^<]+?>")


def strip_html(text: str) -> str:
    """
    Remove all the HTML tags from a string.

    Note: this uses a regex which is probably not safe against untrusted
    input, but should be fine for my site.
    """
    return STRIP_HTML_RE.sub("", text)


def smartify(text: str) -> str:
    """
    Add curly quotes and smart dashes to a string.
    """
    # Undo some escaping from Mistune.
    text = text.replace("&quot;", '"')

    attrs = (
        # normal quotes (" and ') to curly ones
        smartypants.Attr.q
        |
        # typewriter dashes (--) to en-dashes and dashes (---) to em-dashes
        smartypants.Attr.D
        |
        # dashes (...) to ellipses
        smartypants.Attr.e
        |
        # output Unicode chars instead of numeric character references
        smartypants.Attr.u
    )

    return smartypants.smartypants(text, attrs)


class AlexwlchanRenderer(mistune.HTMLRenderer):
    """
    A custom mistune HTMLRenderer with a couple of options and settings
    for my preferred Markdown setup.
    """

    def __init__(self) -> None:
        """
        Create the renderer.

        Options:
            - escape=False means the renderer won't escape all HTML tags,
              so I can use HTML inline with my Markdown.
        """
        super().__init__(escape=False)

    def block_code(self, code: str, info: str | None = None) -> str:
        """
        Create a code block with optional name highlighting.
        """
        if info is None:
            info = ""
        parts = info.split(" ", 1)

        attrs: dict[str, Any]
        if not info.strip():
            lang, attrs = "text", {}
        elif len(parts) == 1:
            lang, attrs = parts[0], {}
        else:
            lang, attrs = parts[0], json.loads(parts[1])

        if "names" in attrs:
            attrs["names"] = {int(idx): name for idx, name in attrs["names"].items()}

        return apply_syntax_highlighting(code, lang, **attrs)

    def heading(self, text: str, level: int, **attrs: Any) -> str:
        """
        Create a heading which includes an `id` attribute.
        """
        assert attrs == {}, attrs

        tag = f"h{level}"
        heading_id = re.sub(r"[^\w]+", "-", text.lower()).strip("-")

        text = smartify(text)

        return f'<{tag} id="{heading_id}">{text}</{tag}>\n'

    def paragraph(self, text: str) -> str:
        """
        Create a paragraph with curly quotes and smart dashes.
        """
        return super().paragraph(text=smartify(text))

    def list_item(self, text: str) -> str:
        """
        Create a list item with curly quotes and smart dashes.
        """
        return super().list_item(text=smartify(text))


class MosaicBlockParser(mistune.BlockParser):
    """
    Overrides the default block parser so it considers more tags to
    be pre tags (treat contents as-is, don't parse as Markdown).

    The default implementation only considers pre, script, style, and
    textarea to be exempt from Markdown parsing.
    """

    def parse_raw_html(self, m: Match[str], state: BlockState) -> int | None:
        """
        Overrides the parent method of the same name, with extra cases
        for elements I use.
        """
        from mistune.block_parser import _parse_html_to_end

        marker = m.group(0).strip()
        open_tag = marker[1:].lower()

        # These are not all pre tags in the strictest sense, but any
        # time you see one in my source Markdown, I can assume everything
        # until the closing tag is pure HTML and doesn't need the Markdown
        # library to interfere.
        PRE_TAGS = ["figure", "picture", "blockquote", "ol", "ul", "div", "details"]

        if open_tag in PRE_TAGS:
            end_tag = "</" + open_tag + ">"
            return _parse_html_to_end(state, end_tag, m.end())

        return super().parse_raw_html(m, state)


markdown = mistune.Markdown(renderer=AlexwlchanRenderer(), block=MosaicBlockParser())


@functools.cache
def markdownify(text: str) -> str:
    """
    Format text using Markdown.
    """
    html = markdown(text)
    assert isinstance(html, str), f"unexpected type: {type(html)}"
    return html.strip()


def markdownify_oneline(text: str) -> str:
    """
    Format a single line of text using Markdown, but without <p> tags.
    """
    return markdownify(text).replace("<p>", "").replace("</p>", "").strip()


def cleanup_text(text: str) -> str:
    """
    Apply all my cleanup rules to text.
    """
    text = add_non_breaking_characters(text)
    text = add_latex_css_classes(text)
    text = force_text_footnote_markers(text)
    return text.strip()


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

PROPER_NAME_RE = re.compile(r"(?P<initials>[A-Z]\.[A-Z]\.) (?P<surname>[A-Z])")


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

    return text


def add_latex_css_classes(html: str) -> str:
    """
    Make the words TeX and LaTeX display nicely in my HTML.
    """
    html = html.replace(
        " LaTeX",
        ' <style type="x-text/scss">@use "components/latex";</style> '
        '<span class="visually-hidden">LaTeK</span>'
        '<span class="latex" aria-hidden="true">L<sup>a</sup>T<sub>e</sub>X</span>',
    )

    html = html.replace(
        " TeX",
        ' <style type="x-text/scss">@use "components/latex";</style> '
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


def assert_is_invariant_under_markdown(html: str) -> None:
    """
    Check if an HTML string is unmodified by Markdown.

    This is to catch edge cases where an attribute on a Jinja2 tag
    is incorrectly interpreted as Markdown, e.g. arrows (~>) in alt text.
    """
    markdownified = markdownify(html)

    # The Markdown plugin adds leading/trailing <p> tags; remove them
    # before doing the comparison.
    if (
        '<blockquote class="update"' not in html
        and '<figure class="slide">' not in html
    ):
        markdownified = markdownified.replace("<p>", "", 1)
        markdownified = re.sub(r"</p>$", "", markdownified)

    assert minify_html.minify(markdownified) == minify_html.minify(html), (
        minify_html.minify(markdownified),
        minify_html.minify(html),
    )


def find_unique_prefixes(strings: set[str]) -> dict[str, str]:
    """
    Given a collection of strings, find the shortest abbreviation that
    uniquely identifies each string in this collection.

    Example:
        >>> find_shortest_abbreviations(["amber", "application", "banana"])
        {"amber": "am", "application": "ap", "banana": "b"}

    """
    # Start by calculating all the prefixes for every string,
    # for example "amber" gives us ["a", "am", "amb", "ambe", "amber"]
    all_prefixes = collections.defaultdict(list)

    for s in strings:
        for i in range(1, len(s) + 1):
            all_prefixes[s[:i]].append(s)

    # Delete all prefixes which point to multiple words, so we're left
    # with unique prefixes
    unique_prefixes = {
        prefix: words for prefix, words in all_prefixes.items() if len(words) == 1
    }

    # Invert the map, so now we know all the candidate prefixes for each word
    candidate_prefixes = collections.defaultdict(list)

    for prefix, words in unique_prefixes.items():
        candidate_prefixes[words[0]].append(prefix)

    # Choose the shortest candidate prefix for each word.
    result = {
        word: min(prefixes, key=len) for word, prefixes in candidate_prefixes.items()
    }

    # Check that no keys were lost in the transformation, which can occur
    # if one string was a prefix of the other.
    assert result.keys() == strings, strings - set(result.keys())

    return result
