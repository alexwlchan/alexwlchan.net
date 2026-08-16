"""
Tools for managing and interacting with categories.
"""

from abc import ABC
import json
from threading import Lock
from typing import Any, Optional, TypeVar

from pydantic import BaseModel, Field, field_validator


__all__ = [
    "Topic",
    "TopicNotFoundError",
    "HasTopics",
    "all_topics",
    "get_topic",
    "refresh_topics",
    "filter_for_topic",
]


class TopicNotFoundError(Exception):
    """Raised when attempting to look up a topic that does not exist."""


class Topic(BaseModel):
    """A topic is a hierarchical category on the site."""

    name: str
    href: str
    parent: Optional["Topic"] = None
    children: list["Topic"] = Field(default_factory=lambda: list())

    @property
    def breadcrumb(self) -> list["Topic"]:
        """
        Return the ancestor hierarchy leading down to this topic.
        """
        if self.parent is not None:
            return self.parent.breadcrumb + [self]
        else:
            return [self]


_TOPICS_LOCK = Lock()
_TOPICS_BY_NAME: dict[str, Topic] = {}


def get_topic(name: str) -> Topic:
    """
    Look up a single topic by name.
    """
    with _TOPICS_LOCK:
        try:
            return _TOPICS_BY_NAME[name]
        except KeyError:
            raise TopicNotFoundError(f"could not find {name!r}")


def all_topics() -> dict[str, Topic]:
    """
    Return the nested hierarchy of all topics.
    """
    with _TOPICS_LOCK:
        return dict(_TOPICS_BY_NAME)


def refresh_topics():
    """
    Rebuild the in-memory topic cache from the JSON file on-disk.
    """
    with open("topics.json") as in_file:
        topic_data = json.load(in_file)

    new_topics: dict[str, Topic] = {}

    for t in topic_data:
        name = t["name"]
        href = t["href"]
        parent_name = t.get("parent")

        if parent_name:
            parent_topic = new_topics[parent_name]
            this_topic = Topic(name=name, href=href, parent=parent_topic)
            new_topics[name] = this_topic
            parent_topic.children.append(this_topic)
        else:
            new_topics[name] = Topic(name=name, href=href)

    global _TOPICS_BY_NAME
    with _TOPICS_LOCK:
        _TOPICS_BY_NAME = new_topics


class HasTopics(BaseModel, ABC):
    """
    An abstract mixin for Pydantic models that transparently converts
    topic names into full Topic instances.
    """

    topics: list[Topic] = Field(default_factory=list)

    hidden_topics: list[str] = Field(
        default_factory=list,
        description="Topics reserved for future usage or not currently displayed.",
    )

    @field_validator("topics", mode="before")
    @classmethod
    def _coerce_topics(cls, value: Any) -> list[Topic]:
        if not isinstance(value, list):  # pragma: no cover
            raise TypeError(f"Expected a list of topics, got {type(value).__name__}")

        resolved: list[Topic] = []
        for item in value:
            if isinstance(item, str):
                resolved.append(get_topic(item))
            else:  # pragma: no cover
                raise TypeError(f"Topic items must be str, got {type(item).__name__}")

        return resolved

    def belongs_to_topic(self, topic: str | Topic) -> bool:
        """
        Check whether this item belongs directly to a topic or any of
        its subtopics.
        """
        if not self.topics:
            return False

        if not isinstance(topic, Topic):
            topic = get_topic(topic)

        if topic in self.topics:
            return True
        else:
            return any(self.belongs_to_topic(c) for c in topic.children)


T = TypeVar("T")


def filter_for_topic[T: HasTopics](items: list[T], topic_name: str) -> list[T]:
    """
    Filter a list of items to those matching a topic or its subtopics.
    """
    return [it for it in items if it.belongs_to_topic(topic_name)]


refresh_topics()
