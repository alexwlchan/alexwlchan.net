"""
Tests for `mosaic.models.topics`.
"""

import pytest

from mosaic.models import HasTopics, TopicNotFoundError, filter_for_topic, get_topic


class Item(HasTopics):
    """A dummy item which has a topic and a label."""

    label: str


def test_filter_for_topic() -> None:
    """
    Filtering by topic looks at the topic on a page, and all parent topics.
    """
    item1 = Item(label="1")
    item2 = Item(label="2", topics=["Python"])
    item3 = Item(label="3", topics=["Computers and code"])
    item4 = Item(label="4", topics=["Art and creativity", "Python"])
    item5 = Item(label="5", topics=["Generative art", "Interesting words"])

    items: list[Item] = [item1, item2, item3, item4, item5]

    assert filter_for_topic(items, topic_name="Python") == [item2, item4]
    assert filter_for_topic(items, topic_name="Computers and code") == [
        item2,
        item3,
        item4,
    ]
    assert filter_for_topic(items, topic_name="Art and creativity") == [item4, item5]


def test_lookup_nonexistent_topic() -> None:
    """
    Looking up a non-existent topic throws a `TopicNotFoundError`.
    """
    with pytest.raises(TopicNotFoundError):
        get_topic("Does not exist")
