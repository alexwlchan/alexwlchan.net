"""
Tests for `mosaic.caddy`.
"""

from pathlib import Path

from mosaic.caddy import parse_caddy_redirects


def test_parse_caddy_redirects() -> None:
    """
    parse_caddy_redirects reads my redirects file.
    """
    redir_path = Path("caddy/redirects.Caddyfile")
    redirects = parse_caddy_redirects(redir_path)

    assert redirects[0].source == "/.well-known/host-meta*"
    assert redirects[0].target == "https://social.alexwlchan.net/.well-known/host-meta"

    assert any(
        r.source == "/blog/2012/12/hypercritical/"
        and r.target == "/2012/hypercritical/"
        for r in redirects
    )
