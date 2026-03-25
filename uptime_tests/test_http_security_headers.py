"""
Test my HTTP security headers.
"""

from ssl import SSLContext
import urllib.request


def test_alexwlchan(ssl_context: SSLContext) -> None:
    """
    Test security headers for alexwlchan.net.
    """
    url = "https://alexwlchan.net"

    with urllib.request.urlopen(url, context=ssl_context) as resp:
        assert resp.headers["Content-Security-Policy"] == (
            "default-src 'self' 'unsafe-inline' https://youtube-nocookie.com "
            "https://www.youtube-nocookie.com; "
            "script-src 'self' 'unsafe-inline'; "
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
