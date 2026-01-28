"""
Code for dealing with CSS and website styles.
"""

from collections import OrderedDict
from pathlib import Path
import re
from typing import TypedDict

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


STYLE_RE = re.compile(r"\s*<style[^>]*>(?P<css>.*?)</style>\s*", re.DOTALL)
SCSS_USE_RE = re.compile(r'@use "(?P<name>[^"]+)";')
EMPTY_DEFS_RE = re.compile(r"\s*<defs>\s*</defs>\s*")


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

    # Find and remove all <style> tags. I do this using regex because
    # it's faster than parsing with BeautifulSoup, and avoids any
    # changing of the behaviour or meaning of the HTML.
    while m := STYLE_RE.search(html):
        css = m.group("css")

        while use_m := SCSS_USE_RE.search(css):
            use_path = Path("css") / (use_m.group("name") + ".css")
            use_css = use_path.read_text()
            css = css.replace(use_m.group(0), use_css)

        styles[css] = None
        html = html.replace(m.group(0), "")

    # If removing the <style> tags has rendered a set of <defs> empty,
    # just remove them.
    html = EMPTY_DEFS_RE.sub("", html)

    return {"html": html, "styles": "".join(styles)}
