"""
Tests for `mosaic.html_page`.
"""

from pathlib import Path

import pytest

from mosaic.html_page import HtmlPage


def test_read_error_includes_filename(tmp_path: Path) -> None:
    """
    An error reading the Markdown file includes the filename.
    """
    src_dir = tmp_path / "src"
    md_path = src_dir / "example.md"

    with pytest.raises(RuntimeError, match=str(md_path)):
        HtmlPage.from_path(src_dir, md_path)
