"""
Tests for `mosaic.page_types.topic_pages`.
"""

from pathlib import Path


from mosaic.page_types import TopicPage


def test_topic_page_properties(src_dir: Path) -> None:
    """
    Test the basic properties of a TopicPage.
    """
    tp = TopicPage(
        md_path=src_dir / "topics/python.md",
        src_dir=src_dir,
        title="Python",
    )

    assert tp.template_name == "topic.html"
    assert tp.url == "/python/"
    assert tp.breadcrumb == []
