"""
Add a table of contents when you insert {% table_of_contents %}.
"""

from jinja2 import nodes, pass_context
from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2.runtime import Context, Macro

from mosaic.text import assert_is_invariant_under_markdown, parse_html_headings


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

        html = template.render(headings=parse_html_headings(page.content))
        assert_is_invariant_under_markdown(html)
        return html
