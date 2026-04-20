"""
Models for project/Git repo pages.
"""

from pathlib import Path
from typing import Self, TypedDict

from pydantic import model_validator

from mosaic.git import Commit, GitRepository
from ._base import BaseHtmlPage, BreadcrumbEntry


class BaseProjectPage(BaseHtmlPage):
    """
    Root definition for all pages in the /projects/ folder.
    """

    repo: GitRepository

    @property
    def name(self) -> str:
        """
        The human-readable name of this project.
        """
        return self.repo.name

    @property
    def slug(self) -> str:
        """
        The URL slug for this project under /projects/.
        """
        return self.repo.name


class ProjectHomepage(BaseProjectPage):
    """
    The homepage/README of a project.
    """

    template_name: str = "projects/homepage.html"

    archive_url: str

    @model_validator(mode="after")
    def set_title(self) -> Self:
        """
        Set the title of the page to be the commit summary and commit ID.
        """
        self.title = self.name
        return self

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/projects/{self.slug}/"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [BreadcrumbEntry(label="projects", href="/projects/")]


class ProjectLog(BaseProjectPage):
    """
    The list of commits for a project.
    """

    template_name: str = "projects/log.html"
    title: str = "Log"

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/projects/{self.slug}/commits/"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label="projects", href="/projects/"),
            BreadcrumbEntry(label=self.name, href=f"/projects/{self.slug}/"),
        ]


class ChangedFile(TypedDict):
    """
    A changed file.
    """

    path: str
    diff: str
    is_binary: bool


class ProjectCommit(BaseProjectPage):
    """
    A single commit for a project.
    """

    template_name: str = "projects/commit.html"

    commit: Commit

    @model_validator(mode="after")
    def set_title(self) -> Self:
        """
        Set the title of the page to be the commit summary and commit ID.
        """
        self.title = f"{self.commit.summary} – {self.commit.id[:7]} – {self.name}"
        return self

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/projects/{self.slug}/commits/{self.commit.id}/"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label="projects", href="/projects/"),
            BreadcrumbEntry(label=self.name, href=f"/projects/{self.slug}/"),
            BreadcrumbEntry(label="log", href=f"/projects/{self.slug}/commits/"),
        ]


class ProjectTags(BaseProjectPage):
    """
    A list of tags/releases for a project.
    """

    template_name: str = "projects/tags.html"

    @model_validator(mode="after")
    def set_title(self) -> Self:
        """
        Set the title of the page to be "Tags" and the project name.
        """
        self.title = f"Tags – {self.name}"
        return self

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/projects/{self.slug}/tags/"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label="projects", href="/projects/"),
            BreadcrumbEntry(label=self.name, href=f"/projects/{self.slug}/"),
        ]


class ProjectTree(BaseProjectPage):
    """
    A tree of all the files for a project.
    """

    template_name: str = "projects/tree.html"

    @model_validator(mode="after")
    def set_title(self) -> Self:
        """
        Set the title of the page to be "Files" and the project name.
        """
        self.title = f"Files – {self.name}"
        return self

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/projects/{self.slug}/files/"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label="projects", href="/projects/"),
            BreadcrumbEntry(label=self.name, href=f"/projects/{self.slug}/"),
        ]


class ProjectSingleFile(BaseProjectPage):
    """
    A rendered view of a single file.
    """

    template_name: str = "projects/single_file.html"

    file_path: Path
    file_contents: str
    file_size: int

    @model_validator(mode="after")
    def set_title(self) -> Self:
        """
        Set the title of the page to be the file path and the project name.
        """
        self.title = f"{self.file_path} – {self.name}"
        return self

    @property
    def url(self) -> str:
        """
        The output URL of this page.
        """
        return f"/projects/{self.slug}/files/{self.file_path}"

    @property
    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label="projects", href="/projects/"),
            BreadcrumbEntry(label=self.name, href=f"/projects/{self.slug}/"),
            BreadcrumbEntry(label="files", href=f"/projects/{self.slug}/files/"),
        ]

    def out_path(self, out_dir: Path) -> Path:
        """
        Return the path where this HTML file should be written.
        """
        return out_dir / (self.url.strip("/") + ".html")
