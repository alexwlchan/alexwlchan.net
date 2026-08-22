"""
Create a series of macOS man pages that I can link to.

This is based on scripts written by Dr Drang:
https://leancrew.com/all-this/2025/04/html-man-pages
"""

from collections.abc import Iterator
import re
import subprocess
from typing import NamedTuple


class Command(NamedTuple):
    """
    A command that could have a man page.
    """

    section: str
    name: str


# MANPAGE_REF_RE = re.compile(r'([0-9a-zA-Z_.:+-]+?)\(([1-9][a-zA-Z]*?)\)'))

MANPAGE_REF_RE = re.compile(
    r"(?P<command_name>[a-zA-Z0-9@\-_\.\+:]+|\[)\((?P<section>[1-9])\)"
)


def get_manpage_contents(
    section: str, name: str, expand_references: bool = False
) -> str:
    """
    Return the manpage for a command, formatted as HTML.
    """
    text = subprocess.check_output(["man", section, name], text=True)

    # \x08 is the Unicode backspace character.
    #
    # In the default output from man:
    #
    #   [char]\x08[char] means bold text,
    #   _\x08[char]      means underlines
    #
    # Replace these with HTML tags.
    text = re.sub(r"([^_])\x08\1", r"<b>\1</b>", text)
    text = text.replace("</b><b>", "")

    text = re.sub(r"_\x08(.)", r"<u>\1</u>", text)
    text = text.replace("</u><u>", "")

    # Replace URLs with <a> tags. man formatting always wraps URLs in <u>,
    # so we can use that to detect the end of a URL.
    text = re.sub(r"<u>(https?://.*?)</u>", r'<a href="\1">\1</a>', text)

    return text


MANPAGE_URL_RE = re.compile(
    r"(/man|\.\.)/man(?P<section>[0-9])/(?P<command_name>[a-z]+)\.html"
)


def find_manpage_urls(text: str) -> Iterator[Command]:
    """
    Given a block of Markdown or HTML, return a set of references to
    man page URLs.
    """
    for m in MANPAGE_URL_RE.finditer(text):
        yield Command(m.group("section"), m.group("command_name"))


if __name__ == "__main__":  # pragma: no cover
    # Add a command-line interface to create manpages with my HTML formatting,
    # for example:
    #
    #     $ python3 mosaic/manpages.py tar 1
    #
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).parent.parent))

    from mosaic.page_types import ManPage
    from mosaic.templates import get_jinja_environment

    try:
        name = sys.argv[1]
        section = sys.argv[2]
    except IndexError:
        sys.exit(f"Usage: {__file__} NAME SECTION")

    content = get_manpage_contents(name=name, section=section)
    page = ManPage(command_name=name, section=section, content=content)

    env = get_jinja_environment(src_dir=Path("src"), out_dir=Path("_out"))

    html = page.render_full_html(env)

    out_path = f"{name}-{section}.html"
    with open(out_path, "w") as f:
        f.write(html)
    print(out_path)
