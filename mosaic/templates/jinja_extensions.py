"""
Helper classes for Jinja extensions.
"""

from abc import ABC, abstractmethod
from typing import Any

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.parser import Parser


class KwargsExtensionBase(ABC, Extension):
    """
    KwargsExtensionBase is for Jinja tags that take keyword arguments,
    e.g. picture or inline_svg.
    """

    @abstractmethod
    def render_html(self, **kwargs: dict[str, Any]) -> str:
        """
        Render the HTML for this extension. Subclasses should override this.
        """

    @property
    def tag_name(self) -> str:
        """
        Returns the name of the Jinja tag. This is derived from `tags`.
        """
        assert len(self.tags) == 1, self.tags
        return list(self.tags)[0]

    def parse(self, parser: Parser) -> nodes.Node:
        """
        Parse a Jinja tag that takes keyword arguments.
        """
        # The first token should be the name of the tag, e.g. "picture"
        first_token = next(parser.stream)
        assert first_token.value == self.tag_name, (
            f"first token = {first_token!r}, tag name = {self.tag_name}"
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
            self.call_method("render_html", kwargs=kwargs), [], [], []
        ).set_lineno(first_token.lineno)
