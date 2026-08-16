"""
Tests for `mosaic.text`.
"""

from mosaic import text as t


def test_find_unique_prefixes() -> None:
    """
    Test the example given for `find_unique_prefixes`.
    """
    actual = t.find_unique_prefixes({"amber", "application", "banana"})
    expected = {"amber": "am", "application": "ap", "banana": "b"}
    assert actual == expected
