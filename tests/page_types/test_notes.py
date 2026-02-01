"""
Tests for `mosaic.page_types.notes`.
"""

from datetime import datetime
from pathlib import Path

import pytest

from mosaic.page_types import Note


@pytest.mark.parametrize(
    "src_path, url",
    [
        ("entertainment/2026-02-01-example.md", "/entertainment/example/"),
        ("2026-02-01-example.md", "/example/"),
    ],
)
def test_url(src_dir: Path, src_path: str, url: str) -> None:
    """
    The URL of a note matches the path within the source directory.
    """
    n = Note(
        layout="note",
        md_path=src_dir / src_path,
        src_dir=src_dir,
        date=datetime(2006, 2, 1),
    )
    assert n.url == url
