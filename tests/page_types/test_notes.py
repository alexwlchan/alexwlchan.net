"""
Tests for `mosaic.page_types.notes`.
"""

from datetime import datetime
from pathlib import Path

import pytest

from mosaic.page_types import BreadcrumbEntry, Note


def test_note_properties(src_dir: Path) -> None:
    """
    Test the basic properties of a note.
    """
    n = Note(
        md_path=src_dir / "notes/2026/2026-02-03-example-note.md",
        src_dir=src_dir,
        date=datetime(2026, 2, 3),
        topics=["Python"],
    )

    assert n.template_name == "note.html"
    assert n.url == "/notes/2026/example-note/"
    assert n.breadcrumb == [
        BreadcrumbEntry(label="Computers and code", href="/computers-and-code/"),
        BreadcrumbEntry(label="Python", href="/python/"),
    ]


def test_note_must_have_topics(src_dir: Path) -> None:
    """
    Creating a note with no topics is a ValueError.
    """
    with pytest.raises(ValueError, match="no topics"):
        Note(
            md_path=src_dir / "notes/2026/2026-02-03-example-note.md",
            src_dir=src_dir,
            date=datetime(2026, 2, 3),
            topics=[],
        )


@pytest.mark.parametrize(
    "path",
    [
        "_articles/2001/2001-01-01-example.md",
        "_notes/2010/2001-01-01-example.md",
        "_notes/2001/2010-01-01-example.md",
        "_notes/2001/example.md",
        "2001/2001-01-01-example.md",
    ],
)
def test_invalid_note_path(src_dir: Path, path: str) -> None:
    """
    Note paths that don't match the metadata are rejected.
    """
    with pytest.raises(ValueError, match="wrong path"):
        Note(
            md_path=src_dir / path,
            src_dir=src_dir,
            date=datetime(2001, 1, 1),
            topics=["Example topic"],
        )
