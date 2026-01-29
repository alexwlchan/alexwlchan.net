"""
Linter rules for verifying the final website output.
"""

import collections
from pathlib import Path
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .caddy import parse_caddy_redirects


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

    for m in re.finditer(r"&lt;/(?:picture|code|pre)>", html_str):
        errors.append(f"malformed closing tag <p>: {m.group(0)}")

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

        if urlparse(url).netloc == "localhost:5757":
            errors.append(f"linking to localhost URL: {url}")

    return errors


def check_redirects(redir_path: Path, out_dir: Path) -> list[str]:
    """
    Check the redirects are consistent.
    """
    errors = []
    redirects = parse_caddy_redirects(redir_path)

    # The source of every redirect is a page that doesn't exist.
    for r in redirects:
        # Skip the Mastodon URLs, which are a bit special
        if r.source.startswith("/.well-known/") and r.target.startswith(
            "https://social.alexwlchan.net"
        ):
            continue

        if (out_dir / r.source.lstrip("/") / "index.html").exists():
            errors.append(f"L{r.lineno}: redirect from file that exists ({r.source})")

    # The source of every redirect is unique
    source_tally = collections.defaultdict(set)
    for r in redirects:
        source_tally[r.source].add(r.lineno)

    for source, linenos in source_tally.items():
        if len(linenos) > 1:
            lineno_str = ", ".join(f"L{ln}" for ln in linenos)
            errors.append(f"duplicate source on lines {lineno_str} ({source})")

    # The target of every redirect is a page that does exist.
    for r in redirects:
        # Skip the Mastodon URLs, which are a bit special
        if r.source.startswith("/.well-known/") and r.target.startswith(
            "https://social.alexwlchan.net"
        ):
            continue

        if r.target.endswith("/"):
            expected_path = out_dir / r.target.lstrip("/") / "index.html"
        else:
            expected_path = out_dir / r.target.lstrip("/")

        if not (expected_path).exists():
            errors.append(
                f"L{r.lineno}: redirect to a page that does not exist ({r.target})"
            )

    return errors
