"""
Template to show updates at the bottom of a post.
"""

from datetime import datetime

from jinja2 import nodes, pass_context
from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2.runtime import Context, Macro

from mosaic.text import assert_is_invariant_under_markdown, markdownify


class UpdateExtension(Extension):
    """
    Defines the {% update %} extension.
    """

    tags = {"update"}

    def parse(self, parser: Parser) -> nodes.Node:
        """
        Parse a date and an update.
        """
        lineno = next(parser.stream).lineno

        # 1. Parse the 'date="2026-01-20"' argument
        kwargs = []
        while parser.stream.current.type != "block_end":
            target = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            kwargs.append(nodes.Keyword(target.name, value))

        # 2. Capture everything until {% endupdate %}
        body = parser.parse_statements(("name:endupdate",), drop_needle=True)

        # 3. Call our helper method _render_update
        return nodes.CallBlock(
            self.call_method("_render_update", kwargs=kwargs), [], [], body
        ).set_lineno(lineno)

    @pass_context
    def _render_update(self, context: Context, caller: Macro, date: str) -> str:
        """
        Render the update.
        """
        env = context.environment

        timestamp_template = env.get_template("partials/timestamp.html")
        update_template = env.get_template("partials/update.html")

        date_obj = datetime.strptime(date, "%Y-%m-%d")
        timestamp = timestamp_template.render(date=date_obj)

        md = caller().strip()

        html = update_template.render(
            date=date_obj,
            text=markdownify(f"<strong>Update, {timestamp}:</strong> {md}"),
        )

        assert_is_invariant_under_markdown(html)
        return html
