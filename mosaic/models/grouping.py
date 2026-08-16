"""
Items that can be grouped into alternating visual blocks on a page.
"""

from abc import ABC
from collections.abc import Iterator
import itertools
from typing import Literal, TypedDict, TypeVar


__all__ = ["Groupable", "group_items_for_layout"]


class Groupable(ABC):
    """
    Base class for items that can be shown in a layout group of cards/lists.
    """

    # Whether the item should be excluded from layout output.
    is_excluded: bool

    # Whether the item should be displayed as a card.
    is_featured: bool


T = TypeVar("T")


class ItemGroup[T: Groupable](TypedDict):
    """
    A grouped collection of items organised for page layout.
    """

    type: Literal["cards", "list"]
    entries: list[T]


def group_items_for_layout[T: Groupable](items: list[T]) -> Iterator[ItemGroup[T]]:
    """
    Group a list of items into alternating visual blocks for page layout.

    Pairs items flagged as cards into groups of 2, interspersed with runs
    of at least 3 list items.
    """
    result: list[ItemGroup[T]] = []
    card_items: list[T] = []
    list_items: list[T] = []

    for it in items:
        if it.is_excluded:
            continue

        if it.is_featured:
            card_items.append(it)
        else:
            list_items.append(it)

        if len(card_items) != 2:
            continue

        result.append({"type": "cards", "entries": card_items})
        card_items = []

        if len(list_items) >= 3:
            result.append({"type": "list", "entries": list_items})
            list_items = []

    # Flush remaining items, putting cards before list overflow
    if card_items:
        result.append({"type": "cards", "entries": card_items})

    if list_items:
        result.append({"type": "list", "entries": list_items})

    # Group consecutive groups of the same layout type.
    for group_type, groups in itertools.groupby(result, key=lambda g: g["type"]):
        yield {
            "type": group_type,
            "entries": list(itertools.chain(*(g["entries"] for g in groups))),
        }
