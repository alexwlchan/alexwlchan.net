"""
Use the inline_svg plugin from Mosaic.
"""

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import templates as t
from mosaic.templates import slides as ts


@dataclass
class StubPage:
    """Stub entry for a page."""

    date: datetime | None
    slug: str


if __name__ == "__main__":
    try:
        post_date: datetime | None = datetime.strptime(sys.argv[1], "%Y-%m-%d")
        slug = sys.argv[2]
        plugin_args = json.loads(sys.argv[3])
    except (IndexError, ValueError):
        raise
        sys.exit(f"Usage: {__file__} POST_DATE PLUGIN_ARGS_JSON")

    src_dir = Path("src")
    out_dir = Path("_site")

    env = t.get_jinja_environment(src_dir, out_dir)
    page = StubPage(post_date, slug)

    context = {"page": page, "src_dir": src_dir, "out_dir": out_dir, "environment": env}

    print(ts.render_slide(context, **plugin_args), end="")  # type: ignore
