"""
Linter rules for finding malformed or broken HTML.
"""

from collections import Counter
from pathlib import Path
import re

from bs4 import BeautifulSoup


def check_html_paragraphs(html_str: str) -> list[str]:
    """
    Look at <p> tags for unexpected HTML or entities, which are usually
    a sign of an HTML rendering error.
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


def check_malformed_closing_tags(path: Path, html_str: str) -> list[str]:
    """
    Look at malformed closing tags like <picture> and <pre>, which are
    usually a sign of an HTML rendering error.
    """
    # Note(2026-05-09): these tests have a <pre> inside a <pre>,
    # because I'm testing how code operates on a <pre> tag.
    # Ignore for now.
    if path in {
        Path(
            "_out/projects/chives/commits/74520670083b5073a282f24992a84d1affcd13d7/index.html"
        ),
        Path(
            "_out/projects/chives/commits/37bd7f646db6b4617d7680d3318053f3ebc1b3a5/index.html"
        ),
        Path("_out/projects/chives/files/tests/test_text.py.html"),
    }:  # pragma: no cover
        return []

    return [
        f"malformed closing tag: {m.group(0)}"
        for m in re.finditer(r"&lt;/(?:picture|code|pre)>", html_str)
    ]


def check_style_tags(html_str: str, soup: BeautifulSoup) -> list[str]:
    """
    Look for <style> tags that look like they contain HTML or rendering errors.
    """
    errors = []

    # Unexpected HTML tags or markup inside HTML tags can be a clue that
    # something is broken in the rendering pipeline.
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

    return errors


def check_pre_tags(path: Path, soup: BeautifulSoup) -> list[str]:
    """
    Look for <pre> tags that contain triple backticks, which is usually
    a sign of a rendering error.
    """
    if path in {
        Path("_out/2017/extensions-in-python-markdown/index.html"),
        Path("_out/2021/console-copying/index.html"),
        Path("_out/notes/2024/how-to-highlight-python-console-in-jekyll/index.html"),
        Path("_out/notes/2024/use-the-raw-tag-to-describe-liquid-in-liquid/index.html"),
    }:  # pragma: no cover
        return []

    if path.is_relative_to(Path("_out/projects")):  # pragma: no cover
        return []

    errors = []

    for pre in soup.find_all("pre"):
        if "```" in pre.text:
            errors.append(f"malformed <pre> tag: <pre>{pre.text}</pre>")

    return errors


def check_all_ids_are_unique(html_str: str, soup: BeautifulSoup) -> list[str]:
    """
    Look for pages where there are multiple elements with the same
    `id` attribute.
    """
    errors = []

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
