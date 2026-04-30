"""
Functions related to Caddy, my web server.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
from subprocess import PIPE
import time
import urllib.error
import urllib.request


__all__ = ["parse_caddy_redirects", "local_webserver"]


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


@contextmanager
def local_webserver(out_dir: Path, port: int = 5757) -> Iterator[str]:
    """
    Start a local instance of Caddy with the specified directory.

    This is a context manager that returns a base URL you can use
    to access the dev server.
    """
    cmd = ["caddy", "run", "--config", "caddy/local_dev.Caddyfile"]
    env = {
        "SITE_ROOT": str(out_dir.absolute()),
        "PORT": str(port),
        "PATH": os.environ["PATH"],
    }

    with subprocess.Popen(cmd, env=env, stdout=PIPE, stderr=PIPE) as proc:
        url = f"http://localhost:{port}/"

        # Wait for up to a second waiting for the server to start.
        #
        # If we get a ConnectionRefusedError, the server hasn't started yet.
        # If we get an HTTPError or a 200 OK, we've connected to the server
        # and it's serving HTTP traffic, so it's started.
        t0 = time.time()
        while time.time() - t0 < 1:  # pragma: no cover
            try:
                urllib.request.urlopen(url)
            except urllib.error.HTTPError:
                break
            except urllib.error.URLError as exc:
                if exc.args and isinstance(exc.args[0], ConnectionRefusedError):
                    pass
                else:
                    raise
            else:
                break

        yield url

        proc.terminate()
        proc.wait(timeout=1)
