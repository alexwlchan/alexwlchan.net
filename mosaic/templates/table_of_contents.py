"""
Add a table of contents when you insert {% table_of_contents %}.
"""

from html.parser import HTMLParser
from typing import TypeAlias, TypedDict

from jinja2 import nodes, pass_context
from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2.runtime import Context, Macro

from mosaic.text import assert_is_invariant_under_markdown, markdownify


class TableOfContentsExtension(Extension):
    """
    Defines the {% table_of_contents %} tag.
    """

    tags = {"table_of_contents"}

    def parse(self, parser: Parser) -> nodes.Node:
        """
        Parse the tag, which doesn't take any arguments.
        """
        lineno = next(parser.stream).lineno
        return nodes.CallBlock(self.call_method("_render_toc"), [], [], "").set_lineno(
            lineno
        )

    @pass_context
    def _render_toc(self, context: Context, caller: Macro) -> str:
        """
        Render the table of contents.
        """
        env = context.environment
        page = context["page"]

        template = env.get_template("partials/table_of_contents.html")

        html = template.render(toc_entries=parse_toc_entries(page.content))
        assert_is_invariant_under_markdown(html)
        return html


Subheading = TypedDict("Subheading", {"id": str, "label": str})
TocEntry = TypedDict(
    "TocEntry", {"id": str, "label": str, "sub_headings": list[Subheading]}
)

HTMLAttrs: TypeAlias = list[tuple[str, str | None]]


class TocParser(HTMLParser):
    """
    An HTML parser that looks for heading tags and builds a list of
    TocEntries.
    """

    def __init__(self) -> None:
        super().__init__()
        self.result: list[TocEntry] = []
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


def parse_toc_entries(md: str) -> list[TocEntry]:
    """
    Extract all the headings from a Markdown document.
    """
    html = markdownify(md)
    parser = TocParser()
    parser.feed(html)
    return parser.result
