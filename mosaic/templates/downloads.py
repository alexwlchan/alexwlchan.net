"""
A Jekyll tag to show file downloads.

I don't use this much but it's a simple plugin and easier to migrate
from Jekyll than to remove.

TODO: Should I just get rid of this plugin?
"""

import os
import re
from typing import Any

from jinja2 import pass_context
from jinja2.runtime import Context

from mosaic.text import assert_is_invariant_under_markdown

from .jinja_extensions import KwargsExtensionBase
from .pictures import render_picture


class DownloadExtension(KwargsExtensionBase):
    """
    Defines the {% download %} tag to render file downloads.
    """

    tags = {"download"}

    @pass_context
    def render_html(self, *args: Any, **kwargs: Any) -> str:
        """
        Render the slide tag.
        """
        html = render_download(*args, **kwargs)
        assert_is_invariant_under_markdown(html)
        return html


def render_download(context: Context, filename: str, caller: Any) -> str:
    """
    Create the HTML to display a download.
    """
    icon_name = choose_icon(filename)
    year = context["page"].date.year

    picture_html = render_picture(
        context,
        filename=f"download_{icon_name}.png",
        parent="/images/icons",
        width=64,
        alt="",
    )

    # Add the data-proofer-ignore tag
    picture_html = re.sub(r"<img([^>]+)>", r"<img\1 data-proofer-ignore>", picture_html)

    return (
        '<style type="x-text/scss">\n'
        '  @use "components/download";\n'
        "</style>\n"
        f'<a href="/files/{year}/{filename}" class="download">'
        + picture_html
        + f" {filename}</a>"
    )


def choose_icon(filename: str) -> str:
    """
    Choose the icon based on the filename being downloaded.
    """
    match os.path.splitext(filename)[1]:
        case ".js":
            return "javascript"
        case ".py":
            return "python"
        case ".rb":
            return "ruby"
        case ".zip":
            return "zip"
        case _:
            raise ValueError(f"Unrecognised file extension: {filename}")
