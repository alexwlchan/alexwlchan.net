"""
Prepare an SVG file to be rendered as an inline SVG.
"""

import os
from pathlib import Path
import shutil
import re
from typing import Any, Literal

from bs4 import BeautifulSoup, Comment
from chives.text import smartify

from mosaic import cache


__all__ = ["render_inline_svg"]


def render_inline_svg(
    src_dir: Path,
    src_path: Path,
    out_dir: Path,
    alt: str | None = None,
    link_to: Literal["original"] | None = None,
    **kwargs: Any,
) -> str:
    """
    Create the HTML to render an inline SVG.
    """
    # 1. Verify the file extension
    if src_path.suffix != ".svg":
        raise ValueError(
            f"You can only use {{% inline_svg %}} with SVG images; got {src_path!r}"
        )

    # 2. Read and parse the SVG
    soup = BeautifulSoup(src_path.read_text(), "xml")
    svg_tag = soup.find("svg")
    if svg_tag is None:
        raise ValueError(f"No <svg> tag found in {src_path!r}")

    # Record that this is an inline SVG.
    cache.set("is_inline_svg", key=os.path.relpath(src_path, start=src_dir))

    # 3. Add the accessibility role. See "Accessible SVGs" §2.
    svg_tag["role"] = "img"

    # 4. If alt text, add a <title> element.
    # TODO: Are there any cases where I wouldn't have alt text?
    if alt is not None:
        svg_id = f"svg_{src_path.stem}"

        # Create a new <title> tag
        title_tag = soup.new_tag("title")
        title_tag["id"] = svg_id
        title_tag.string = smartify(alt)

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

    # 7. Minify style tags. This isn't a full minification; just removing
    # enough that the Markdown renderer doesn't interpret this as a
    # code block halfway through.
    for style in soup.find_all("style"):
        style.string.replace_with(  # type: ignore
            "\n".join([ln.lstrip() for ln in style.text.splitlines() if ln.lstrip()])
        )

    # 8. Minify/Clean XML declaration
    # We convert to string and strip the <?xml ... ?> header
    xml_output = str(soup)
    xml_output = re.sub(r"<\?xml.*?\?>", "", xml_output).strip()

    # 9. Wrap in link if necessary.
    if link_to == "original":
        dst_path = out_dir / src_path.relative_to(src_dir)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_path, dst_path)
        href = "/" + str(dst_path.relative_to(out_dir))
        html = f'<a href="{href}">{xml_output}</a>'
    else:
        html = xml_output

    return html
