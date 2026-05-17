"""
Code for dealing with CSS and website styles.
"""

from collections import OrderedDict
from pathlib import Path
import re
from typing import TypedDict

from bs4 import BeautifulSoup
import lightningcss

from .git import git_root
from .text import md5


__all__ = ["CSS_DIR", "create_base_css", "get_inline_styles"]


CSS_DIR = git_root() / "css"


def create_base_css() -> tuple[str, str]:
    """
    Return the contents of the base CSS file for the site.

    This resolves all @import rules into a single stylesheet.

    Returns the filename and new CSS.
    """
    css_path = CSS_DIR / "style.css"

    css = lightningcss.bundle_css(str(css_path), minify=True)

    # The lightningcss minifier collapses these text-decoration styles
    # together, which looks wrong in WebKit. Undo this minification.
    css = css.replace(
        "text-decoration:underline 4px",
        "text-decoration:underline;text-decoration-thickness:4px",
    )

    # Using three characters of hash gives me 16^3 = 4096 bits of entropy.
    # Given I cache CSS for a year and only change it a handful of times,
    # that should be plenty.
    h = md5(css)[:3]

    return f"style.{h}.css", css


ParsedStyles = TypedDict("ParsedStyles", {"html": str, "styles": str})


STYLE_RE = re.compile(r"\s*<style[^>]*>(?P<css>.*?)</style>\s*", re.DOTALL)
LINK_RE = re.compile(r"\s*(<link[^>]+>)\s*", re.DOTALL)
EMPTY_DEFS_RE = re.compile(r"\s*<defs>\s*</defs>\s*")


def get_inline_styles(html: str) -> ParsedStyles:
    """
    Extract <style> tags from an HTML doc so they can be moved to the <head>.

    I add inline <style> tags to my Markdown source files, but they're only
    meant to go in the <head>. This file has a function that finds and extracts
    all those inline tags, so they can be moved and de-duplicated.
    """
    if "<style" not in html and "<link" not in html:
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
        styles[css] = None
        html = html.replace(m.group(0), "")

    # Find and remove all the <link> tags.
    for m in LINK_RE.finditer(html):
        link_tag = BeautifulSoup(m.group(0), "html.parser").find("link")
        assert link_tag is not None

        if link_tag.attrs["rel"] != ["stylesheet"]:
            continue

        href = link_tag.attrs["href"]
        assert isinstance(href, str)
        css = Path(href).read_text()

        styles[css] = None
        html = html.replace(m.group(0), "")

    # If removing the <style> tags has rendered a set of <defs> empty,
    # just remove them.
    if "<defs" in html:
        html = EMPTY_DEFS_RE.sub("", html)

    return {"html": html, "styles": "".join(styles)}
