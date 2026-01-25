"""
The legacy {% code %} tag from Jekyll, which I'm phasing out in favour
of fenced code blocks.
"""

from typing import Any

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2.runtime import Macro

from mosaic.syntax_highlighting import apply_syntax_highlighting


class CodeBlockExtension(Extension):
    """
    Implements the {% code %} tag.
    """

    tags = {"code"}

    def parse(self, parser: Parser) -> nodes.Node:
        """
        Parse an instance of the {% code %} tag.
        """
        lineno = next(parser.stream).lineno

        kwargs = []
        while parser.stream.current.type != "block_end":
            target = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            kwargs.append(nodes.Keyword(target.name, value))

        body = parser.parse_statements(("name:endcode",), drop_needle=True)

        return nodes.CallBlock(
            self.call_method("_render_code", kwargs=kwargs), [], [], body
        ).set_lineno(lineno)

    def _render_code(self, caller: Macro, lang: str = "text", **kwargs: Any) -> str:
        """
        Render a block of code as HTML.
        """
        return apply_syntax_highlighting(src=caller().strip(), lang=lang)
