"""
Some utility code for creating Jinja extensions.
"""

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.parser import Parser


class KwargsExtensionBase(Extension):
    """
    KwargsExtensionBase is for Jinja tags that take keyword arguments,
    e.g. picture or inline_svg.
    """

    def _parse_kwargs(self, parser: Parser, tag_name: str, render_method: str) -> str:
        """
        Run the parsing for a Jinja tag which takes keyword arguments,
        e.g. picture or inline_svg.
        """
        # The first token should be the name of the tag, e.g. "picture"
        first_token = next(parser.stream)
        assert first_token.value == tag_name, (
            f"first token = {first_token!r}, tag name = {tag_name}"
        )

        # Parse the keyword arguments
        kwargs: list[nodes.Keyword] = []
        while parser.stream.current.type != "block_end":
            # Handle the '=' sign between key and value
            target = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            kwargs.append(nodes.Keyword(target.name, value))

        return nodes.CallBlock(
            self.call_method(render_method, kwargs=kwargs), [], [], []
        ).set_lineno(first_token.lineno)
