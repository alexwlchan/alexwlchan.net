"""
Models for a topic page.
"""

from pathlib import Path

from ._base import BaseHtmlPage


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
        if self.md_path.name == "index.md":
            relative_path = self.md_path.parent.relative_to(self.src_dir)
        else:
            relative_path = self.md_path.relative_to(self.src_dir).with_suffix("")
        return f"/{relative_path}/".replace("./", "")
