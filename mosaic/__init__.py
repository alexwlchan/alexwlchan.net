"""
Build system for alexwlchan.net.
"""

import collections
from dataclasses import dataclass
import filecmp
import hashlib
from pathlib import Path
import shutil

from tqdm import tqdm

from .css import create_base_css
from .fs import find_paths_under
from .html_page import Article, HtmlPage
from .tint_colours import get_default_tint_colours, TintColours


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

        # Read all the Markdown source files.
        pages: list[HtmlPage] = []
        for md_path in find_paths_under(self.src_dir, suffix=".md"):
            if "_favicons" in str(md_path):
                continue
            if "_plugins" in str(md_path):
                continue

            pages.append(HtmlPage.from_path(self.src_dir, md_path))

        # Work out all the tint colours being used.
        tint_colours: list[TintColours] = [
            get_default_tint_colours(css_dir=self.css_path.parent)
        ]
        for p in pages:
            if p.colors is not None:
                tint_colours.append(p.colors)

        # Ordering: add a numeric "order" attribute to every article,
        # which is used for sorting on /articles/.
        articles = [p for p in pages if isinstance(p, Article)]
        for order, art in enumerate(
            sorted(articles, key=lambda art: art.date), start=1
        ):
            art.order = order

        # Tags:
        #
        #   - Work out all the tags being used
        #   - Create an HtmlPage that should be written for each page
        #
        tag_tally = collections.defaultdict(list)
        for p in pages:
            for t in p.tags:
                tag_tally[t].append(p)

        for tag_name, tagged_pages in tag_tally.items():
            pages.append(
                HtmlPage(
                    url=f"/tags/{tag_name}/".replace(":", "/"),
                    template_name="tag.html",
                    title=f"Tagged with “{tag_name}”",
                    extra_variables={"tagged_pages": tagged_pages},
                )
            )

        self.copy_static_files()

        # Create all the tint colour assets
        for tc in tint_colours:
            tc.create_assets(self.out_dir)

        # Write all the HTML files to the output directory.
        for p in pages:
            out_path = p.out_path(self.out_dir)
            out_path.parent.mkdir(exist_ok=True, parents=True)
            out_path.write_text(str(p))

        # TODO: Clean up dangling HTML files.

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

    def copy_static_files(self) -> None:  # pragma: no cover
        """
        Copy all the static files from the src to the dst directory.
        """
        static_files = []

        for src_p in find_paths_under(self.src_dir):
            if src_p.suffix == ".md" and "_files" not in src_p.parts:
                continue

            if src_p.name.endswith("atom.xml"):
                continue

            if src_p.is_relative_to(self.src_dir / "_images"):
                static_files.append(
                    (
                        src_p,
                        self.out_dir
                        / "images"
                        / src_p.relative_to(self.src_dir / "_images"),
                    )
                )
            elif src_p.is_relative_to(self.src_dir / "_files"):
                static_files.append(
                    (
                        src_p,
                        self.out_dir
                        / "files"
                        / src_p.relative_to(self.src_dir / "_files"),
                    )
                )
            else:
                static_files.append(
                    (src_p, self.out_dir / src_p.relative_to(self.src_dir))
                )

        with tqdm(desc="static files", total=len(static_files)) as pbar:
            for src_p, out_p in static_files:
                if not out_p.exists() or not filecmp.cmp(src_p, out_p, shallow=False):
                    out_p.parent.mkdir(exist_ok=True, parents=True)
                    shutil.copyfile(src_p, out_p)

                pbar.update(1)
