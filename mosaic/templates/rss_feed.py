"""
Filters for producing the RSS feed.
"""

import re
from xml.sax.saxutils import quoteattr

from bs4 import BeautifulSoup, Comment, Tag


def xml_escape(text: str) -> str:
    """
    Escape a string for use in an XML document.
    """
    for old, new in [("&", '&amp;'), ('"', '&quot;'), ('<', '&lt;'), ('>', '&gt;')]:
        text = text.replace(old, new)
    
    return text


def fix_youtube_iframes(html: str) -> str:
    """
    Replace YouTube iframes in the RSS feed with links.

    This is based on https://github.com/rubys/feedvalidator, which says
    that embedding an <iframe> in an RSS feed can be a security risk.
    """
    while m := re.search(
        r'<iframe class="youtube" id="youtube_(?P<video_id>[^"]+)"', html
    ):
        url = f"https://youtube.com/watch?v={m.group('video_id')}"
        html = html.replace(m.group(0), f'<p><a href="{url}">{url}</a></p>')

    return html


def fix_relative_url(tag: Tag, attribute_name: str) -> None:
    """
    Convert a URL to be an absolute URL.
    """
    existing_value = tag.get(attribute_name)
    if not existing_value:
        return

    # Handle comma-separated values (common in srcset)
    values = [v.strip() for v in str(existing_value).split(",")]
    new_values = []

    for v in values:
        if v.startswith("/images") or v.startswith("/files"):
            new_values.append(f"https://alexwlchan.net{v}")
        else:
            new_values.append(v)

    tag[attribute_name] = ", ".join(new_values)


def fix_html_for_feed_readers(html: str) -> str:
    """
    Apply some clean-ups for HTML embedded in the RSS feed.
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1. Remove all tags which aren't appropriate in an RSS feed.
    for tag in soup.find_all(["link", "script", "style"]):
        tag.extract()

    # 2. Remove specific attributes: style, controls, aria-hidden
    #
    # According to https://github.com/rubys/feedvalidator, these aren't
    # allowed in an RSS feed.
    bad_attrs = ["style", "controls", "aria-hidden", "title", "onchange", "onclick"]
    for tag in soup.find_all(True):  # True finds all tags
        for attr in bad_attrs:
            if tag.has_attr(attr):
                del tag[attr]

    # 3. Delete the logo and avatars from embedded social media posts.
    for embed in soup.select("blockquote.embed"):
        for logo in embed.select("svg.logo"):
            logo.decompose()
        for avatar in embed.select("img.avatar"):
            avatar.decompose()

    # 4. Replace twemoji SVGs with their alt text (the emoji itself)
    for emoji in soup.select("img.twemoji"):
        assert isinstance(emoji["alt"], str)
        emoji.replace_with(emoji["alt"])

    # 5. Replace relative URLs with absolute URLs.
    link_elements = [
        {"selector": "img", "attr": "src"},
        {"selector": "a", "attr": "href"},
        {"selector": "source", "attr": "srcset"},
        {"selector": "image", "attr": "src"},  # For inline SVGs
    ]

    for config in link_elements:
        for tag in soup.select(config["selector"]):
            fix_relative_url(tag, config["attr"])
    
    # 6. Remove comments.
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

    # 7. Convert back to string and remove empty paragraphs
    # We use .decode_contents() to get just the inner HTML without
    # the body tags
    output = soup.body.decode_contents() if soup.body else str(soup)
    return output.replace("<p></p>", "")
