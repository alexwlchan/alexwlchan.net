"""
Functions for rendering and manipulating HTML.
"""

from html.parser import HTMLParser
from typing import TypeAlias, TypedDict

import minify_html as minify_html_lib


__all__ = ["minify_html", "parse_html_headings"]


def minify_html(html: str) -> str:
    """
    Minify an HTML string.
    """
    return minify_html_lib.minify(
        html,
        keep_html_and_head_opening_tags=True,
        keep_closing_tags=True,
        minify_css=True,
        minify_js=True,
    )


class Subheading(TypedDict):
    """A sub-heading in an HTML document."""

    id: str
    label: str


class Heading(TypedDict):
    """A top-level heading in an HTML document."""

    id: str
    label: str
    sub_headings: list[Subheading]


HTMLAttrs: TypeAlias = list[tuple[str, str | None]]


class HeadingParser(HTMLParser):
    """
    An HTML parser that looks for heading tags (<h2> and <h3>).
    """

    def __init__(self) -> None:
        super().__init__()
        self.result: list[Heading] = []
        self.last_seen_tag: str | None = None
        self.last_seen_id: str | None = None
        self.accumulator: list[str] = []

    def handle_starttag(self, tag: str, attrs: HTMLAttrs) -> None:
        """
        If this is an opening heading tag, record the heading level and ID
        and start a new state.
        """
        if tag in {"h2", "h3"}:
            attr_dict = dict(attrs)
            self.last_seen_tag = tag
            self.last_seen_id = attr_dict["id"]
            assert isinstance(self.last_seen_id, str)
            self.accumulator = []

    def handle_data(self, data: str) -> None:
        """
        If we're in the middle of a heading tag, add the data we've
        received to the accumulator.
        """
        if self.last_seen_tag:
            self.accumulator.append(data)

    def handle_endtag(self, tag: str) -> None:
        """
        If this is a closing heading tag, process all the data we've
        received until this point, append the result, then reset the state.
        """
        if tag == self.last_seen_tag:
            label = "".join(self.accumulator).strip()
            heading_id = self.last_seen_id
            assert isinstance(heading_id, str)

            if tag == "h2":
                self.result.append(
                    {"id": heading_id, "label": label, "sub_headings": []}
                )
            elif tag == "h3":
                self.result[-1]["sub_headings"].append(
                    {"id": heading_id, "label": label}
                )
            else:  # pragma: no cover
                assert 0, "unreachable"

            self.last_seen_tag = None
            self.last_seen_id = None


def parse_html_headings(md: str) -> list[Heading]:
    """
    Extract all the headings from a Markdown document.
    """
    from .markdown import markdownify

    html = markdownify(md)
    parser = HeadingParser()
    parser.feed(html)
    return parser.result
