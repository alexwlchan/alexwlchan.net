"""
A compatibility extension that lets Jinja2 ignore Liquid-style comments.

I used to write the site with the Liquid templating engine, which uses

    {% comment %} … {% endcomment %}

for comments, whereas Jinja2 uses

    {# … #}

This extension provides a temporary bridging gap so I can keep all
my existing Liquid comments, but eventually I'll migrate them to Jinja2
and delete this extension.
"""

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.parser import Parser


class LiquidCommentExtension(Extension):
    """
    An extension that deletes its contents.

    Usage:

        {% comment %}
        Nothing in here will appear on the apge
        {% endcomment %}

    """

    # The tag name to look for
    tags = {"comment"}

    def parse(self, parser: Parser) -> list[nodes.Node]:
        """Parse the token stream and return nothing."""
        # The first token is the tag name 'comment'
        next(parser.stream).lineno

        # Parse everything until we find '{% endcomment %}'.
        # 'drop_needle=True' tells Jinja to remove the 'endcomment' token
        # from the stream
        parser.parse_statements(("name:endcomment",), drop_needle=True)

        # Return an empty list of nodes, which renders as nothing.
        return []
