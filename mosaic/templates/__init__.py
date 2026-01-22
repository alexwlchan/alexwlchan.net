"""
Code for dealing with HTML and XML templates.
"""

from datetime import datetime
from pathlib import Path
from typing import TypeVar

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from mosaic.css import get_inline_styles
from mosaic.text import cleanup_text, markdownify, markdownify_oneline, strip_html

from .comments import LiquidCommentExtension
from .downloads import DownloadExtension
from .inline_svg import InlineSvgExtension
from .pictures import PictureExtension
from .slides import SlideExtension
from .social_embeds import SocialExtension
from .table_of_contents import TableOfContentsExtension
from .updates import UpdateExtension


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
            DownloadExtension,
            InlineSvgExtension,
            LiquidCommentExtension,
            PictureExtension,
            SlideExtension,
            SocialExtension,
            TableOfContentsExtension,
            UpdateExtension,
        ],
    )

    env.filters.update(
        {
            "cleanup_text": cleanup_text,
            "escape_attribute_value": escape_attribute_value,
            "format_date": format_date,
            "get_inline_styles": get_inline_styles,
            "markdownify": markdownify,
            "markdownify_oneline": markdownify_oneline,
            "strip_html": strip_html,
        }
    )
    env.globals.update({"src_dir": src_dir, "out_dir": out_dir})

    return env


def format_date(date_string: str, format: str) -> str:
    """
    Reads an ISO-formatted date, and reformats it in the specified format.
    """
    return datetime.fromisoformat(date_string).strftime(format)


T = TypeVar("T")


def escape_attribute_value(value: T) -> T:
    """
    Escape an attribute value, especially in alt text.

    Ensure characters that might be interpreted as HTML or Markdown
    don't get included in their raw form.
    """
    if not isinstance(value, str):
        return value

    for old, new in [
        ("<", "&lt;"),
        (">", "&gt;"),
        ("`", "&grave;"),
        ("*", "&ast;"),
        ("_", "&lowbar;"),
    ]:
        value = value.replace(old, new)  # type: ignore

    return value
