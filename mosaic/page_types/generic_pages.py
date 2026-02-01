"""
Models for a generic page.
"""

from typing import Any

from ._base import BaseHtmlPage


class Page(BaseHtmlPage):
    """
    A generic page which doesn't fit into another template.

    Ideally I should have very few of these.
    """

    # Allow the constructor to set an explicit URL.
    _url: str | None = None

    def __init__(self, url: str | None = None, **kwargs: Any):
        """
        Construct a new instance of Page.
        """
        super().__init__(**kwargs)
        self._url = url

    @property
    def template_name(self) -> str:
        """
        The name of HTML file used as a template for this type of page.
        """
        return "page.html"

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        if self._url is not None:
            return self._url
        else:
            assert self.md_path is not None
            assert self.src_dir is not None
            if self.md_path.name == "index.md":
                relative_path = self.md_path.parent.relative_to(self.src_dir)
            else:
                relative_path = self.md_path.relative_to(self.src_dir).with_suffix("")
            return f"/{relative_path}/".replace("./", "")
