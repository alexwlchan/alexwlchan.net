"""
Build system for alexwlchan.net.
"""

from collections import Counter
from datetime import datetime, timezone
import filecmp
import itertools
from pathlib import Path
import shutil

from jinja2 import Environment
from pydantic import BaseModel, Field
from tqdm import tqdm
import yaml

from . import page_types
from .css import create_base_css
from .fs import find_paths_under
from .git import GitRepository
from .page_types import (
    Article,
    BaseHtmlPage,
    BookReview,
    Note,
    Post,
    ProjectCommit,
    ProjectHomepage,
    ProjectLog,
    ProjectSingleFile,
    ProjectTags,
    ProjectTree,
    read_markdown_files,
)
from .templates import get_jinja_environment
from .text import find_unique_prefixes
from .tint_colours import get_default_tint_colours
from .topics import rebuild_topics_by_name


GIT_REPOS = [
    GitRepository(
        name="chives",
        description="Utility functions for working with my local media archives",
        repo_root=Path.home() / "repos/chives",
    )
]


class Site(BaseModel):
    """
    Wraps the whole site build process.
    """

    src_dir: Path = Path("src")
    out_dir: Path = Path("_out")

    all_pages: list[BaseHtmlPage] = Field(default_factory=lambda: list())

    time: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    @property
    def posts(self) -> list[page_types.Post]:
        """
        Return the posts on the site, sorted in decreasing date order
        (newest first).
        """
        return sorted(
            (p for p in self.all_pages if isinstance(p, Post)),
            key=lambda p: p.date,
            reverse=True,
        )

    @property
    def articles(self) -> list[page_types.Article]:
        """
        Return the articles on the site, sorted in decreasing date order
        (newest first).
        """
        return [p for p in self.posts if isinstance(p, Article)]

    @property
    def book_reviews(self) -> list[page_types.BookReview]:
        """
        Return the book reviews on the site, sorted in decreasing date order
        (newest first).
        """
        return [p for p in self.posts if isinstance(p, BookReview)]

    @property
    def notes(self) -> list[page_types.Note]:
        """
        Return the notes on the site, sorted in decreasing date order
        (newest first).
        """
        return [p for p in self.posts if isinstance(p, Note)]

    @property
    def pages(self) -> list[page_types.BaseHtmlPage]:
        """
        Return a list of pages that don't fit into another category.
        """
        return [
            p
            for p in self.all_pages
            if not isinstance(p, Article)
            and not isinstance(p, BookReview)
            and not isinstance(p, Note)
        ]

    def build_site(self, incremental: bool = False) -> bool:  # pragma: no cover
        """
        Build a complete copy of the site.

        Returns True if the build succeeded, False if there were errors.
        """
        self.time = datetime.now(tz=timezone.utc)
        self.all_pages = read_markdown_files(self.src_dir)

        # Check none of the URLs are duplicated
        counter = Counter(p.url for p in self.all_pages)
        duplicate_urls = {url: count for url, count in counter.items() if count > 1}
        assert duplicate_urls == {}, duplicate_urls

        # Work out all the tint colours being used.
        tint_colours = [get_default_tint_colours()] + [
            p.colors for p in self.all_pages if p.colors is not None
        ]

        # Ordering: add a numeric "order" attribute to every article,
        # which is used for sorting on /articles/.
        for order, art in enumerate(
            sorted(self.articles, key=lambda art: art.date), start=1
        ):
            art.order = order

        # Article cards: pick a short name for every article card.
        #
        # These filenames are repeated many times on the global articles page,
        # so they should be as short as possible.
        #
        # For example, "digital-decluttering" could become "di".
        articles_with_cards = itertools.groupby(
            (art for art in self.articles if art.card_path),
            key=lambda art: art.date.year,
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

        # Write the CSS file.
        css_url = self.build_base_css_file()

        # Create the Jinja2 environment.
        # TODO(2026-01-21): Figure out how to handle global varibales better.
        env = get_jinja_environment(self.src_dir, self.out_dir)

        env.globals.update(
            {
                "css_url": css_url,
                "site": self,
                "all_topics": rebuild_topics_by_name(),
                "git_repos": GIT_REPOS,
                "elsewhere": yaml.safe_load(open(self.src_dir / "_data/elsewhere.yml")),
            }
        )

        for repo in GIT_REPOS:
            self.prepare_project_pages(env, repo)

        if not incremental:
            self.copy_static_files()

        # Create all the tint colour assets
        for tc in tint_colours:
            tc.create_assets(self.out_dir)

        written_html_paths = set()

        if incremental:
            all_pages = self.all_pages
        else:
            all_pages = tqdm(self.all_pages, desc="writing html")  # type: ignore

        for pg in all_pages:
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
        self.generate_rss_feeds(env)

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
        css_filename, base_css = create_base_css()

        out_path = self.static_dir / css_filename
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

    def generate_rss_feeds(self, env: Environment) -> None:
        """
        Generate the RSS feeds for the site.
        """
        atom_template = env.get_template("atom.xml")
        atom_xml = atom_template.render(articles=self.articles)
        (self.out_dir / "atom.xml").write_text(atom_xml)

        notes_atom_template = env.get_template("notes_atom.xml")
        notes_atom_xml = notes_atom_template.render(notes=self.notes)
        (self.out_dir / "notes/atom.xml").write_text(notes_atom_xml)

    def prepare_project_pages(
        self, env: Environment, repo: GitRepository
    ) -> None:  # pragma: no cover
        """
        Generate the /projects/ folder from my Git repos.
        """
        archive_path = repo.write_archive(out_dir=self.out_dir / "projects")
        archive_url = "/" + str(archive_path.relative_to(self.out_dir))

        self.all_pages.append(ProjectHomepage(repo=repo, archive_url=archive_url))
        self.all_pages.append(ProjectLog(repo=repo))
        self.all_pages.append(ProjectTags(repo=repo))
        self.all_pages.append(ProjectTree(repo=repo))

        for commit in repo.commits.values():
            self.all_pages.append(ProjectCommit(repo=repo, commit=commit))

        # TODO: Clear out the old `raw` directory

        for file_path, is_binary, file_data in repo.iterfiles():
            out_path = self.out_dir / "projects" / repo.name / "raw" / file_path
            out_path.parent.mkdir(exist_ok=True, parents=True)
            out_path.write_bytes(file_data)

            # TODO: If I show per-file history on file pages, render
            # a page for all binary files which previews the file
            # and/or just says "binary file".
            if not is_binary:
                self.all_pages.append(
                    ProjectSingleFile(
                        repo=repo,
                        file_path=file_path,
                        file_contents=file_data.decode("utf8"),
                    )
                )

        repo.create_clone_for_serving(
            out_dir=self.out_dir / f"projects/{repo.name}.git"
        )
