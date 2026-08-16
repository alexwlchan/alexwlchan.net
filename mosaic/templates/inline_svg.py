"""
Inline the contents of an SVG from a separate file.

I inline small SVG images (anything ~1 KB or less) to reduce the overhead
of extra HTTP requests.  I don't inline them directly in the Markdown source
because they're easier to write if they're kept in separate files.

Example usage:

    {%
      inline_svg
      filename="sqs_queue_worker.svg"
      alt="Three boxes joined by arrows"
    %}

References:
  - Accessible SVGs https://css-tricks.com/accessible-svgs/
    Explains how to ensure accessibility is preserved with inline SVGs.

  - sdumetz/jekyll-inline-svg https://github.com/sdumetz/jekyll-inline-svg
    Jekyll plugin for doing something similar.

"""

from typing import Any

from jinja2 import pass_context
from jinja2.runtime import Context

from mosaic.images import render_inline_svg
from mosaic.text import assert_is_invariant_under_markdown

from .jinja_extensions import KwargsExtensionBase


class InlineSvgExtension(KwargsExtensionBase):
    """
    Defines the {% inline_svg %} tag to render inline SVGs.
    """

    tags = {"inline_svg"}

    @pass_context
    def render_html(self, context: Context, *args: Any, **kwargs: Any) -> str:
        """
        Render the inline_svg tag.
        """
        assert not args, "only pass keyword arguments"

        # Discard the caller argument sent by Jinja2, which I don't use.
        kwargs.pop("caller")

        # Work out where this inline SVG will be saved. Look in the per-date
        # folder if this is a dated post, or the images dir if not.
        src_dir = context["src_dir"]
        out_dir = context["out_dir"]
        images_dir = src_dir / "images"

        filename = kwargs.pop("filename")
        if context["page"].date:
            src_path = images_dir / str(context["page"].date.year) / filename
        else:
            src_path = images_dir / filename

        html = render_inline_svg(
            src_dir=src_dir,
            src_path=src_path,
            out_dir=out_dir,
            **kwargs,
        )
        assert_is_invariant_under_markdown(html)
        return html
