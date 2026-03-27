"""
Check that my alternative domains and subdomains redirect to my main site.
"""

from ssl import SSLContext
import urllib.request

import pytest


@pytest.mark.parametrize(
    "src, dst",
    [
        # Sub-paths under HTTP are redirected to HTTPS
        ("http://alexwlchan.net/contact/", "https://alexwlchan.net/contact/"),
    ],
)
def test_redirects(ssl_context: SSLContext, src: str, dst: str) -> None:
    """
    My website redirects from HTTP to HTTPS.
    """
    with urllib.request.urlopen(src, context=ssl_context) as resp:
        assert resp.getcode() == 200
        assert resp.geturl() == dst


@pytest.mark.parametrize(
    "url",
    [
        "http://alexwlchan.net",
        "https://www.alexwlchan.net",
        "https://alexwlchan.com",
        "http://alexwlchan.com",
        "https://alexwlchan.co.uk",
        "http://alexwlchan.co.uk",
    ],
)
def test_alternative_domains(ssl_context: SSLContext, url: str) -> None:
    """
    Alternative domains are redirected to my main website.
    """
    with urllib.request.urlopen(url, context=ssl_context) as resp:
        assert resp.getcode() == 200
        assert resp.geturl() == "https://alexwlchan.net/"
