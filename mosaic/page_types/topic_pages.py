"""
Models for a topic page.
"""

from pathlib import Path

from mosaic.models import BreadcrumbEntry, Topic, get_topic

from ._base import BaseHtmlPage


class TopicPage(BaseHtmlPage):
    """
    A page which shows you everything I've published about a topic.
    """

    template_name: str = "topic.html"

    # Properties inherited from BaseHtmlPage which are guaranteed
    # to be set for a TopicPage.
    md_path: Path
    src_dir: Path

    @property
    def topic(self) -> Topic:
        """
        The Topic this page is describing.
        """
        return get_topic(name=self.title)

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return self.topic.href

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return self.topic.breadcrumb[:-1]
