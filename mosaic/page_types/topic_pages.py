"""
Models for a topic page.
"""

from pathlib import Path

from ._base import BaseHtmlPage, BreadcrumbEntry


def url_slug(topic_name: str) -> str:
    """
    Creates the URL slug for a topic name.
    """
    if topic_name == "Books I've read":
        return "book-reviews"
    return topic_name.lower().replace(" ", "-")


class TopicPage(BaseHtmlPage):
    """
    A page which shows you everything I've published about a topic.
    """

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a TopicPage.
    md_path: Path
    src_dir: Path

    @property
    def template_name(self) -> str:
        """
        The name of HTML file used as a template for this type of page.
        """
        return "topic.html"

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        slug = url_slug(self.title)
        return f"/{slug}/"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return []
