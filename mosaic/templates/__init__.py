"""
Code for dealing with HTML and XML templates.
"""

from collections.abc import Iterator
from datetime import datetime
import json
from pathlib import Path
import random
from typing import Literal, TypedDict, TypeVar

from chives.text import smartify
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from mosaic import page_types
from mosaic.css import get_inline_styles
from mosaic.page_types import Post
from mosaic.text import (
    cleanup_text,
    markdownify,
    markdownify_oneline,
    strip_html,
)
from mosaic.topics import get_topic_by_name

from .downloads import DownloadExtension
from .inline_svg import InlineSvgExtension
from .pictures import article_card_image, PictureExtension
from .rss_feed import fix_html_for_feed_readers, xml_escape
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
            "filter_for_topic": filter_for_topic,
            "fix_html_for_feed_readers": fix_html_for_feed_readers,
            "format_date": format_date,
            "get_inline_styles": get_inline_styles,
            "group_list_of_posts": group_list_of_posts,
            "jsonify": json.dumps,
            "print": lambda p: print(repr(p)),
            "markdownify": markdownify,
            "markdownify_oneline": markdownify_oneline,
            "minify_json": lambda js: json.dumps(json.loads(js), separators=(",", ":")),
            "sample": random.sample,
            "smartify": smartify,
            "strip_html": strip_html,
            "xml_escape": xml_escape,
        }
    )
    env.globals.update(
        {"src_dir": src_dir, "out_dir": out_dir, "get_topic_by_name": get_topic_by_name}
    )

    return env


def format_date(date_string: str, format: str) -> str:
    """
    Reformat an ISO-formatted date in the specified format.
    """
    return datetime.fromisoformat(date_string).strftime(format)


def absolute_url(path: str) -> str:
    """
    Return the absolute URL for this path.
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


def filter_for_topic(
    pages: list[page_types.BaseHtmlPage], topic_name: str
) -> list[page_types.BaseHtmlPage]:
    """
    Return a list of pages that match a particular topic.
    """
    return [p for p in pages if p.belongs_to_topic(topic_name)]


PostGroup = TypedDict(
    "PostGroup", {"type": Literal["featured", "remaining"], "posts": list[Post]}
)


def group_list_of_posts(posts: list[Post]) -> Iterator[PostGroup]:  # pragma: no cover
    """
    Group a list of posts for display on a page.

    Always start with featured articles, then put at least 3 other posts
    between a run of featured articles.
    """
    featured_posts = []
    remaining_posts = []

    for p in posts:
        if p.index.exclude:
            continue

        if p.index.feature:
            featured_posts.append(p)
        else:
            remaining_posts.append(p)

        if len(featured_posts) != 2:
            continue

        yield {"type": "featured", "posts": featured_posts}
        featured_posts = []

        if len(remaining_posts) >= 3:
            yield {"type": "remaining", "posts": remaining_posts}
            remaining_posts = []

    if featured_posts:
        yield {"type": "featured", "posts": featured_posts}

    if remaining_posts:
        yield {"type": "remaining", "posts": remaining_posts}
