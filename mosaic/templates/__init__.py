"""
Code for dealing with HTML and XML templates.
"""

import collections
from pathlib import Path
import re
from typing import TypedDict

import bs4
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .comments import LiquidCommentExtension
from .pictures import PictureExtension
from .text import cleanup_text, markdownify, markdownify_oneline, strip_html


def get_jinja_environment(src_dir: Path, out_dir: Path) -> Environment:
    """
    Create a Jinja2 environment which looks in the "templates" directory.
    """
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=False,
        undefined=StrictUndefined,
        extensions=[
            "jinja2.ext.loopcontrols",
            LiquidCommentExtension,
            PictureExtension,
        ],
    )

    env.filters.update(
        {
            "cleanup_text": cleanup_text,
            "get_inline_styles": get_inline_styles,
            "markdownify": markdownify,
            "markdownify_oneline": markdownify_oneline,
            "strip_html": strip_html,
        }
    )
    env.globals.update({"src_dir": src_dir, "out_dir": out_dir})

    return env


ParsedStyles = TypedDict("ParsedStyles", {"html": str, "styles": str})


def get_inline_styles(html: str) -> ParsedStyles:
    """
    Find inline <style> tags in an HTML document, and extract them.
    """
    if "<style" not in html:
        return {"html": html, "styles": ""}

    # Contents of <style> tags we've discovered
    styles = collections.OrderedDict[str, None]()

    # Parse the document as HTML, and look for <style> tags.
    soup = bs4.BeautifulSoup(html, "html.parser")
    for style_tag in soup.find_all("style"):
        styles[style_tag.text.strip()] = None

    # Remove all the <style> tags. We do this as a string manipulation
    # to avoid bs4 changing the meaning or behaviour of our HTML.
    for css in styles:
        html = re.sub(
            r"\s*<style[^>]*>\s*" + re.escape(css) + r"\s*</style>\s*", "", html
        )

    # If removing the <style> tags has rendered a set of <defs> empty,
    # just remove them.
    if "<defs>" in html:
        html = re.sub(r"\s*<defs>\s*</defs>\s*", "", html)

    return {"html": html, "styles": "".join(styles)}
