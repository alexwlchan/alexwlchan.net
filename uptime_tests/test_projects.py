"""
Tests for Git repositories served under /projects/.
"""

from ssl import SSLContext
import urllib.request

from chives.fetch import fetch_url
import pytest


def test_file_page() -> None:
    """
    Loading an individual file works correctly.
    """
    resp = fetch_url("https://alexwlchan.net/projects/chives/files/src/chives/media.py")
    assert b"<pre>" in resp
    assert b"Functions for interacting with images/videos." in resp


@pytest.mark.parametrize(
    "path",
    [
        "src/chives/",
        "doesnotexist.txt",
    ],
)
def test_redirect(ssl_context: SSLContext, path: str) -> None:
    """
    If you look up a file or folder under /files/ that doesn't exist,
    you get redirect back to the /files/ browser with an error.
    """
    url = f"https://alexwlchan.net/projects/chives/files/{path}"

    with urllib.request.urlopen(url, context=ssl_context) as resp:
        assert resp.getcode() == 200
        assert (
            resp.geturl()
            == f"https://alexwlchan.net/projects/chives/files/?missing={path}"
        )
