"""
Inline the CSS from a partial file.
"""

import base64
import glob
from io import BytesIO
import json
from pathlib import Path

from jinja2 import nodes, pass_context
from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2.runtime import Context
from PIL import Image

from mosaic.text import assert_is_invariant_under_markdown

from .pictures import render_picture
from .social_embed_models import (
    MastodonEmbed,
    MediaEntity,
    SocialEmbedData,
    TwitterEmbed,
    parse_social_embed_data,
)


class UseCSSExtension(Extension):
    """
    Defines the {% use_css %} extension.
    """

    def parse(self, parser: Parser) -> nodes.Node:
        """
        Parse the name of the component file to include.
        """
        first_token = next(parser.stream)
        assert first_token.value == "use_css", f"first token = {first_token!r}"

        lineno = first_token.lineno

        # Capture the next token as a string (the name of the CSS file)
        filename_token = next(parser.stream)
        filename = nodes.Const(filename_token.value)

        # Call the helper method to turn the URL into HTML
        call = self.call_method("_render_social", [url], lineno=lineno)

        # Return an Output node so it prints to the page
        return nodes.Output([call], lineno=lineno)

    @pass_context
    def _render_css(self, context: Context, filename: str) -> str:
        """
        Render the <style> tag for this CSS filename.
        """
        css_dir = Path("css")
        css_path = css_dir / filename
        return "<style>" + css_path.read_text() + "</style>"
