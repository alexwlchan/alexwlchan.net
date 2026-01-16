"""
Code for dealing with HTML and XML templates.
"""

import collections
import re
from typing import TypedDict

import bs4


ParsedStyles = TypedDict("ParsedStyles", {"html": str, "styles": str})


def get_inline_styles(html: str) -> ParsedStyles:
    """
    Find inline <style> tags in an HTML document, and extract them.
    """
    if "<style" not in html:
        return {"html": html, "styles": ""}

    # Contents of <style> tags we've discovered
    styles = collections.OrderedDict[str, None]()

    # Parse the document as HTML, and look for <style> tags.
    soup = bs4.BeautifulSoup(html, "html.parser")
    for style_tag in soup.find_all("style"):
        styles[style_tag.text.strip()] = None

    # Remove all the <style> tags. We do this as a string manipulation
    # to avoid bs4 changing the meaning or behaviour of our HTML.
    for css in styles:
        html = re.sub(
            r"\s*<style[^>]*>\s*" + re.escape(css) + r"\s*</style>\s*", "", html
        )

    # If removing the <style> tags has rendered a set of <defs> empty,
    # just remove them.
    if "<defs>" in html:
        html = re.sub(r"\s*<defs>\s*</defs>\s*", "", html)

    return {"html": html, "styles": "".join(styles)}
