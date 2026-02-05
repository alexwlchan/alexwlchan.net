"""
Tests for `mosaic.caddy`.
"""

from pathlib import Path

import pytest

from mosaic.caddy import parse_caddy_redirects, Redirect


@pytest.mark.parametrize(
    "line, redirect",
    [
        (
            "redir /old-path/ /new-path/",
            Redirect(lineno=1, source="/old-path/", target="/new-path/"),
        ),
        (
            "  redir /old-path/ /new-path/",
            Redirect(lineno=1, source="/old-path/", target="/new-path/"),
        ),
        (
            "\tredir /old-path/ /new-path/",
            Redirect(lineno=1, source="/old-path/", target="/new-path/"),
        ),
        (
            "\tredir /old-path/ https://alexwlchan.net/new-path/",
            Redirect(lineno=1, source="/old-path/", target="/new-path/"),
        ),
    ],
)
def test_parse_ignores_whitespace(
    tmp_path: Path, line: str, redirect: Redirect
) -> None:
    """
    The parser ignores lines that start with whitespace.
    """
    redir_path = tmp_path / "redirects.Caddyfile"
    redir_path.write_text(line)
    assert parse_caddy_redirects(redir_path) == [redirect]
