"""
Tests for `mosaic.page_types.manpages`.
"""

from pathlib import Path


from mosaic.page_types import ManPage


def test_page_properties(out_dir: Path) -> None:
    """
    Test the basic properties of a page.
    """
    p = ManPage(
        section="1",
        command_name="xargs",
        content="xargs – construct argument list(s) and execute utility",
    )

    assert p.template_name == "manpage.html"
    assert p.url == "/man/man1/xargs.html"
    assert p.out_path(out_dir) == out_dir / "man/man1/xargs.html"
