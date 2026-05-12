"""
Tests for redirects.
"""

from ssl import SSLContext
import urllib.request

import pytest


@pytest.mark.parametrize(
    "src, dst",
    [
        (
            "https://alexwlchan.net/2021/06/s3-deprecates-bittorrent/",
            "/2021/s3-deprecates-bittorrent/",
        ),
        ("https://til.alexwlchan.net/", "https://alexwlchan.net/notes/"),
        (
            "https://til.alexwlchan.net/animate-svg-elements-with-animate/",
            "https://alexwlchan.net/notes/2024/animate-svg-elements-with-animate/",
        ),
        ("https://alexwlchan.net/all-posts", "/articles/"),
        ("https://alexwlchan.net/all-posts/", "/articles/"),
    ],
)
def test_redirect(ssl_context: SSLContext, src: str, dst: str) -> None:
    """
    Pages are redirected correctly.
    """
    if dst.startswith("/"):
        expected_url = "https://alexwlchan.net" + dst
    else:
        expected_url = dst

    with urllib.request.urlopen(src, context=ssl_context) as resp:
        assert resp.getcode() == 200
        assert resp.geturl() == expected_url
