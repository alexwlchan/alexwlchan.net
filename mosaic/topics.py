"""
Defines my topic tree.
"""

import json
from typing import Optional

from pydantic import BaseModel, Field


__all__ = ["get_topic_by_name", "Topic"]


class Topic(BaseModel):
    """
    Represents a topic on the site.
    """

    name: str
    href: str
    parent: Optional["Topic"] = None
    children: list["Topic"] = Field(default_factory=lambda: list())

    @property
    def breadcrumb(self) -> list["Topic"]:
        """
        Get the breadcrumb for a topic.
        """
        if self.parent is not None:
            return self.parent.breadcrumb + [self]
        else:
            return [self]


TOPICS_BY_NAME: dict[str, Topic] = {}


def get_topic_by_name(topic_name: str) -> Topic:
    """
    Look up a topic by name.
    """
    try:
        return TOPICS_BY_NAME[topic_name]
    except KeyError:
        rebuild_topics_by_name()
        return TOPICS_BY_NAME[topic_name]


def rebuild_topics_by_name() -> None:
    """
    Rebuild TOPICS_BY_NAME based on the current contents of `TOPICS_BY_NAME`.
    """
    global TOPICS_BY_NAME
    TOPICS_BY_NAME = {}

    with open("topics.json") as in_file:
        topic_data = json.load(in_file)

    for t in topic_data:
        if t.get("parent"):
            parent_topic = TOPICS_BY_NAME[t["parent"]]
            this_topic = Topic(name=t["name"], href=t["href"], parent=parent_topic)
            TOPICS_BY_NAME[t["name"]] = this_topic
            parent_topic.children.append(this_topic)
        else:
            TOPICS_BY_NAME[t["name"]] = Topic(name=t["name"], href=t["href"])
