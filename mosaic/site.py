"""
Build system for alexwlchan.net.
"""

import collections
from dataclasses import dataclass
from datetime import datetime, timezone
import filecmp
import hashlib
import heapq
import itertools
from pathlib import Path
import shutil

from jinja2 import Environment
from tqdm import tqdm
import yaml

from .css import create_base_css
from .fs import find_paths_under
from .html_page import Article, HtmlPage
from .templates import get_jinja_environment
from .text import find_unique_prefixes
from .tint_colours import get_default_tint_colours, TintColours


@dataclass
class Site:
    """
    Wraps the whole site build process.
    """

    css_path: Path
    src_dir: Path
    out_dir: Path

    def build_site(self, incremental: bool = False) -> bool:  # pragma: no cover
        """
        Build a complete copy of the site.

        Returns True if the build succeeded, False if there were errors.
        """
        pages = self.read_markdown_source_files()

        # Work out all the tint colours being used.
        tint_colours: list[TintColours] = [
            get_default_tint_colours(css_dir=self.css_path.parent)
        ]
        for p in pages:
            if p.colors is not None:
                tint_colours.append(p.colors)

        # Ordering: add a numeric "order" attribute to every article,
        # which is used for sorting on /articles/.
        articles = sorted(
            (p for p in pages if isinstance(p, Article)), key=lambda art: art.date
        )
        for order, art in enumerate(articles, start=1):
            art.order = order

        # Article cards: pick a short name for every article card.
        #
        # These filenames are repeated many times on the global articles page,
        # so they should be as short as possible.
        #
        # For example, "digital-decluttering" could become "di".
        articles_with_cards = itertools.groupby(
            (art for art in articles if art.card_path), key=lambda art: art.date.year
        )
        for year, articles_that_year_gen in articles_with_cards:
            articles_that_year = list(articles_that_year_gen)

            # Prefix each post with the month, its slug, and delete hyphens.
            slugs = {
                art: f"{art.date.month}{art.slug}".replace("-", "")
                for art in articles_that_year
            }
            prefixes = find_unique_prefixes(set(slugs.values()))

            for art in articles_that_year:
                art.card_short_name = prefixes[slugs[art]]

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
            if ":" in tag_name:
                namespace, tag_name = tag_name.split(":")
            else:
                namespace, tag_name = "", tag_name

            tag_descriptions = yaml.safe_load(
                (self.src_dir / "_data/tag_descriptions.yml").read_text()
            )

            pages.append(
                HtmlPage(
                    url=f"/tags/{namespace}/{tag_name}/".replace("//", "/").replace(
                        " ", "-"
                    ),
                    template_name="tag.html",
                    title=f"Tagged with “{tag_name}”",
                    extra_variables={
                        "tagged_pages": tagged_pages,
                        "namespace": namespace,
                        "tag_name": tag_name,
                        "tag_description": tag_descriptions.get(tag_name),
                    },
                )
            )

        # Write the CSS file.
        css_url = self.build_base_css_file()

        # Create the Jinja2 environment.
        # TODO(2026-01-21): Figure out how to handle global varibales better.
        env = get_jinja_environment(self.src_dir, self.out_dir)
        env.globals.update(
            {
                "css_url": css_url,
                "environment": "production",
                "site": {
                    "title": "alexwlchan",
                    "description": "Alex Chan's personal website",
                    "url": "https://alexwlchan.net",
                    "data": {
                        "elsewhere": yaml.safe_load(
                            open(self.src_dir / "_data/elsewhere.yml")
                        ),
                        "popular_tags": heapq.nlargest(
                            25,
                            tag_tally.keys(),
                            lambda tag_name: len(tag_tally[tag_name]),
                        ),
                        "tag_tally": tag_tally,
                    },
                    "articles": articles,
                    "pages": pages,
                    "email": "alex@alexwlchan.net",
                    "time": datetime.now(tz=timezone.utc),
                },
            }
        )

        if not incremental:
            self.copy_static_files()

        # Create all the tint colour assets
        for tc in tint_colours:
            tc.create_assets(self.out_dir)

        written_html_paths = set()

        if not incremental:
            pages = tqdm(pages, desc="writing html")  # type: ignore

        for pg in pages:
            try:
                out_path = pg.write(env, out_dir=self.out_dir)
                written_html_paths.add(out_path)
            except Exception as exc:  # pragma: no cover
                print(f"error writing {pg!r}: {exc}")
                raise

        # Render the RSS feeds.
        #
        # This must occur after generating the pages, so the `html_content`
        # attribute is populated.
        self.generate_rss_feeds(
            env, articles, tils=[p for p in pages if p.layout == "til"]
        )

        # Clean up HTML files that weren't written as part of this build;
        # this usually indicates a renamed or deleted page.
        for pth in find_paths_under(self.out_dir, suffix=".html"):  # pragma: no cover
            if "files" in pth.parts or "fun-stuff" in pth.parts:
                continue

            if pth in written_html_paths:
                continue

            print(f"delete stale HTML file: {pth}")
            pth.unlink()

        return True

    def read_markdown_source_files(self) -> list[HtmlPage]:
        """
        Read all the Markdown source files.
        """
        pages = []

        for md_path in find_paths_under(self.src_dir, suffix=".md"):
            if "_plugins" in str(md_path):
                continue

            pages.append(HtmlPage.from_path(self.src_dir, md_path))

        return pages

    @property
    def static_dir(self) -> Path:
        """
        Static output directory, where static assets are saved.
        """
        return self.out_dir / "static"

    def build_base_css_file(self) -> str:
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

        return "/" + str(out_path.relative_to(self.out_dir))

    def copy_static_files(self) -> None:  # pragma: no cover
        """
        Copy all the static files from the src to the dst directory.
        """
        static_files = []

        for src_p in find_paths_under(self.src_dir):
            if src_p.suffix == ".md" and "_files" not in src_p.parts:
                continue

            if any(
                p in src_p.parts
                for p in (
                    "_data",
                    "_includes",
                    "_layouts",
                    "_plugin_tests",
                    "_plugins",
                    "_scss",
                )
            ):
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

    def generate_rss_feeds(
        self, env: Environment, articles: list[Article], tils: list[HtmlPage]
    ) -> None:
        """
        Generate the RSS feeds for the site.
        """
        atom_template = env.get_template("atom.xml")
        atom_xml = atom_template.render(articles=articles)
        (self.out_dir / "atom.xml").write_text(atom_xml)

        til_atom_template = env.get_template("til_atom.xml")
        til_atom_xml = til_atom_template.render(tils=tils)
        (self.out_dir / "til/atom.xml").write_text(til_atom_xml)
