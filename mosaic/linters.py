"""
Linter rules for verifying the final website output.
"""

import collections
from collections import Counter
from collections.abc import Iterator
import os
from pathlib import Path
import re
from typing import Any
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup, Tag

from .caddy import parse_caddy_redirects
from .fs import find_paths_under


def check_no_broken_html(html_str: str, soup: BeautifulSoup) -> list[str]:
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
        errors.append(f"malformed closing tag following <p>: {m.group(0)}")

    for s in soup.find_all("style"):
        if any(v in s.text for v in ("@use", "<p>", "<br>", "<br/>")):
            errors.append(f"malformed <style> tag: <style>{s.text}</style>")

        # Note(2026-04-06): the `checkbox-text-adventure/index.html` file
        # gets a false error here, because Beautiful Soup sees a <style>
        # string in the middle of some JavaScript.
        #
        # The actual <style> tags are fine, so just ignore this one file.
        if (
            s.find_parent("head") is None
            and "You find yourself standing in a room" not in html_str
        ):
            errors.append(f"<style> tag outside <head>: <style>{s.text}</style>")

    # Look for duplicate ID attributes.
    #
    # There are a handful of exceptions to this rule where I have pages
    # with duplicate ID attributes that are tricky to clean up; leave them
    # as-is but don't add any new ones.
    id_attributes: dict[str, int] = Counter()
    for t in soup.descendants:
        try:
            id_attributes[t.attrs["id"]] += 1  # type: ignore
        except (AttributeError, KeyError):
            pass
    duplicate_ids = {id for id, count in id_attributes.items() if count > 1}
    if duplicate_ids and not any(
        title in html_str
        for title in (
            "Generating art from lattice graphs",
            "Drawing repetitive radial artworks",
            "The best way to tell a website your age",
            "Getting alerts about flaky ECS tasks in Slack",
        )
    ):
        errors.append(f"duplicate IDs detected: {duplicate_ids}")

    return errors


def check_no_localhost_links(html: BeautifulSoup) -> list[str]:
    """
    Check an HTML file doesn't have any links to localhost URLs.
    """
    errors = []

    for tag_name, url in find_all_links(html):
        if urlsplit(url).netloc == "localhost:5757":
            errors.append(f"linking to localhost URL in <{tag_name}>: {url}")

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
    html_urls = set()

    for p in find_paths_under(out_dir, suffix=".html"):
        relative_path = p.relative_to(out_dir)

        # The /files/ directory is just a grab bag of HTML files, and
        # I don't expect it to be hackable.
        if relative_path.is_relative_to("files"):  # pragma: no cover
            continue

        # If it's a subdirectory of /files/ in the /projects/ folder,
        # ignore it -- these all get redirected back to /files/
        if (
            relative_path.is_relative_to("projects")
            and len(relative_path.parts) >= 5
            and relative_path.parts[2] == "files"
        ):  # pragma: no cover
            continue

        if p.name == "index.html":
            html_urls.add(f"/{relative_path.parent}/".replace("/./", "/"))
        else:
            html_urls.add(f"/{relative_path}")

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


def assert_str(s: Any) -> str:
    """
    Type-check a string value.
    """
    assert isinstance(s, str), s
    return s


def find_all_links(html: BeautifulSoup) -> Iterator[tuple[str, str]]:
    """
    Find all links to external resources in this HTML.

    Returns the tag name and external URL.
    """
    # Look for <a> and <link> tags and their `href` attribute.
    # TODO: Should it be an error to omit the href value?
    for anchor in html.find_all(["a", "link"]):
        if "data-proofer-ignore" in anchor.attrs:  # pragma: no cover
            continue
        try:
            yield anchor.name, assert_str(anchor.attrs["href"])
        except KeyError:
            pass

    # Look for <img> and <script> tags and their `src` attribute
    for tag in html.find_all(["img", "script"]):
        try:
            yield tag.name, assert_str(tag.attrs["src"])
        except KeyError:
            pass

    # Look for <source> tags and their `srcset` attribute
    for tag in html.find_all(["img", "source"]):
        if tag.name == "img" and "srcset" not in tag.attrs:
            continue

        for srcset_entry in assert_str(tag.attrs["srcset"]).split(","):
            parts = srcset_entry.split()
            assert len(parts) <= 2, srcset_entry
            url = parts[0]
            yield tag.name, url

    # Look for <meta> tags for cards
    for meta in html.find_all("meta", {"name": "twitter:image"}):
        yield meta.name, assert_str(meta["content"])
    for meta in html.find_all("meta", {"name": "og:image"}):
        yield meta.name, assert_str(meta["content"])

    # Look for xlink:href or href on SVG elements
    for svg in html.find_all("svg"):
        for elem in svg.descendants:
            if not isinstance(elem, Tag):
                continue

            try:
                yield elem.name, assert_str(elem["href"])
            except KeyError:
                pass

            try:
                yield elem.name, assert_str(elem["xlink:href"])
            except KeyError:
                pass


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

        for tag_name, url in find_all_links(soup):
            linked_urls.append((p, tag_name, url))

    # 2. Go through each URL in turn, and check if it exists.
    print("checking links...")
    for pth, tag_name, url in linked_urls:
        if expected_path := get_expected_path(out_dir, pth, url):
            if not expected_path.exists():
                errors.append((pth, tag_name, url))
                continue

            # If the fragment points to a page ID, check the ID exists.
            # If the fragment points to some text on the page, check the
            # page contains that text.
            fragment = urlsplit(url).fragment
            if fragment and fragment.startswith(":~:text="):
                expected_text = unquote(fragment[len(":~:text=") :])
                if expected_text not in pages[expected_path].text:
                    errors.append((pth, tag_name, url))
            elif fragment and not pages[expected_path].find(id=fragment):
                errors.append((pth, tag_name, url))

    # 3. Reorganise the errors into the final output
    result = collections.defaultdict(list)
    for pth, tag_name, url in errors:
        result[pth].append(f"broken url in <{tag_name}>: {url}")
    return result


def get_expected_path(out_dir: Path, page_path: Path, url: str) -> Path | None:
    """
    Return the expected local path for a URL which is linked from a page,
    or None if the URL doesn't exist locally.
    """
    u = urlsplit(url)

    # Skip URLs for external sites or other schemes that are pointing
    # to something other than a remote resource.
    if u.scheme in {"http", "https", "data", "mailto", "javascript", "tel"}:
        return None

    # Query-only URLs, e.g. "?tag=preservation".
    if not u.path:
        return page_path

    # HTML page under /projects/…/files/ subdirectory of a project.
    if (
        u.path.startswith("/projects/")
        and "/files/" in u.path
        and not u.path.endswith("/files/")
    ):
        return out_dir / (u.path.lstrip("/") + ".html")

    # Static file: check if a corresponding file exists in the out_dir.
    # Example: /f/17823e-32x32.svg
    if u.path.startswith("/") and not u.path.endswith("/"):
        return out_dir / u.path.lstrip("/")

    # Static file relative to the current page
    # Example: qunit/qunit-2.24.1.css
    if not u.path.endswith("/") and not u.fragment:
        return page_path.parent / u.path

    # HTML page: check if there's a corresponding HTML page somewhere
    # in the out_dir.
    # Examples: /, /tags/, /2020/example-post/
    if u.path.startswith("/") and u.path.endswith("/"):
        return out_dir / u.path.lstrip("/") / "index.html"

    raise NotImplementedError(url)  # pragma: no cover
