"""
Functions related to Caddy, my web server.
"""

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class Redirect:
    """
    A URL redirect in my Caddyfile.
    """

    lineno: int
    source: str
    target: str


def parse_caddy_redirects(redir_path: Path) -> list[Redirect]:
    """
    Return a list of my configured redirects.
    """
    result: list[Redirect] = []
    current_domain = ""

    with open(redir_path) as in_file:
        for lineno, line in enumerate(in_file, start=1):
            if m := re.match(r"^(?P<subdomain>[a-z]+)\.alexwlchan.net \{$", line):
                current_domain = f"https://{m.group('subdomain')}.alexwlchan.net"
                continue
            elif line == "}":
                current_domain = ""

            if not line.strip().startswith("redir"):
                continue

            _, source, target, *_ = line.strip().split()

            if target.startswith("https://alexwlchan.net/"):
                target = target.replace("https://alexwlchan.net/", "/")

            result.append(Redirect(lineno, current_domain + source, target))

    return result
