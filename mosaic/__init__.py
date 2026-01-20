"""
Build system for alexwlchan.net.
"""

from dataclasses import dataclass
import hashlib
from pathlib import Path

from .css import create_base_css
from .fs import find_paths_under
from .html_page import HtmlPage


@dataclass
class Site:
    """
    Wraps the whole site build process.
    """

    css_path: Path
    src_dir: Path
    out_dir: Path

    def build_site(self) -> None:  # pragma: no cover
        """
        Build a complete copy of the site.
        """
        self.build_base_css_file()

        pages: list[HtmlPage] = []
        for md_path in find_paths_under(self.src_dir, suffix=".md"):
            if "_favicons" in str(md_path):
                continue
            if "_plugins" in str(md_path):
                continue

            pages.append(HtmlPage.from_path(self.src_dir, md_path))

        print(len(pages))

    @property
    def static_dir(self) -> Path:
        """
        Static output directory, where static assets are saved.
        """
        return self.out_dir / "static"

    def build_base_css_file(self) -> None:
        """
        Build the base static/style.css file for the site.

        This includes a short hash in the filename to ensure cache busting
        when the CSS changes.
        """
        base_css = create_base_css(self.css_path)

        # Using three characters of hash gives me 16^3 = 4096 bits of entropy.
        # Given I cache CSS for a year and only change it a handful of times,
        # that should be plenty.
        h = hashlib.md5(base_css.encode("utf8")).hexdigest()
        h = h[:3]

        out_path = self.static_dir / f"style.{h}.css"
        out_path.parent.mkdir(exist_ok=True, parents=True)
        out_path.write_text(base_css)

        # Clean up any old CSS files
        for f in self.static_dir.iterdir():
            if f.suffix == ".css" and f.name != out_path.name:
                f.unlink()
