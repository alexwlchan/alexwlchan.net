"""
Provide a rendered view of macOS man pages.

This is a thin wrapper around the template, and mostly exists to ensure
my clean-up logic doesn't delete any manpages.
"""

from pathlib import Path

from ._base import BaseHtmlPage, BreadcrumbEntry


class ManPage(BaseHtmlPage):
    """
    A rendered view of a macOS man page.
    """

    template_name: str = "manpage.html"
    section: str
    command_name: str

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:  # pragma: no cover
        """
        The breadcrumb trail for this page.
        """
        raise NotImplementedError

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/man/man{self.section}/{self.command_name}.html"

    def out_path(self, out_dir: Path) -> Path:
        """
        Return the path where this HTML file should be written.
        """
        return out_dir / self.url.strip("/")
