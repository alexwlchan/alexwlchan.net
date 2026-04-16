"""
Models for a topic page.
"""

from pathlib import Path

from mosaic.topics import get_topic_by_name

from ._base import BaseHtmlPage, BreadcrumbEntry


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
        return get_topic_by_name(self.title).href

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label=t.name, href=t.href)
            for t in get_topic_by_name(self.title).breadcrumb[:-1]
        ]
