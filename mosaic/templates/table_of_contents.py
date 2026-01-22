"""
Add a table of contents when you insert {% table_of_contents %}.
"""

from typing import TypedDict

from bs4 import BeautifulSoup
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


def parse_toc_entries(md: str) -> list[TocEntry]:
    """
    Extract all the headings from a Markdown document.
    """
    html = markdownify(md)
    soup = BeautifulSoup(html, "html.parser")

    result: list[TocEntry] = []

    for heading_tag in soup.find_all(["h2", "h3"]):
        heading_id = heading_tag.attrs["id"]
        assert isinstance(heading_id, str)

        if heading_tag.name == "h2":
            result.append(
                {
                    "id": heading_id,
                    "label": heading_tag.text,
                    "sub_headings": [],
                }
            )
        else:
            result[-1]["sub_headings"].append(
                {"id": heading_id, "label": heading_tag.text}
            )

    return result
