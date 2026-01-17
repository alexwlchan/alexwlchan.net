"""
Use the picture plugin from Mosaic.

This is intended as a shim so I can call my new picture code from Jekyll,
and gradually migrate all the "interesting code" into Python.

It takes two arguments:

*   The date of the parent post (if any)
*   The key-value pairs passed to the {% picture %} plugin, as JSON

It prints an HTML string.
"""

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import templates as t
from mosaic.templates import pictures as tp


@dataclass
class StubPage:
    """Stub entry for a page."""

    date: datetime | None


if __name__ == "__main__":
    try:
        if sys.argv[1]:
            post_date: datetime | None = datetime.strptime(sys.argv[1], "%Y-%m-%d")
        else:
            post_date = None
        plugin_args = json.loads(sys.argv[2])
    except (IndexError, ValueError):
        sys.exit(f"Usage: {__file__} POST_DATE PLUGIN_ARGS_JSON")

    src_dir = Path("src")
    out_dir = Path("_site")

    env = t.get_jinja_environment(src_dir, out_dir)
    page = StubPage(post_date)

    context = {"page": page, "src_dir": src_dir, "out_dir": out_dir, "environment": env}

    print(tp.render_picture(context, **plugin_args), end="")  # type: ignore
