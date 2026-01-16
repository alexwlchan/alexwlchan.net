"""
Check that my alternative domains and subdomains redirect to my main site.
"""

import httpx
import pytest


@pytest.mark.parametrize(
    "src, dst",
    [
        # Sub-paths under HTTP are redirected to HTTPS
        ("http://alexwlchan.net/contact/", "https://alexwlchan.net/contact/"),
    ],
)
def test_redirects(src: str, dst: str) -> None:
    """
    My website redirects from HTTP to HTTPS.
    """
    resp = httpx.get(src)

    assert resp.status_code == 308
    assert resp.headers["location"] == dst


@pytest.mark.parametrize(
    "status_code, url",
    [
        (308, "http://alexwlchan.net"),
        (301, "https://www.alexwlchan.net"),
        (301, "https://alexwlchan.com"),
        (308, "http://alexwlchan.com"),
        (301, "https://alexwlchan.co.uk"),
        (308, "http://alexwlchan.co.uk"),
    ],
)
def test_alternative_domains(status_code: int, url: str) -> None:
    """
    Alternative domains are redirected to my main website.
    """
    resp = httpx.get(url)
    assert resp.status_code == status_code

    resp = httpx.get(url, follow_redirects=True)
    assert resp.status_code == 200
    assert resp.url == "https://alexwlchan.net/"
