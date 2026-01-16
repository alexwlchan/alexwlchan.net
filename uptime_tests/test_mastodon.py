"""
Test routes used to find my Mastodon server at social.alexwlchan.net.
"""

import httpx
import pytest


@pytest.mark.parametrize(
    "path",
    ["/.well-known/host-meta", "/.well-known/webfinger", "/.well-known/nodeinfo"],
)
def test_mastodon_redirect(path: str) -> None:
    """
    Paths used by Mastodon instances are redirected to social.alexwlchan.net.
    """
    resp = httpx.get(f"https://alexwlchan.net{path}")

    assert resp.status_code == 301
    assert resp.headers["location"] == f"https://social.alexwlchan.net{path}"
