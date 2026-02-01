"""
Linter rules for verifying the final website output.
"""

import collections
from collections.abc import Iterator
import os
from pathlib import Path
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from tqdm import tqdm

from .caddy import parse_caddy_redirects
from .fs import find_paths_under


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


def check_images_have_alt_text(html: BeautifulSoup) -> list[str]:
    """
    Check every image has alt text.
    """
    errors = []

    for img in html.find_all("img"):
        if "data-proofer-ignore" in img.attrs:
            continue

        if img.attrs.get("alt") is None:
            errors.append(f"image is missing alt text: {img.attrs['src']}")

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


def check_all_urls_are_hackable(redir_path: Path, out_dir: Path) -> list[str]:
    """
    Check that every URL is "hackable".

    Quoting the slightly formal language of Nielsen Norman:

        A usable site requires […] URLs that are "hackable" to allow users
        to move to higher levels of the information architecture by hacking
        off the end of the URL
        ~ https://www.nngroup.com/articles/url-as-ui/

    Make sure I'm doing that!

    Every "hackable" URL should either exist in the site, or there should
    be a redirect for it.
    """
    # Create a set of which paths will return an HTML page.
    #
    # This means either:
    #
    #     - There's a redirect that takes you to another page, or
    #     - There's a folder with an index.html file that will be served
    #
    # The goal is to have two sets of URLs without trailing slashes,
    # e.g. {'/writing', '/til'}
    #
    redirect_urls = {r.source for r in parse_caddy_redirects(redir_path)}
    html_urls = {
        f"/{p.parent.relative_to(out_dir)}/".replace("/./", "/")
        for p in find_paths_under(out_dir, suffix=".html")
        if not p.is_relative_to(out_dir / "files")
    }
    assert "/" in html_urls

    reachable_urls = redirect_urls.union(html_urls)

    # Work out all the URLs that somebody could "hack" their way towards.
    unreachable_urls = set()

    for url in html_urls:
        for u in get_all_hackable_urls(url):
            if u not in reachable_urls:
                unreachable_urls.add(u)

    return [
        f"url can be hacked but won’t resolve: {url!r}"
        for url in sorted(unreachable_urls)
    ]


def get_all_hackable_urls(url: str) -> Iterator[str]:
    """
    Given a URL, return a list of all URLs that can be hacked from it.

        get_all_parent_directories("/blog/2013/01/my-post")
         => ["/blog/2013/01",
             "/blog/2013",
             "/blog"]

    """
    assert url.startswith("/"), f"URLs must start with slash: {url!r}"

    while url != "/":
        url = os.path.dirname(url)
        if url.endswith("/"):
            yield url
        else:
            yield url + "/"


def check_links_are_consistent(
    out_dir: Path, pages: dict[Path, BeautifulSoup]
) -> dict[Path, list[str]]:
    """
    Go through every linked resource in every page (links, images, cards)
    and check they point to a resource that exists.
    """
    # Track known errors of pages linking to a non-existent resource
    errors: list[tuple[Path, str, str]] = []

    # 1. Build a list: path, tag, URL
    linked_urls: list[tuple[Path, str, str]] = []

    for p, soup in pages.items():
        # These are some standalone sites/pages that I'm willing to ignore
        # for the sake of linting.
        if "fun-stuff" in p.parts or "files" in p.parts:  # pragma: no cover
            continue

        # Look for <a> and <link> tags and their `href` attribute.
        # TODO: Should it be an error to omit the href value?
        for anchor in soup.find_all(["a", "link"]):
            if "data-proofer-ignore" in anchor.attrs:  # pragma: no cover
                continue
            try:
                entry = (p, anchor.name, anchor.attrs["href"])
                linked_urls.append(entry)  # type: ignore
            except KeyError:
                pass

        # Look for <img> and <script> tags and their `src` attribute
        for tag in soup.find_all(["img", "script"]):
            try:
                entry = (p, tag.name, tag.attrs["src"])
                linked_urls.append(entry)  # type: ignore
            except KeyError:
                pass

        # Look for <source> tags and their `srcset` attribute
        for tag in soup.find_all(["img", "source"]):
            if tag.name == "img" and "srcset" not in tag.attrs:
                continue

            for srcset_entry in tag.attrs["srcset"].split(","):  # type: ignore
                parts = srcset_entry.split()
                assert len(parts) <= 2, srcset_entry
                url = parts[0]
                linked_urls.append((p, tag.name, url))

        # Look for <meta> tags for cards
        for meta in soup.find_all("meta", {"name": "twitter:image"}):
            linked_urls.append((p, meta.name, meta["content"]))  # type: ignore
        for meta in soup.find_all("meta", {"name": "og:image"}):
            linked_urls.append((p, meta.name, meta["content"]))  # type: ignore

    # 2. Go through each URL in turn, and check if it exists.
    for pth, tag_name, url in tqdm(linked_urls, desc="checking links"):
        u = urlparse(url)

        # Skip URLs for external sites or other schemes that are pointing
        # to something other than a remote resource.
        if (
            u.scheme in {"http", "https", "data", "mailto", "javascript", "tel"}
            and u.netloc != "alexwlchan"
        ):
            continue

        # Query-only URLs, e.g. "?tag=preservation".
        if not u.path and not u.fragment:
            continue

        # Static file: check if a corresponding file exists in the out_dir.
        # Example: /f/17823e-32x32.svg
        if u.path.startswith("/") and not u.path.endswith("/") and not u.fragment:
            expected_path = out_dir / u.path.lstrip("/")
            if not expected_path.exists():
                errors.append((pth, tag_name, url))
            continue

        # Static file relative to the current page
        # Example: qunit/qunit-2.24.1.css
        if not u.path.endswith("/") and not u.fragment:
            expected_path = pth.parent / u.path
            if not expected_path.exists():
                errors.append((pth, tag_name, url))
            continue

        # HTML file with fragment
        if u.path.startswith("/") and not u.path.endswith("/") and u.fragment:
            expected_path = out_dir / u.path.lstrip("/")
            if not expected_path.exists() or not pages[expected_path].find(
                id=u.fragment
            ):
                errors.append((pth, tag_name, url))
            continue

        # Fragment: check if a document with the corresponding ID exists
        # in the HTML file.
        # Example: #main
        if not u.path and not u.query and u.fragment:
            if not pages[pth].find(id=u.fragment):
                errors.append((pth, tag_name, url))
            continue

        # HTML page: check if there's a corresponding HTML page somewhere
        # in the out_dir.
        # Examples: /, /tags/, /2020/example-post/
        if u.path.startswith("/") and u.path.endswith("/"):
            expected_path = out_dir / u.path.lstrip("/") / "index.html"
            if not expected_path.exists() or (
                u.fragment and not pages[expected_path].find(id=u.fragment)
            ):
                errors.append((pth, tag_name, url))
            continue

        raise NotImplementedError(url)  # pragma: no cover

    # 3. Reorganise the errors into the final output
    result = collections.defaultdict(list)
    for pth, tag_name, url in errors:
        result[pth].append(f"broken url in <{tag_name}>: {url}")
    return result
