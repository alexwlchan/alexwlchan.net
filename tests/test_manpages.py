"""
Tests for `mosaic.manpages`.
"""

from mosaic.manpages import get_manpage_contents, find_manpage_urls


def test_get_manpage_contents() -> None:
    """
    Tests for `get_manpage_contents`.
    """
    html = get_manpage_contents("1", "xargs")

    assert "The <b>xargs</b> utility reads space, tab, newline" in html
    assert "executes <u>utility</u> with the strings" in html


def test_get_manpage_contents_expands_urls() -> None:
    """
    If there are HTTP URLs in the man page, they get turned into <a> tags.
    """
    html = get_manpage_contents("1", "file")

    assert '<a href="https://bugs.astron.com/">https://bugs.astron.com/</a>' in html


def test_find_manpage_urls() -> None:
    """
    Tests for `find_manpage_urls`.
    """
    assert list(find_manpage_urls('<a href="/man/man1/xargs.html">xargs</a>')) == [
        ("1", "xargs")
    ]
