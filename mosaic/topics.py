"""
Every page can have at most one topic. Topics can be nested (but ideally
not too much).
"""

from typing import Optional

from pydantic import BaseModel, Field

from .page_types import BreadcrumbEntry, BaseHtmlPage, TopicPage


class Topic(BaseModel):
    """
    Represents a single topic.
    """

    label: str
    url: str | None = None
    parent: Optional["Topic"] = None
    children: list["Topic"] = Field(default_factory=lambda: list())

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        Create a breadcrumb entry that leads to this topic.
        """
        if self.parent is not None:
            parent_entries = self.parent.breadcrumb
        else:
            parent_entries = []

        assert self.url is not None
        return parent_entries + [BreadcrumbEntry(label=self.label, href=self.url)]


def build_topic_tree(pages: list[BaseHtmlPage]) -> dict[str, Topic]:
    """
    Build a tree of topics from all the HTML pages.
    """
    # Build a map (name) -> Topic
    topics: dict[str, Topic] = {}
    for p in pages:
        if isinstance(p, TopicPage):
            topics[p.title] = Topic(label=p.title, url=p.url)

        if p.topic is not None and p.topic not in topics:
            topics[p.topic] = Topic(label=p.topic)

    # Now construct the hierarchy information for each topic, adding
    # parent/child relationships as necessary.
    #
    # I assume I'm not going to create loops or unusable constructions here.
    for p in pages:
        if not isinstance(p, TopicPage):
            continue

        if p.topic is not None:
            this_topic = topics[p.title]
            parent_topic = topics[p.topic]

            this_topic.parent = parent_topic
            parent_topic.children.append(this_topic)

    # Now go through all the pages, and insert a breadcrumb based on
    # the topic it describes.
    for p in pages:
        if p.topic is not None:
            assert p.breadcrumb == [], p
            p.breadcrumb = topics[p.topic].breadcrumb

    # Return a list of top-level topics, i.e. topics with no parent.
    return {t.label: t for t in topics.values() if not t.parent}
