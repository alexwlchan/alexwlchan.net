"""
Code for working with images, including bitmap images added to pages
and images generated from scratch.
"""

from . import tree_icons
from .favicons import create_favicon
from .header_images import create_header_image
from .inline_svg import render_inline_svg
from .pictures import get_picture_template_variables

__all__ = [
    "create_favicon",
    "create_header_image",
    "get_picture_template_variables",
    "render_inline_svg",
    "tree_icons",
]
