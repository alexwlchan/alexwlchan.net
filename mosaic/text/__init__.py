"""
Utilities for dealing with text.
"""

import collections

from .cleanup_text import cleanup_text
from .html import fix_html_for_feed_readers, minify_html, parse_html_headings
from .markdown import (
    assert_is_invariant_under_markdown,
    markdownify,
    markdownify_oneline,
)
from .syntax_highlighting import apply_syntax_highlighting

__all__ = [
    "apply_syntax_highlighting",
    "assert_is_invariant_under_markdown",
    "cleanup_text",
    "find_unique_prefixes",
    "fix_html_for_feed_readers",
    "markdownify",
    "markdownify_oneline",
    "minify_html",
    "parse_html_headings",
]


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
    candidate_prefixes = collections.defaultdict(list[str])

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
