"""
Tests for `mosaic.templates`.
"""

import pytest

from mosaic.templates import absolute_url


@pytest.mark.parametrize(
    "path, url",
    [("/", "https://alexwlchan.net/"), ("example", "https://alexwlchan.net/example")],
)
def test_absolute_url(path: str, url: str) -> None:
    """
    Tests for `absolute_url`.
    """
    assert absolute_url(path) == url
