"""
Tests for `mosaic.page_types.notes`.
"""

from datetime import datetime
from pathlib import Path


from mosaic.page_types import BreadcrumbEntry, Note


def test_note_properties(src_dir: Path) -> None:
    """
    Test the basic properties of a note.
    """
    n = Note(
        md_path=src_dir / "notes/2026/2026-02-03-example-note.md",
        src_dir=src_dir,
        date=datetime(2006, 2, 3),
        topic="Examples",
    )

    assert n.template_name == "note.html"
    assert n.url == "/notes/2026/example-note/"
    assert n.breadcrumb == [
        BreadcrumbEntry(label="Examples", href="/examples/"),
    ]
