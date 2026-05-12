"""
Test routes used to find my Mastodon server at social.alexwlchan.net.
"""

from ssl import SSLContext
import urllib.request

import pytest


@pytest.mark.parametrize(
    "path",
    [
        "/.well-known/host-meta",
        "/.well-known/webfinger?resource=acct:alex@alexwlchan.net",
        "/.well-known/nodeinfo",
    ],
)
def test_mastodon_redirect(ssl_context: SSLContext, path: str) -> None:
    """
    Paths used by Mastodon instances are redirected to social.alexwlchan.net.
    """
    url = f"https://alexwlchan.net{path}"

    with urllib.request.urlopen(url, context=ssl_context) as resp:
        assert resp.getcode() == 200
        assert resp.geturl() == f"https://social.alexwlchan.net{path}"
