"""
Test my HTTP security headers.
"""

import httpx


def test_alexwlchan() -> None:
    """
    Test security headers for alexwlchan.net.
    """
    resp = httpx.get("https://alexwlchan.net")

    assert resp.headers["Content-Security-Policy"] == (
        "default-src 'self' 'unsafe-inline' https://youtube-nocookie.com "
        "https://www.youtube-nocookie.com; "
        "script-src 'self' 'unsafe-inline'; "
        "connect-src https://analytics.alexwlchan.net; "
        "img-src 'self' 'unsafe-inline' data:"
    )
    assert resp.headers["Permissions-Policy"] == (
        "geolocation=(), midi=(), notifications=(), push=(), sync-xhr=(), "
        "microphone=(), camera=(), magnetometer=(), gyroscope=(), vibrate=(), "
        "payment=()"
    )
    assert resp.headers["Referrer-Policy"] == "no-referrer-when-downgrade"
    assert (
        resp.headers["Strict-Transport-Security"]
        == "max-age=31536000; includeSubDomains"
    )
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "ALLOWALL"
    assert resp.headers["X-Xss-Protection"] == "1; mode=block"


def test_books() -> None:
    """
    Test security headers for books.alexwlchan.net.
    """
    resp = httpx.get("https://books.alexwlchan.net")

    assert resp.headers["Content-Security-Policy"] == (
        "default-src ; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "script-src 'self' 'unsafe-inline' https://unpkg.com/;connect-src https://analytics.alexwlchan.net/;"
    )
    assert resp.headers["Permissions-Policy"] == (
        "geolocation=(), midi=(), notifications=(), push=(), sync-xhr=(), "
        "microphone=(), camera=(), magnetometer=(), gyroscope=(), vibrate=(), "
        "payment=()"
    )
    assert resp.headers["Referrer-Policy"] == "no-referrer-when-downgrade"
    assert (
        resp.headers["Strict-Transport-Security"]
        == "max-age=31536000; includeSubDomains"
    )
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["X-Xss-Protection"] == "1; mode=block"
