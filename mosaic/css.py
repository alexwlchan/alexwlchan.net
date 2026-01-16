"""
Code for dealing with CSS and website styles.
"""

from pathlib import Path

import lightningcss


def create_base_css(css_path: str | Path) -> str:
    """
    Return the contents of the base CSS file for the site.

    This resolves all @import rules into a single stylesheet.
    """
    return lightningcss.bundle_css(str(css_path), minify=True)
