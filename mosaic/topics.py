"""
Every page can have at most one topic. Topics can be nested (but ideally
not too much).
"""

from typing import Optional

from pydantic import BaseModel, Field

from .page_types import BreadcrumbEntry, BaseHtmlPage, BookReview, TopicPage


class Topic(BaseModel):
    """
    Represents a single topic.
    """

    label: str
    url: str | None = None
    parent: Optional["Topic"] = None
    children: list["Topic"] = Field(default_factory=lambda: list())
    pages_in_topic: list[BaseHtmlPage] = Field(default_factory=lambda: list())

    def __repr__(self) -> str:
        """
        Returns a debugging representation of this topic.
        """
        return (
            f"<Topic label={self.label!r} url={self.url!r} "
            "#pages={len(self.pages_in_topic)}>"
        )

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        Create a breadcrumb entry that leads to this topic.
        """
        if self.parent is not None:
            parent_entries = self.parent.breadcrumb
        else:
            parent_entries = []

        return parent_entries + [BreadcrumbEntry(label=self.label, href=self.url)]


def build_topic_tree(pages: list[BaseHtmlPage]) -> dict[str, Topic]:
    """
    Build a tree of topics from all the HTML pages.
    """
    # 1. Build a map (name) -> Topic
    all_topics: dict[str, Topic] = {}
    for p in pages:
        if isinstance(p, TopicPage):
            all_topics[p.title] = Topic(label=p.title, url=p.url)
            assert len(p.topics) <= 1

            if p.topics:
                parent_topic_name = p.topics[0]
                if parent_topic_name not in all_topics:
                    all_topics[parent_topic_name] = Topic(label=parent_topic_name)

        else:
            for t in p.topics:
                if t not in all_topics:
                    all_topics[t] = Topic(label=t)

    # Create an "Everything else" topic; I'll do something with this later.
    all_topics["Everything else"] = Topic(label="Everything else")

    # 2. Construct the hierarchy information for each topic, adding
    # parent/child relationships as necessary.
    #
    # I assume I'm not going to create loops or unusable constructions here.
    for p in pages:
        if not isinstance(p, TopicPage):
            continue

        for t in p.topics:
            this_topic = all_topics[p.title]
            parent_topic = all_topics[t]

            this_topic.parent = parent_topic
            parent_topic.children.append(this_topic)

    # 3. Create a list of pages attached to each topic.
    #
    # These cascade upwards, so a topic T includes:
    #
    #   - any page where T is a topic, or
    #   - any page where a child of T is a topic
    #
    for p in pages:
        if isinstance(p, TopicPage):
            continue

        for t in p.topics:
            topic = all_topics[t]
            while True:
                topic.pages_in_topic.append(p)
                if topic.parent:
                    topic = topic.parent
                else:
                    break

        if not p.topics and not isinstance(p, BookReview):
            all_topics["Everything else"].pages_in_topic.append(p)

    return all_topics
