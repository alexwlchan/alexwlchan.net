"""
Code for dealing with HTML and XML templates.
"""

from datetime import datetime
import json
from pathlib import Path
import random
from typing import TypeVar

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from mosaic.css import get_inline_styles
from mosaic.text import cleanup_text, markdownify, markdownify_oneline, strip_html

from .downloads import DownloadExtension
from .inline_svg import InlineSvgExtension
from .legacy_code import CodeBlockExtension
from .pictures import article_card_image, PictureExtension
from .rss_feed import fix_html_for_feed_readers, fix_youtube_iframes, xml_escape
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
            "jinja2.ext.do",
            "jinja2.ext.loopcontrols",
            CodeBlockExtension,
            DownloadExtension,
            InlineSvgExtension,
            PictureExtension,
            SlideExtension,
            SocialExtension,
            TableOfContentsExtension,
            UpdateExtension,
        ],
        trim_blocks=True,
        lstrip_blocks=True,
    )

    env.filters.update(
        {
            "absolute_url": absolute_url,
            "article_card_image": article_card_image,
            "cleanup_text": cleanup_text,
            "escape_attribute_value": escape_attribute_value,
            "fix_html_for_feed_readers": fix_html_for_feed_readers,
            "fix_youtube_iframes": fix_youtube_iframes,
            "format_date": format_date,
            "get_inline_styles": get_inline_styles,
            "jsonify": json.dumps,
            "print": lambda p: print(repr(p)),
            "markdownify": markdownify,
            "markdownify_oneline": markdownify_oneline,
            "minify_json": lambda js: json.dumps(json.loads(js), separators=(",", ":")),
            "sample": random.sample,
            "strip_html": strip_html,
            "xml_escape": xml_escape,
        }
    )
    env.globals.update({"src_dir": src_dir, "out_dir": out_dir})

    return env


def format_date(date_string: str, format: str) -> str:
    """
    Reads an ISO-formatted date, and reformats it in the specified format.
    """
    return datetime.fromisoformat(date_string).strftime(format)


def absolute_url(path: str) -> str:
    """
    Returns the absolute URL for this path.
    """
    if path.startswith("/"):
        return "https://alexwlchan.net" + path
    else:
        return "https://alexwlchan.net/" + path


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
