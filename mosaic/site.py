"""
Build system for alexwlchan.net.
"""

from collections import Counter
from datetime import datetime, timezone
import functools
import glob
import itertools
import os
from pathlib import Path
import shutil
import time
from typing import Any, Self

from jinja2 import Environment
from pydantic import BaseModel, Field
import yaml

from . import cache, page_types
from .css import create_base_css
from .git import GitRepository
from .page_types import (
    Article,
    BaseHtmlPage,
    BookReview,
    Note,
    Page,
    Post,
    ProjectCommit,
    ProjectHomepage,
    ProjectLog,
    ProjectSingleFile,
    ProjectTags,
    ProjectTree,
    read_markdown_files,
    read_page_from_markdown,
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


def register_task(label: str) -> Any:
    """
    Annotate a build task so it will be printed and profiled in output.
    """

    def decorator(f: Any) -> Any:
        @functools.wraps(f)
        def wrapper(site: "Site", *args: Any, **kwargs: Any) -> Any:
            t0 = time.time()
            result = f(site, *args, **kwargs)

            if site.build_options.profile:  # pragma: no cover
                elapsed = time.time() - t0
                print(f"{label}...".ljust(30) + f"{elapsed:.2f}s")

            return result

        return wrapper

    return decorator


class BuildOptions(BaseModel):
    """
    Options for the site build process.
    """

    incremental_read: bool = False
    copy_static_files: bool = True
    cleanup_leftover_files: bool = True
    create_tint_colour_assets: bool = True

    # Whether to print detailed timings about each step in the build
    profile: bool = False


class Site(BaseModel):
    """
    Wraps the whole site build process.
    """

    src_dir: Path = Path("src")
    out_dir: Path = Path("_out")

    all_pages: list[BaseHtmlPage] = Field(default_factory=lambda: list())

    written_html_paths: set[str] = Field(default_factory=lambda: set())

    build_options: BuildOptions = BuildOptions()

    css_url: str = ""

    # The time the site was built. This is used in the RSS feed.
    time: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    def build_site(
        self, options: BuildOptions = BuildOptions()
    ) -> bool:  # pragma: no cover
        """
        Build a complete copy of the site.

        Returns True if the build succeeded, False if there were errors.
        """
        self.build_options = options

        self.read_markdown_files()
        self.check_for_duplicate_urls()
        self.set_article_attributes()

        css_url = self.build_base_css_file()

        env = self.get_jinja_environment(css_url=css_url)

        self.time = datetime.now(tz=timezone.utc)

        if self.build_options.create_tint_colour_assets:
            self.create_tint_colour_assets()
        if self.build_options.copy_static_files:
            self.copy_static_files()
        self.write_git_repos(env)
        self.write_html_files(env)
        self.generate_rss_feeds(env)

        if self.build_options.cleanup_leftover_files:
            self.cleanup_leftover_files()

        return True

    @register_task("read markdown files")  # type: ignore
    def read_markdown_files(self) -> None:  # pragma: no cover
        """
        Update the `all_pages` attribute with Markdown files from disk.

        If the `incremental_read` option is selected, only read files that
        changed since our last read.
        """
        if not self.build_options.incremental_read:
            self.all_pages = read_markdown_files(self.src_dir)
            return

        cur_md_paths = set(glob.glob(f"{self.src_dir}/**/*.md", recursive=True))
        known_md_paths = {str(p.md_path) for p in self.all_pages if p.md_path}

        needs_new_index_pages = False
        need_new_tint_colour_assets = False

        updated_pages = []
        for old_p in self.all_pages:
            # Skip a page which doesn't correspond to a Markdown file --
            # it will be regenerated later.
            if old_p.md_path is None:
                continue

            # Skip a file which has been deleted from disk
            if str(old_p.md_path) not in cur_md_paths:
                continue

            # Use the existing page if the Markdown file hasn't been
            # changed recently, or read it from disk if it's changed.
            if not self.has_changed_since_last_read(old_p.md_path):
                updated_pages.append(old_p)
            else:
                print(f"re-reading {old_p.md_path}")
                new_p = read_page_from_markdown(self.src_dir, md_path=old_p.md_path)
                if old_p.colors != new_p.colors:
                    need_new_tint_colour_assets = True
                if (
                    old_p.title != new_p.title
                    or old_p.summary != new_p.summary
                    or old_p.topics != new_p.topics
                    or old_p.date != new_p.date
                ) or isinstance(new_p, BookReview):
                    needs_new_index_pages = True
                updated_pages.append(new_p)
                new_p.clear_cache()

        # Read any Markdown files which have been written since we last
        # read the source folder.
        for p in cur_md_paths - known_md_paths:
            print(f"reading {p}")
            page = read_page_from_markdown(self.src_dir, md_path=Path(p))
            if page.colors is not None:
                need_new_tint_colour_assets = True
            updated_pages.append(page)
            needs_new_index_pages = True

        self.all_pages = updated_pages
        self.build_options.create_tint_colour_assets = need_new_tint_colour_assets

        if needs_new_index_pages:
            for page in self.all_pages:
                if isinstance(page, Page):
                    page.clear_cache()

    def has_changed_since_last_read(self, p: Path | str) -> bool:  # pragma: no cover
        """
        Check if a file has changed since the last time we built the site.
        """
        if not self.build_options.incremental_read:
            return True

        return os.stat(p).st_mtime > self.time.timestamp() - 10

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

    @property
    def static_dir(self) -> Path:
        """
        Static output directory, where static assets are saved.
        """
        return self.out_dir / "static"

    def check_for_duplicate_urls(self) -> Self:
        """
        Every page should have a unique URL.
        """
        counter = Counter(p.url for p in self.all_pages)
        duplicate_urls = {url: count for url, count in counter.items() if count > 1}

        if duplicate_urls:
            raise RuntimeError(
                f"multiple pages write to the same URL: {duplicate_urls}"
            )

        return self

    @register_task("create tint colour assets")  # type: ignore
    def create_tint_colour_assets(self) -> None:
        """
        Create the tint colour assets.
        """
        tint_colours = [get_default_tint_colours()] + [
            p.colors for p in self.all_pages if p.colors is not None
        ]

        for tc in tint_colours:
            tc.create_assets(self.out_dir)

    def get_jinja_environment(self, css_url: str) -> Environment:
        """
        Create the Jinja2 environment.
        """
        # TODO(2026-01-21): Figure out how to handle global varibales better.
        env = get_jinja_environment(self.src_dir, self.out_dir)

        with open(self.src_dir / "_data/elsewhere.yml") as in_file:
            elsewhere = yaml.safe_load(in_file)

        env.globals.update(
            {
                "css_url": css_url,
                "site": self,
                "all_topics": rebuild_topics_by_name(),
                "git_repos": GIT_REPOS,
                "elsewhere": elsewhere,
            }
        )

        return env

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

        css_url = "/" + str(out_path.relative_to(self.out_dir))

        self.css_url = css_url
        return css_url

    @register_task("write html files")  # type: ignore
    def write_html_files(self, env: Environment) -> None:
        """
        Write all the HTML files to the output directory.
        """
        # Check if anything in the CSS/templates/Mosaic has changed since
        # the last build; if so, invalidate the HTML cache and rebuild
        # everything from scratch.
        cache_ns = "write_html_files"

        css_mtime = str(get_latest_mtime("css"))
        templates_mtime = str(get_latest_mtime("templates"))

        cache_entries = [
            ("mosaic", mosaic_mtime),
            ("css", css_mtime),
            ("templates", templates_mtime),
        ]

        bust_cache = False
        for label, cur_value in cache_entries:  # pragma: no cover
            cache_key = f"{label}_mtime"
            if cache.get(cache_ns, cache_key) != cur_value:
                if cache.contains(cache_ns, cache_key):
                    print(f"detected changes to {label}...")
                bust_cache = True

        if bust_cache:  # pragma: no cover
            cache.purge(namespace=cache_ns)
            for pg in self.all_pages:
                pg.clear_cache()

        for pg in self.all_pages:
            try:
                out_path = pg.write(env, out_dir=self.out_dir)
                self.written_html_paths.add(str(out_path))
            except Exception as exc:  # pragma: no cover
                print(f"error writing {pg!r}: {exc}")
                raise

        for label, cur_value in cache_entries:
            cache_key = f"{label}_mtime"
            cache.set(cache_ns, cache_key, cur_value)

    @register_task("copy static files")  # type: ignore
    def copy_static_files(self) -> None:
        """
        Copy all the static files from the src to the dst directory.
        """
        # A list of (src, dst) static files to be copied.
        static_files: list[tuple[str, str]] = []

        for src_p in glob.glob(f"{self.src_dir}/**/*", recursive=True):
            if src_p.endswith(".md"):
                continue
            if not os.path.isfile(src_p):
                continue

            # If this is an incremental build and the original file hasn't
            # changed recently, don't bother doing another copy.
            if not self.has_changed_since_last_read(src_p):  # pragma: no cover
                continue

            out_p = os.path.join(
                self.out_dir, os.path.relpath(src_p, start=self.src_dir)
            )

            # If the files have the same size and modification time,
            # assume they're the same and we don't need to copy again.
            if (
                os.path.exists(out_p)
                and os.stat(src_p).st_size == os.stat(out_p).st_size
                and os.stat(src_p).st_mtime == os.stat(out_p).st_mtime
            ):
                continue

            static_files.append((src_p, out_p))

        for src_p, out_p in static_files:
            os.makedirs(os.path.dirname(out_p), exist_ok=True)
            shutil.copy2(src_p, out_p)

    @register_task("generate rss feeds")  # type: ignore
    def generate_rss_feeds(self, env: Environment) -> None:
        """
        Generate the RSS feeds for the site.
        """
        atom_template = env.get_template("atom.xml")
        atom_xml = atom_template.render(env=env, articles=self.articles)
        (self.out_dir / "atom.xml").write_text(atom_xml)

        notes_atom_template = env.get_template("notes_atom.xml")
        notes_atom_xml = notes_atom_template.render(env=env, notes=self.notes)
        (self.out_dir / "notes/atom.xml").write_text(notes_atom_xml)

    def set_article_attributes(self) -> None:  # pragma: no cover
        """
        Set the `order` and `card_short_name` properties for articles.
        """
        # Ordering: add a numeric "order" attribute to every article,
        # which is used for sorting on /articles/.
        for order, art in enumerate(reversed(self.articles), start=1):
            art.order = order

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

    @register_task("write git repos")  # type: ignore
    def write_git_repos(self, env: Environment) -> None:  # pragma: no cover
        """
        Write the /projects/ folder for my Git repos.
        """
        for repo in GIT_REPOS:
            self.write_pages_for_single_repo(env, repo)

    def write_pages_for_single_repo(
        self, env: Environment, repo: GitRepository
    ) -> None:  # pragma: no cover
        """
        Write the /projects/ folder data for a single Git repo.
        """
        archive_path = repo.write_archive(out_dir=self.out_dir / "projects")
        archive_url = "/" + str(archive_path.relative_to(self.out_dir))

        self.all_pages.append(ProjectHomepage(repo=repo, archive_url=archive_url))
        self.all_pages.append(ProjectLog(repo=repo))
        self.all_pages.append(ProjectTags(repo=repo))
        self.all_pages.append(ProjectTree(repo=repo))

        for commit in repo.commits.values():
            self.all_pages.append(ProjectCommit(repo=repo, commit=commit))

        # Write a per-file page for every file in the tree, and write
        # the raw file if it hasn't been written already.
        #
        # Record the blob ID that was written, so we can record the last
        # version we wrote in the cache, and skip writing it again if
        # we're already up to data. Reading the blob data is slow, so we
        # want to avoid it if we can.
        #
        # TODO: Clear out stale entries from the `raw` directory
        for f in repo.tree.files:
            raw_path = self.out_dir / "projects" / repo.name / "raw" / f.path
            stub_page = ProjectSingleFile(repo=repo, file=f, file_contents="")
            html_path = stub_page.out_path(self.out_dir)

            cache_ns = "git.write_raw_file"
            mtime = (
                f"{mosaic_mtime}"
                f":{get_latest_mtime('css')}"
                f":{get_latest_mtime('templates/projects')}"
            )
            cache_id = f"{raw_path}:{f.blob_id}"

            if (
                raw_path.exists()
                and (html_path.exists() or f.is_binary)
                and cache.get(cache_ns, cache_id) == mtime
            ):
                if f.is_binary:
                    self.written_html_paths.add(str(html_path))
                continue
            else:
                stub_page.clear_cache()

            file_data = repo.get_blob_data(f.blob_id)

            raw_path.parent.mkdir(exist_ok=True, parents=True)
            raw_path.write_bytes(file_data)

            # TODO: If I show per-file history on file pages, render
            # a page for all binary files which previews the file
            # and/or just says "binary file".
            if not f.is_binary:
                page = ProjectSingleFile(
                    repo=repo,
                    file=f,
                    file_contents=file_data.decode("utf8"),
                )
                out_path = page.write(env, self.out_dir)
                self.written_html_paths.add(str(out_path))

            cache.set(cache_ns, cache_id, mtime)

        # Create a version of the repo that be cloned.
        #
        # This is quite a slow operation, so cached the HEAD ID that was
        # used for the clone; if the HEAD hasn't changed since we did the
        # last clone, assume it's up-to-date.
        cache_ns = "git:clone_for_serving"
        clone_dir = self.out_dir / f"projects/{repo.name}.git"

        if not clone_dir.exists() or cache.get(cache_ns, repo.name) != repo.head:
            repo.create_clone_for_serving(
                out_dir=self.out_dir / f"projects/{repo.name}.git"
            )
            cache.set(cache_ns, repo.name, repo.head)

    @register_task("clean up leftover files")  # type: ignore
    def cleanup_leftover_files(self) -> None:
        """
        Clean up HTML files that weren't rewritten as part of this build.

        This usually indicates a renamed or deleted page.
        """
        for p in glob.glob(
            f"{self.out_dir}/**/*.html", recursive=True
        ):  # pragma: no cover
            if p in self.written_html_paths:
                continue

            if "/files/" in p or "/fun-stuff/" in p:
                continue

            print(f"delete stale HTML file: {p}")
            os.unlink(p)


def get_latest_mtime(dirname: str) -> float:
    """
    Return the latest modification time for the files in this directory.
    """
    return max(
        os.stat(p).st_mtime for p in glob.glob(f"{dirname}/**/*", recursive=True)
    )


# Changes to the Mosaic code won't affect the running process, so it's
# sufficient to get this once.
mosaic_mtime = str(get_latest_mtime("mosaic"))
