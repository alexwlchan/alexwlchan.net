import re
from typing import Any

from jinja2 import nodes
from jinja2.ext import Extension
from markdown import markdown

from .article_cards import article_card_image
from .book_info import BookInfoExtension
from .embeds import EmbedExtension
from .pictures import create_image_derivatives, PictureExtension
from .slides import SlideExtension
from .text import markdownify, markdownify_oneline
from .updates import UpdateExtension

__all__ = ["article_card_image", "create_image_derivatives",
"markdownify", "markdownify_oneline", "BookInfoExtension", "EmbedExtension", "PictureExtension", "SlideExtension", "UpdateExtension"]


def cleanup_text(text: str) -> str:
    """
    Apply text transformations and clean-ups.

    TODO: Implement this.
    """
    return text


def get_inline_styles(html: str) -> Any:
    return {"inline_styles": "", "html": html}


STRIP_HTML_RE = re.compile(r"<[^<]+?>")


def strip_html(text: str) -> str:
    """
    Remove all the HTML tags from a string.

    Note: this uses a regex which is probably not safe against untrusted
    input, but should be fine for my site.
    """
    return STRIP_HTML_RE.sub("", text)


class KwargsExtension(Extension):
    # This is the tag name the parser will look for
    tags = {"inline_code", "inline_svg", "download"}

    def parse(self, parser):
        # The first token is the tag name 'picture'
        lineno = next(parser.stream).lineno

        # Parse keyword arguments (key="value")
        kwargs = []
        while parser.stream.current.type != "block_end":
            # Handle the '=' sign between key and value
            target = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            kwargs.append(nodes.Keyword(target.name, value))

        # Call the helper method '_render_picture' with the parsed kwargs
        return nodes.CallBlock(
            self.call_method("_render_picture", kwargs=kwargs), [], [], []
        ).set_lineno(lineno)

    def _render_picture(self, **kwargs):
        # print(kwargs)
        return f"KWARGS {kwargs}"


class CommentExtension(Extension):
    # TODO: Replace this with Jinja2 comment syntax
    # The tag name to look for
    tags = {"comment"}

    def parse(self, parser):
        # The first token is the tag name 'comment'
        next(parser.stream).lineno

        # Parse everything until we hit '{% endcomment %}'
        # 'drop_needle=True' tells Jinja to remove the 'endcomment' token from the stream
        parser.parse_statements(["name:endcomment"], drop_needle=True)

        # Return an empty list of nodes (renders as nothing)
        return []


class CodeBlockExtension(Extension):
    tags = {"code", "update", "annotatedhighlight"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        # 1. Parse the 'lang="python"' argument
        kwargs = []
        while parser.stream.current.type != "block_end":
            target = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            kwargs.append(nodes.Keyword(target.name, value))

        # 2. Capture everything until {% endcode %}
        # We use parse_statements to get the body of the block
        body = parser.parse_statements(
            ["name:endcode", "name:endupdate", "name:endannotatedhighlight"],
            drop_needle=True,
        )

        # 3. Call our helper method _render_code
        return nodes.CallBlock(
            self.call_method("_render_code", kwargs=kwargs), [], [], body
        ).set_lineno(lineno)

    def _render_code(self, **kwargs):
        # caller() renders the body content we captured
        # content = caller()
        #
        # # Clean up leading/trailing whitespace common in block tags
        # content = content.strip()

        return f"CodeBlockExtension {kwargs}"


class TOCExtension(Extension):
    # The tag name to look for
    tags = {"table_of_contents"}

    def parse(self, parser):
        # Line number for error reporting
        lineno = next(parser.stream).lineno

        # We don't need to parse any arguments, so we just
        # tell Jinja to call the '_generate_toc' method.
        return nodes.Output([self.call_method("_generate_toc")]).set_lineno(lineno)

    def _generate_toc(self):
        # In a real scenario, you might pull this from the context
        # or a global 'headers' list.
        toc_html = """
        <nav class="toc">
            <h3>Table of Contents</h3>
            <ul>
                <li><a href="#intro">Introduction</a></li>
                <li><a href="#setup">Setup</a></li>
                <li><a href="#usage">Usage</a></li>
            </ul>
        </nav>
        """
        return toc_html
