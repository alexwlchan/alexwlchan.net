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
