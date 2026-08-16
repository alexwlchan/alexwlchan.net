"""
Code for working with images, including bitmap images added to pages
and images generated from scratch.
"""

from . import tree_icons
from .favicons import create_favicon
from .header_images import create_header_image
from .inline_svg import render_inline_svg

__all__ = ["create_favicon", "create_header_image", "render_inline_svg", "tree_icons"]
