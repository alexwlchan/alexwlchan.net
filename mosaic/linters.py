"""
Linter rules for verifying the final website output.
"""

import re

from bs4 import BeautifulSoup
import hyperlink


def check_no_broken_html(html_str: str) -> list[str]:
    """
    Check an HTML file doesn't have any <p> tags followed by unexpected
    HTML, which is often a sign of a rendering error.
    """
    errors = []

    for m in re.finditer(r"<p><(?P<tag_name>[^\s>/]+)(.*?)/?>", html_str):
        tag_name = m.group("tag_name")

        if tag_name in {
            "a",
            "br",
            "cite",
            "code",
            "em",
            "img",
            "picture",
            "s",
            "strong",
        }:
            continue

        errors.append(f"unexpected tag following <p>: {m.group(0)}")

    for m in re.finditer(r"<p>&lt;(.*?)&gt;", html_str):
        errors.append(f"malformed tag following <p>: {m.group(0)}")

    return errors


def check_no_localhost_links(html: BeautifulSoup) -> list[str]:
    """
    Check an HTML file doesn't have any links to localhost URLs.
    """
    errors = []

    for anchor in html.find_all("a"):
        try:
            url = anchor.attrs["href"]
        except KeyError:
            continue
        assert isinstance(url, str)

        u = hyperlink.parse(url)
        if u.host == "localhost" and u.port == 5757:
            errors.append(f"linking to localhost URL: {url}")

    return errors
