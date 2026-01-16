"""
Tests for redirects.
"""

import httpx
import pytest


@pytest.mark.parametrize(
    "src, dst",
    [
        (
            "https://alexwlchan.net/2021/06/s3-deprecates-bittorrent/",
            "/2021/s3-deprecates-bittorrent/",
        ),
        ("https://til.alexwlchan.net/", "https://alexwlchan.net/til/"),
        (
            "https://til.alexwlchan.net/animate-svg-elements-with-animate/",
            "https://alexwlchan.net/til/2024/animate-svg-elements-with-animate/",
        ),
        ("https://alexwlchan.net/all-posts", "/articles/"),
        ("https://alexwlchan.net/all-posts/", "/articles/"),
    ],
)
def test_redirect(src: str, dst: str) -> None:
    """
    Pages are redirected correctly.
    """
    resp = httpx.get(src)
    assert resp.status_code == 301
    assert resp.headers["location"] == dst

    resp = httpx.get(src, follow_redirects=True)
    assert resp.status_code == 200

    if dst.startswith("/"):
        assert resp.url == "https://alexwlchan.net" + dst
    else:
        assert resp.url == dst
