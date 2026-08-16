"""
Tests for `templates.grouping`.
"""

from pydantic import BaseModel
import pytest

from mosaic.models import Groupable, group_items_for_layout


class Item(Groupable, BaseModel):
    """Dummy item for use in grouping tests."""

    label: str = ""


@pytest.mark.parametrize(
    "items",
    [
        [True, True, True],
        [True, True, True, True],
        [False, False, False, True, True, False],
    ],
)
def test_groups_remaining_items(items: list[bool]) -> None:
    """
    After doing the first pass, if all the leftover posts are remaining,
    they get merged with the final group.
    """
    # This is a regression test for a bug on the /images-and-videos/
    # page, where two 'remaining' posts were leftover and separated
    # from the rest of the group.
    result = group_items_for_layout(
        [Item(is_featured=f, is_excluded=False) for f in items]
    )
    groups = list(result)

    for i in range(len(groups) - 1):
        assert groups[i]["type"] != groups[i + 1]["type"]


def test_excludes_items() -> None:
    """
    If an item is marked as "excluded", it's not included in the groups.
    """
    items = [
        Item(label="item0", is_featured=True, is_excluded=True),
        Item(label="item1", is_featured=True, is_excluded=True),
        Item(label="item2", is_featured=True, is_excluded=False),
        Item(label="item3", is_featured=True, is_excluded=False),
        Item(label="item4", is_featured=True, is_excluded=True),
        Item(label="item5", is_featured=True, is_excluded=False),
    ]
    groups = list(group_items_for_layout(items))

    assert groups == [{"type": "cards", "entries": [items[2], items[3], items[5]]}]
