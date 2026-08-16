"""
Convert Markdown-formatted text to HTML.
"""

import json
import re
from typing import Any, Match

from chives.text import smartify
import mistune
from mistune.core import BlockState

from mosaic import cache
from .syntax_highlighting import apply_syntax_highlighting


__all__ = ["assert_is_invariant_under_markdown", "markdownify", "markdownify_oneline"]


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

        if isinstance(attrs.get("names"), dict):
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
    Override the default block parser so it considers more tags to
    be pre tags (treat contents as-is, don't parse as Markdown).

    The default implementation only considers pre, script, style, and
    textarea to be exempt from Markdown parsing.
    """

    def parse_raw_html(self, m: Match[str], state: BlockState) -> int | None:
        """
        Override the parent method of the same name, with extra cases
        for elements I use.
        """
        from mistune.block_parser import _parse_html_to_end

        marker = m.group(0).strip()
        open_tag = marker[1:].lower()

        # These are not all pre tags in the strictest sense, but any
        # time you see one in my source Markdown, I can assume everything
        # until the closing tag is pure HTML and doesn't need the Markdown
        # library to interfere.
        PRE_TAGS = [
            "figure",
            "picture",
            "blockquote",
            "ol",
            "ul",
            "div",
        ]

        if open_tag == "svg":
            return _parse_to_end_of_svg(state, m.end())

        elif open_tag in PRE_TAGS:
            end_tag = "</" + open_tag + ">"
            return _parse_html_to_end(state, end_tag, m.end())

        return super().parse_raw_html(m, state)


def _parse_to_end_of_svg(state: BlockState, start_pos: int) -> int:
    """
    Parse to the end of the current <svg> tag, noting that <svg> tags
    can be nested within each other.
    """
    if "</svg>" not in state.src[start_pos:]:  # pragma: no cover
        raise ValueError(f"no closing </svg> found in HTML: {state.src}")

    # Find all instances of a closing </svg> tag, then pick the first one
    # where we have balanced opening/closing tags -- that means we've
    # correctly skipped over all the nested <svg> tags.
    candidates = [m.end() for m in re.finditer("</svg>", state.src[start_pos:])]

    for c in candidates:
        marker_pos = start_pos + c
        text = state.src[state.cursor : marker_pos]
        if text.count("<svg") == text.count("</svg>"):
            break
    else:  # no break  # pragma: no cover
        raise ValueError("<svg> tags not balanced")

    state.cursor = marker_pos
    end_pos = state.find_line_end()
    text += state.get_text(end_pos)

    state.append_token({"type": "block_html", "raw": text})
    return end_pos


markdown = mistune.Markdown(renderer=AlexwlchanRenderer(), block=MosaicBlockParser())


def markdownify(text: str) -> str:
    """
    Format text using Markdown.
    """
    cache_ns = "markdownify"
    cache_key = cache.md5(text)

    if cached_html := cache.get(cache_ns, cache_key):
        return cached_html

    html = markdown(text)
    assert isinstance(html, str), f"unexpected type: {type(html)}"
    html = html.strip()

    cache.set(cache_ns, cache_key, html)

    return html


def markdownify_oneline(text: str) -> str:
    """
    Format a single line of text using Markdown, but without <p> tags.
    """
    return markdownify(text).replace("<p>", "").replace("</p>", "").strip()


def assert_is_invariant_under_markdown(html: str) -> None:
    """
    Check if an HTML string is unmodified by Markdown.

    This is to catch edge cases where an attribute on a Jinja2 tag
    is incorrectly interpreted as Markdown, e.g. arrows (~>) in alt text.
    """
    from .html import minify_html

    markdownified = markdownify(html)

    # The Markdown plugin adds leading/trailing <p> tags; remove them
    # before doing the comparison.
    if (
        '<aside class="update"' not in html
        and '<figure class="slide">' not in html
        and not html.startswith("<svg")
    ):
        markdownified = markdownified.replace("<p>", "", 1)
        markdownified = re.sub(r"</p>$", "", markdownified)

    assert minify_html(markdownified) == minify_html(html), (
        minify_html(markdownified),
        minify_html(html),
    )
