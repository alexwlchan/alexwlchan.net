"""
Test my error pages.
"""

from ssl import SSLContext
import urllib.request

import pytest


def test_error_page(ssl_context: SSLContext) -> None:
    """
    Loading a page that doesn't exist returns my 404 page.
    """
    url = "https://alexwlchan.net/doesnotexist/"

    with pytest.raises(urllib.error.HTTPError) as excinfo:
        urllib.request.urlopen(url, context=ssl_context)

    assert excinfo.value.code == 404
    assert b"404 Not Found" in excinfo.value.read()
    excinfo.value.close()


def test_removed_page_is_410(ssl_context: SSLContext) -> None:
    """
    Loading a page that I removed gets my 410 Gone page.
    """
    url = "https://alexwlchan.net/2015/bbfc-podcast/"

    with pytest.raises(urllib.error.HTTPError) as excinfo:
        urllib.request.urlopen(url, context=ssl_context)

    assert excinfo.value.code == 410
    assert b"410 Gone" in excinfo.value.read()
    excinfo.value.close()


def test_wp_login_is_400(ssl_context: SSLContext) -> None:
    """
    Loading my non-existent WordPress login returns a minimal 400 page.
    """
    url = "https://alexwlchan.net/wp-login.php"

    with pytest.raises(urllib.error.HTTPError) as excinfo:
        urllib.request.urlopen(url, context=ssl_context)

    assert excinfo.value.code == 400
    assert excinfo.value.read() == b"400 Bad Request"
    excinfo.value.close()
