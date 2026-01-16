"""
Test my error pages.
"""

import httpx


def test_unknown_url_is_404() -> None:
    """
    Loading a page that doesn't exist returns my 404 page.
    """
    resp = httpx.get("https://alexwlchan.net/doesnotexist/")

    assert resp.status_code == 404
    assert "404 Not Found" in resp.text


def test_removed_page_is_410() -> None:
    """
    Loading a page that I removed gets my 410 Gone page.
    """
    resp = httpx.get("https://alexwlchan.net/2015/bbfc-podcast/")

    assert resp.status_code == 410
    assert "410 Gone" in resp.text


def test_wp_login_is_400() -> None:
    """
    Loading my non-existent WordPress login returns a minimal 400 page.
    """
    resp = httpx.get("https://alexwlchan.net/wp-login.php")

    assert resp.status_code == 400
    assert resp.text == "400 Bad Request"
