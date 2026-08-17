"""
Code for dealing with CSS and website styles.
"""

from collections import OrderedDict
from pathlib import Path
import re

from bs4 import BeautifulSoup, Tag
import lightningcss
from pydantic import BaseModel

from .cache import get_cache, md5
from .git import git_root


__all__ = ["CSS_DIR", "create_base_css", "get_inline_styles"]


CSS_DIR = git_root() / "css"
_CACHE = get_cache(".cache/css.db")

STYLE_RE = re.compile(r"\s*<style[^>]*>(?P<css>.*?)</style>\s*", re.DOTALL)
LINK_RE = re.compile(r"\s*(<link[^>]+>)\s*", re.DOTALL)
EMPTY_DEFS_RE = re.compile(r"\s*<defs>\s*</defs>\s*")


class ParsedStyles(BaseModel):
    """
    An HTML document free of inline <style> or <link> tags, and the
    CSS that should be added to the document <head>.
    """

    html: str
    styles: str = ""


def create_base_css() -> tuple[str, str]:
    """
    Bundle and minify the base stylesheet into a single file string.

    Resolves all `@import` statements in `css/style.css` and appends
    a short hash for cache busting.

    Returns a tuple of (hashed_filename, compiled_css).
    """
    css_path = CSS_DIR / "style.css"

    css = lightningcss.bundle_css(str(css_path), minify=True)  # type: ignore

    # Lightning CSS combines text-decoration properties, which renders
    # incorrectly in WebKit. Restore separate text-decoration properties.
    css = css.replace(
        "text-decoration:underline 4px",
        "text-decoration:underline;text-decoration-thickness:4px",
    )

    # 3 hex characters provide 16^3 = 4096 possible values.
    # Given CSS is cached for a year and changes infrequently, the risk
    # of a collision is negligible.
    h = md5(css)[:3]

    return f"style.{h}.css", css


def get_inline_styles(html: str) -> ParsedStyles:
    """
    Return parsed inline styles for an HTML document, caching the result.
    """
    cache_ns = "parse_inline_styles"
    cache_key = md5(html)

    if styles_json := _CACHE.get(cache_ns, cache_key):
        return ParsedStyles.model_validate_json(styles_json)
    else:
        styles = parse_inline_styles(html)
        _CACHE.set(cache_ns, cache_key, styles.model_dump_json())
        return styles


def parse_inline_styles(html: str) -> ParsedStyles:
    """
    Extract `<style>` tags and linked stylesheets from an HTML document.

    This is used to extract inline styles added during Markdown rendering,
    so they can be added to the `<head>` instead.
    """
    if "<style" not in html and "<link" not in html:
        return ParsedStyles(html=html)

    # Deduplicate styles, but preserve the order they were found.
    # TODO(2026-01-21): Can lightningcss do this de-duplication for me?
    styles = OrderedDict[str, None]()

    # Extract and strip <style> tags.
    #
    # Use regex rather than BeautifulSoup because it's faster and avoids
    # any unwanted changing of the HTML.
    for m in STYLE_RE.finditer(html):
        styles[m.group("css")] = None

    html = STYLE_RE.sub("", html)

    # Find, load, and remove external <link rel="stylesheet"> tags.
    def _process_link_tag(match: re.Match[str]) -> str:
        raw_tag = match.group(0)
        link_tag = BeautifulSoup(raw_tag, "html.parser").find("link")
        assert isinstance(link_tag, Tag), link_tag

        rel_attrs = link_tag.get("rel") or []
        assert isinstance(rel_attrs, list), rel_attrs

        if "stylesheet" not in rel_attrs:
            return raw_tag

        href = link_tag.get("href")
        assert isinstance(href, str), href

        file_path = CSS_DIR / Path(href).relative_to("css")
        if not file_path.exists():
            raise ValueError(f"<link> tag points to missing file: {href}")

        styles[file_path.read_text()] = None
        return ""

    html = LINK_RE.sub(_process_link_tag, html)

    # Clean up <defs> tags left empty after removing <style> tags.
    if "<defs" in html:
        html = EMPTY_DEFS_RE.sub("", html)

    return ParsedStyles(html=html, styles="".join(styles))
