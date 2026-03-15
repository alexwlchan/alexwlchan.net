"""
Read-only browser for Git repos. This file exports a Flask blueprint that
can be registered for different repos.
"""

from pathlib import Path
from typing import Any

from flask import abort, Flask, render_template, url_for

from mosaic.page_types import BreadcrumbEntry, Page
from mosaic.templates import get_jinja_environment


PROJECTS = {
    "chives": Path.home() / "repos/chives/.git",
    "javascript-data-files": Path.home() / "repos/javascript-data-files/.git",
}


class ProjectPage(Page):
    """
    A page for a specific project.
    """

    def __init__(self, url: str | None = None, **kwargs: Any):
        """
        Construct a new instance of ProjectPage.
        """
        super().__init__(**kwargs)
        self._url = url

    def breadcrumb(self) -> list[BreadcrumbEntry]:
        """
        The breadcrumb trail for this page.
        """
        return [
            BreadcrumbEntry(label="projects", href="/projects/"),
            BreadcrumbEntry(label=self.title, href=f"/projects/{self.title}/"),
        ]


def render_project_page(project: str) -> str:
    """
    Returns the homepage for a project.
    """
    if project not in PROJECTS:
        abort(404)

    page = ProjectPage(url=url_for("project_page", project=project), title=project)

    return render_template("gitweb/project.html", project=project, page=page)


def create_app() -> Flask:
    """
    Create an instance of the Git browser app.
    """
    app = Flask(__name__)
    app.jinja_env = get_jinja_environment()  # type: ignore
    app.jinja_env.globals.update(
        {
            "site": {
                "url": "https://alexwlchan.net",
                "title": "alexwlchan",
                "description": "Alex Chan's personal website",
            },
            "css_url": "https://alexwlchan.net/static/style.css",
            "enable_analytics": False,
        }
    )

    @app.route("/<project>/")
    def project_page(project: str) -> str:
        return render_project_page(project)

    return app
