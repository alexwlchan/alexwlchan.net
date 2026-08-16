"""
Code for dealing with HTML and XML templates.
"""

from pathlib import Path

from chives.text import smartify
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from mosaic.css import get_inline_styles
from mosaic.models import filter_for_topic, get_topic, group_items_for_layout
from mosaic.syntax_highlighting import apply_syntax_highlighting
from mosaic.text import cleanup_text, markdownify, markdownify_oneline

from . import tree_icons
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
            "article_card_image": article_card_image,
            "cleanup_text": cleanup_text,
            "filter_for_topic": filter_for_topic,
            "fix_html_for_feed_readers": fix_html_for_feed_readers,
            "get_inline_styles": get_inline_styles,
            "group_items_for_layout": group_items_for_layout,
            "print": lambda p: print(repr(p)),
            "markdownify": markdownify,
            "markdownify_oneline": markdownify_oneline,
            "smartify": smartify,
            "xml_escape": xml_escape,
        }
    )
    env.globals.update(
        {
            "apply_syntax_highlighting": apply_syntax_highlighting,
            "src_dir": src_dir,
            "out_dir": out_dir,
            "get_topic": get_topic,
            "tree_icons": tree_icons,
        }
    )  # type: ignore

    return env
