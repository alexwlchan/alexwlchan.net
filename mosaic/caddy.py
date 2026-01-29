"""
Functions related to Caddy, my web server.
"""

from dataclasses import dataclass
from pathlib import Path


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
    Returns a list of my configured redirects.
    """
    result: list[Redirect] = []

    with open(redir_path) as in_file:
        for lineno, line in enumerate(in_file, start=1):
            if not line.startswith("redir"):
                continue

            _, source, target, *_ = line.strip().split()

            result.append(Redirect(lineno, source, target))

    return result
