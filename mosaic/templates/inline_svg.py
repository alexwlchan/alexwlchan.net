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

import shutil
import re
from typing import Any, Literal

from bs4 import BeautifulSoup, Comment
from jinja2 import pass_context
from jinja2.runtime import Context

from mosaic.text import assert_is_invariant_under_markdown

from .jinja_extensions import KwargsExtensionBase


class InlineSvgExtension(KwargsExtensionBase):
    """
    Defines the {% inline_svg %} tag to render inline SVGs.
    """

    tags = {"inline_svg"}

    @pass_context
    def render_html(self, *args: Any, **kwargs: Any) -> str:
        """
        Render the inline_svg tag.
        """
        html = render_inline_svg(*args, **kwargs)
        assert_is_invariant_under_markdown(html)
        return html


def render_inline_svg(
    context: Context,
    filename: str,
    alt: str | None = None,
    link_to: Literal["original"] | None = None,
    # The caller is a variable passed by Jinja2, but I don't use it
    # so I can discard it.
    caller: Any | None = None,
    **kwargs: Any,
) -> str:
    """
    Create the HTML to render an inline SVG.
    """
    src_dir = context["src_dir"]
    out_dir = context["out_dir"]

    # 1. Verify the file extension
    if not filename.endswith(".svg"):
        raise ValueError(
            f"You can only use {{% inline_svg %}} with SVG images; got {filename!r}"
        )

    # TODO: Support inline SVGs whose parent isn't a per-year directory
    year = context["page"].date.year

    # 2. Read and parse the SVG
    src_path = src_dir / "_images" / str(year) / filename

    soup = BeautifulSoup(src_path.read_text(), "xml")
    svg_tag = soup.find("svg")
    if svg_tag is None:
        raise ValueError(f"No <svg> tag found in {src_path!r}")

    # 3. Add the accessibility role. See "Accessible SVGs" §2.
    svg_tag["role"] = "img"

    # 4. If alt text, add a <title> element.
    # TODO: Are there any cases where I wouldn't have alt text?
    if alt is not None:
        svg_id = f"svg_{src_path.stem}"

        # Create a new <title> tag
        title_tag = soup.new_tag("title")
        title_tag["id"] = svg_id
        title_tag.string = alt

        # Insert the <title> at the beginning of the SVG
        svg_tag.insert(0, title_tag)
        svg_tag["aria-labelledby"] = svg_id

    # 5. Add extra attributes
    if kwargs:
        for k, v in kwargs.items():
            if k == "class":
                existing_classes = svg_tag.get("class", "")
                assert isinstance(existing_classes, str)
                svg_tag["class"] = " ".join([existing_classes, v]).strip()
            else:
                svg_tag[k] = v

    # 6. Remove comments, including any whitespace that was immediately
    # before or after.
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        for sibling in (comment.previous_sibling, comment.next_sibling):
            if sibling and isinstance(sibling, str) and not sibling.strip():
                sibling.extract()
            else:  # pragma: no cover
                pass

        comment.extract()

    # 7. Minify/Clean XML declaration
    # We convert to string and strip the <?xml ... ?> header
    xml_output = str(soup)
    xml_output = re.sub(r"<\?xml.*?\?>", "", xml_output).strip()

    # 8. Wrap in link if necessary.
    #
    # I always wrap the contents in a <figure> tag, which tells the
    # Python-Markdown library to treat this as a block element and
    # skip until it sees the closing </figure> -- otherwise it gets
    # confused if there's an inline <style> tag.
    if link_to == "original":
        dst_path = out_dir / "images" / str(year) / filename
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_path, dst_path)
        href = "/" + str(dst_path.relative_to(out_dir))
        return f'<figure><a href="{href}">{xml_output}</a></figure>'
    else:
        return "<figure>" + xml_output + "</figure>"
