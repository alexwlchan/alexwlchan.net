"""
Code for dealing with CSS and website styles.
"""

from collections import OrderedDict
from pathlib import Path
import re
from typing import TypedDict

from bs4 import BeautifulSoup

import lightningcss


def create_base_css(css_path: str | Path) -> str:
    """
    Return the contents of the base CSS file for the site.

    This resolves all @import rules into a single stylesheet.
    """
    css = lightningcss.bundle_css(str(css_path), minify=True)

    # The lightningcss minifier collapses these text-decoration styles
    # together, which looks wrong in WebKit. Undo this minification.
    css = css.replace(
        "text-decoration:underline 4px",
        "text-decoration:underline;text-decoration-thickness:4px",
    )

    return css

ParsedStyles = TypedDict("ParsedStyles", {"html": str, "styles": str})


def get_inline_styles(html: str) -> ParsedStyles:
    """
    Extract <style> tags from an HTML doc so they can be moved to the <head>.

    I add inline <style> tags to my Markdown source files, but they're only
    meant to go in the <head>. This file has a function that finds and extracts
    all those inline tags, so they can be moved and de-duplicated.
    """
    if "<style" not in html:
        return {"html": html, "styles": ""}

    # Contents of <style> tags we've discovered.
    #
    # This is an OrderedDict so duplicate styles will be removed.
    # TODO(2026-01-21): Can lightningcss do this de-duplication for me?
    styles = OrderedDict[str, None]()

    # Parse the document as HTML, and look for <style> tags.
    soup = BeautifulSoup(html, "html.parser")
    for style_tag in soup.find_all("style"):
        css = style_tag.text.strip()
        
        # Remove this <style> tag. We do this as a string manipulation
        # to avoid bs4 changing the meaning or behaviour of our HTML.
        html = re.sub(
            r"\s*<style[^>]*>\s*" + re.escape(css) + r"\s*</style>\s*", "", html
        )
        
        # TODO(2026-01-21): This looks for the x-text/scss and @use statements
        # I wrote with Jekyll. The better fix would be to replace this
        # with @import statements and use lightningcss to bundle everything.
        while m := re.search(r'@use "(?P<name>[^"]+)";', css):
            use_path = Path("css") / (m.group("name") + ".css")
            use_css = use_path.read_text()
            css = css.replace(m.group(0), use_css)
        
        styles[css] = None

    # If removing the <style> tags has rendered a set of <defs> empty,
    # just remove them.
    if "<defs>" in html:
        html = re.sub(r"\s*<defs>\s*</defs>\s*", "", html)

    return {"html": html, "styles": "".join(styles)}
