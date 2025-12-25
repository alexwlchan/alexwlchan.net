#!/usr/bin/env python3

import collections
import concurrent.futures
from dataclasses import dataclass
import hashlib
from pathlib import Path
import shutil
from typing import Literal

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError
import lightningcss
from PIL import Image, ImageDraw
import yaml

from mosaic.colours import colourise_image, get_colours_like
from mosaic.css import default_tint_colours
from mosaic.fs import list_paths
from mosaic.models import (
    Article,
    CardConfig,
    Colours,
    Page,
    RSSFeed,
    SiteConfig,
    SiteInput,
    StaticFile,
    TagPage,
    TodayILearned,
)
from mosaic.pictures import create_image_derivatives, generate_squares
from mosaic.templates import article_card_image, markdownify


def read_src_files(src_dir: Path) -> SiteInput:
    """
    Read all the source files which are input to the site.
    """
    input = SiteInput(
        src_dir=src_dir,
        config=SiteConfig(
            url="https://alexwlchan.net",
            title="alexwlchan",
            description="Alex Chan's personal website",
            email="alex@alexwlchan.net",
        ),
    )

    for p in list_paths(src_dir):
        if p.name == ".DS_Store":
            continue

        # Ignore folders which contain Jekyll-specific code or templates,
        # which I can safely discard in the Python build system.
        if any(
            f in p.parts
            for f in (
                "_data",
                "_favicons",
                "_includes",
                "_layouts",
                "_plugins",
                "_plugin_tests",
                "_scss",
                ".jekyll-cache",
            )
        ):
            continue

        if p.suffix == ".md":
            _, front_matter_str, markdown = p.read_text().split("---\n", 2)
            front_matter = yaml.load(front_matter_str, Loader=yaml.Loader)
            layout = front_matter["layout"]

            if layout == "page":
                input.pages.append(
                    Page(**front_matter, path=p.relative_to(src_dir), content=markdown)
                )
            elif layout == "post":
                input.articles.append(Article(**front_matter, path=p, content=markdown))
            elif layout == "til":
                input.tils.append(
                    TodayILearned(**front_matter, path=p, content=markdown)
                )
            else:
                raise ValueError(f"Unrecognised layout in {p}: {layout}")

        elif p.suffix == ".xml":
            _, front_matter_str, xml = p.read_text().split("---\n", 2)
            front_matter = yaml.load(front_matter_str, Loader=yaml.Loader)

            input.feeds.append(RSSFeed(**front_matter, path=p, content=xml))

        elif p.is_relative_to(src_dir / "_images"):
            if p.is_relative_to(src_dir / "_images/social_embeds/avatars"):
                continue
            if p.is_relative_to(src_dir / "_images/social_embeds/twemoji"):
                continue
            if p.suffix == ".svg":
                continue

            input.static_files[p] = StaticFile(
                path=Path("images") / p.relative_to(src_dir / "_images")
            )

        elif "_files" in p.parts:
            input.static_files[p] = StaticFile(
                path=Path("files") / p.relative_to(src_dir / "_files")
            )

        else:
            input.static_files[p] = StaticFile(path=p.relative_to(src_dir))

    return input


def add_article_card_images(input: SiteInput) -> None:
    """
    Enrich all the articles/TILs with card images.
    """
    # Build a map (year, slug) -> Path, so we know all the card images.
    article_cards: dict[tuple[str, str], Path] = dict()

    for p in list_paths(input.src_dir / "_images/cards"):
        year = int(p.parent.name)
        slug = p.stem

        article_cards[(year, slug)] = p

        with Image.open(p) as im:
            if im.width / im.height != 2:
                raise ValueError(f"card image doesn't have a 2:1 aspect ratio: {p}")

    # Go through every post, and enrich it with a card image (if present).
    # Build a list of posts which have cards.
    posts_with_cards: dict[int, Article | TodayILearned] = collections.defaultdict(list)

    for post in input.articles + input.tils:
        if post.is_excluded_from_index:
            continue

        try:
            card_path = article_cards[(post.date.year, post.slug)]
        except KeyError:
            continue

        post.card = CardConfig(
            attribution=getattr(post, "card_attribution", None),
            year=post.date.year,
            path=card_path.relative_to(input.src_dir),
        )
        posts_with_cards[post.date.year].append(post)

    # Choose unique abbrevations for the names of each card.
    #
    # These filenames will be used a lot on the global index page, so we
    # want them to be as short as possible.
    #
    # We construct minimal prefixes that uniquely identify each card name,
    # e.g. "digital-decluttering.jpg" might become "di", which is much shorter!
    for year, posts in posts_with_cards.items():
        abbreviations = choose_unique_abbreviations({p.slug for p in posts})

        for p in posts:
            p.card.out_prefix = f"{p.date.year % 100}/{abbreviations[p.slug]}"


def choose_unique_abbreviations(words: set[str]) -> dict[str, str]:
    """
    Choose a unique abbreviation for each word in `words`.

    This is equivalent to Ruby's Abbrev.abbrev.

    TODO: This is fairly inefficient, but fine for small collections.
    If this becomes a slow point, rewrite it to be faster.
    """
    result: dict[str, str] = {}

    for this_word in words:
        for i in range(1, len(this_word) + 1):
            prefix = this_word[:i]
            matching_words = {w for w in words if w.startswith(prefix)}
            if matching_words != {this_word}:
                continue
            result[this_word] = prefix
            break
        else:  # no break
            result[this_word] = this_word

    assert set(result.keys()) == words, words - set(result.keys())
    return result


def prepare_site(input: SiteInput) -> None:
    """
    Run any preparation steps.
    """
    add_article_card_images(input)
    input.visible_tags = get_visible_tags(input)

    for order, article in enumerate(sorted(input.articles, key=lambda a: a.date, reverse=True), start=1):
        article.order = order


def get_visible_tags(input: SiteInput) -> dict[str, int]:
    """
    Return a tally of visible tags, which can be used to render the
    tag pages and the global tags list.

    This only counts posts that are visible in the sitewide indexes.
    """
    tally = collections.Counter()

    for post in input.articles + input.tils:
        if post.is_excluded_from_index:
            continue

        for t in post.tags:
            tally[t] += 1

    return tally


def render_site(input: SiteInput, out_dir: Path) -> None:
    """
    Use the site input to render the site in the given output directory.
    """
    r = Renderer(input=input, out_dir=out_dir)
    r.render_site()


@dataclass
class Renderer:
    input: SiteInput
    out_dir: Path
    env: Environment = None

    @property
    def src_dir(self) -> Path:
        return self.input.src_dir

    def render_site(self) -> None:
        self.env = self.get_jinja_environment(environment="production")
        written_paths: set[Path] = set()

        # Render the CSS file
        bundled_css = lightningcss.bundle_css(
            "css/style.css",
            minify = True,
        )
        h = hashlib.md5(bundled_css.encode("utf8")).hexdigest()[:7]
        (self.out_dir / f"static/style.{h}.css").write_text(bundled_css)

        self.env.globals["css_url"] = f"/static/style.{h}.css"

        # Render the Atom feeds
        

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = set()

            for article in self.input.articles:
                futures.add(executor.submit(self.render_article, article))

            for til in self.input.tils:
                futures.add(executor.submit(self.render_til, til))

            for post in self.input.posts:
                if post.card is not None:
                    futures.add(executor.submit(self.create_sharing_card, post.card))

            for page in self.input.pages:
                futures.add(executor.submit(self.render_page, page))

            for page in self.input.posts + self.input.pages:
                if page.colors is not None:
                    futures.add(
                        executor.submit(
                            self.create_theme_assets_for_colour, page.colors
                        )
                    )

            futures.add(
                executor.submit(
                    self.create_theme_assets_for_colour, default_tint_colours(self.src_dir)
                )
            )

            for t in self.input.visible_tags:
                futures.add(executor.submit(self.render_tag_page, t))

            # TODO: RSS feeds

            for p, sf in self.input.static_files.items():
                futures.add(executor.submit(self.copy_static_file, p, sf.path))

            done, not_done = concurrent.futures.wait(futures)
            assert not_done == set(), f"Uncompleted futures: {not_done}"

            import tqdm

            for fut in tqdm.tqdm(futures):
                written_paths.add(fut.result())

        # Go through the output directory, and delete any files which weren't
        # written as part of the current process.
        for p in list_paths(self.out_dir, suffix=".html"):
            if p not in written_paths:
                p.unlink()

    def get_jinja_environment(
        self, environment: Literal["development", "production"]
    ) -> Environment:
        """
        Create a Jinja2 environment which looks in the `templates` directory.
        """
        from mosaic import templates

        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=False,
            undefined=StrictUndefined,
            extensions=[
                "jinja2.ext.loopcontrols",
                templates.BookInfoExtension,
                templates.EmbedExtension,
                templates.PictureExtension,
                templates.SlideExtension,
                templates.CodeBlockExtension,
                templates.TOCExtension,
                templates.KwargsExtension,
                templates.CommentExtension,
                templates.UpdateExtension,
            ],
        )

        # Remove whitespace around blocks in the templates.
        # TODO: Does this mean I can remove {%- -%} from all my templates?
        env.trim_blocks = True
        env.lstrip_blocks = True

        env.filters.update(
            {
                "absolute_url": lambda u: self.input.config.url + u,
                "article_card_image": lambda card: article_card_image(
                    env, self.src_dir, self.out_dir, card
                ),
                "cleanup_text": templates.cleanup_text,
                "get_inline_styles": templates.get_inline_styles,
                "markdownify": templates.markdownify,
                "markdownify_oneline": templates.markdownify_oneline,
                "strip_html": templates.strip_html,
            }
        )

        env.globals["environment"] = environment
        env.globals["site"] = self.input

        return env

    def _render_html_file(self, template_name: str, page: Article, out_path: Path) -> Path:
        """
        Render a file to the output directory, and return the written path.
        """
        out_path.parent.mkdir(exist_ok=True, parents=True)

        try:
            content_template = self.env.from_string(page.content)
        except TemplateError as e:
            raise ValueError(f"template error in {page.path}: {e}")

        content = content_template.render(
            src_dir=self.src_dir, out_dir=self.out_dir, page=page
        )
        content = markdownify(content)

        template = self.env.get_template(template_name)
        html = template.render(page=page, content=content)
        out_path.write_text(html)

        return out_path

    def render_article(self, article: Article) -> Path:
        """
        Saves an article as HTML to the output directory, and returns the
        written path.
        """
        return self._render_html_file(
            template_name="article.html",
            page=article,
            out_path=self.out_dir / article.url.strip("/") / "index.html",
        )

    def render_til(self, til: TodayILearned) -> Path:
        """
        Saves a TIL as HTML to the output directory, and returns the
        written path.
        """
        return self._render_html_file(
            template_name="til.html",
            page=til,
            out_path=self.out_dir / til.url.strip("/") / "index.html",
        )

    def render_page(self, page: Page) -> Path:
        """
        Saves a page as HTML to the output directory, and returns the
        written path.
        """
        return self._render_html_file(
            template_name="page.html",
            page=page,
            out_path=self.out_dir / page.url.strip("/") / "index.html",
        )

    def render_tag_page(self, tag: str) -> Path:
        """
        Saves a page as HTML to the output directory, and returns the
        written path.
        """
        posts_with_tag = [
            p
            for p in self.input.posts
            if tag in p.visible_tags
        ]
        featured_posts = [
            p for p in posts_with_tag if p.is_featured
        ]
        remaining_posts = [
            p for p in posts_with_tag if not p.is_featured
        ]

        if ":" in tag:
            namespace, tag_name = tag.split(":")
        else:
            namespace, tag_name = "", tag

        page = TagPage(
            namespace=namespace,
            tag_name=tag_name,
            # TODO: Wire up tag descriptions
            # TODO: Require tag descriptions for all tags
            tag_description=None,
            featured_posts=featured_posts,
            remaining_posts=remaining_posts,
        )

        return self._render_html_file(
            template_name="tag.html",
            page=page,
            out_path=self.out_dir / page.url.strip("/") / "index.html",
        )

    def create_sharing_card(self, card: CardConfig) -> None:
        """
        Create all the sizes of a sharing card.
        """
        desired_widths = [
            365,
            365 * 2,  # 2-up column => ~365px wide
            302,
            302 * 2,  # 3-up column => ~302px wide
            405,
            405 * 2,  # 1-up column => ~405px wide
        ]

        create_image_derivatives(
            src_path=self.src_dir / card.path,
            src_dir=self.src_dir,
            out_path=Path("c") / card.out_prefix,
            out_dir=self.out_dir,
            desired_widths=desired_widths,
        )

    def create_theme_assets_for_colour(self, colours: Colours) -> None:
        """
        Create all the themed assets for a set of tint colours.
        """
        if colours.css_light is not None:
            self.create_header_image(colours.css_light)
            self.create_favicon(colours.css_light)
        if colours.css_dark is not None:
            self.create_header_image(colours.css_dark)
            self.create_favicon(colours.css_dark)

    def create_header_image(self, hex: str) -> None:
        """
        Create a mosaic header image for this tint colour.
        """
        out_path = self.out_dir / "h" / f"{hex.replace('#', '')}.png"

        if out_path.exists():
            return

        out_path.parent.mkdir(exist_ok=True)
        colours = get_colours_like(hex)
        squares = generate_squares(width=2500, height=250, sq_size=50)

        im = Image.new(mode="RGB", size=(2500, 250))
        draw = ImageDraw.Draw(im)

        for sq, fill in zip(squares, colours):
            draw.polygon(sq, fill=fill)

        im.save(out_path, optimize=True)

    def create_favicon(self, hex: str) -> None:
        """
        Create PNG, SVG, and ICO variants of the favicon for this tint colour.
        """
        hex_string = hex.replace("#", "")
        favicon_dir = self.out_dir / "f"

        ico_path = favicon_dir / f"{hex_string}.ico"
        if ico_path.exists():
            return

        favicon_dir.mkdir(exist_ok=True)

        # Create colorised versions of the SVG icon at 32x32 and 16x16 sizes
        template16 = self.env.get_template("favicons/favicon-16x16.svg")
        svg16 = template16.render(tint_colour=hex)
        (favicon_dir / f"{hex_string}-16x16.svg").write_text(svg16)

        template32 = self.env.get_template("favicons/favicon-32x32.svg")
        svg32 = template32.render(tint_colour=hex)
        (favicon_dir / f"{hex_string}-32x32.svg").write_text(svg32)

        # Create colorised versions of the PNG icon at 32x32 and 16x16 sizes
        with (
            Image.open("templates/favicons/favicon-16x16.png") as png16,
            Image.open("templates/favicons/favicon-32x32.png") as png32,
        ):
            png16 = colourise_image(png16, hex)
            png16.save(favicon_dir / f"{hex_string}-16x16.png")

            png32 = colourise_image(png32, hex)
            png32.save(favicon_dir / f"{hex_string}-32x32.png")

            png32.save(favicon_dir / f"{hex_string}.ico", append_images=[png16])

    def copy_static_file(self, src: Path, dst: Path) -> Path:
        """
        Copy a file from `src` to `dst`. Returns the destination path.
        """
        dst = self.out_dir / dst

        if (
            src.exists()
            and dst.exists()
            and src.stat().st_size == dst.stat().st_size
            and src.stat().st_mtime < dst.stat().st_mtime
        ):
            return dst

        dst.parent.mkdir(exist_ok=True, parents=True)
        shutil.copyfile(src, dst)
        return dst


if __name__ == "__main__":
    print("Reading source files...")
    input = read_src_files(src_dir=Path("src"))

    print("Preparing site...")
    prepare_site(input)

    print("Rendering output...")
    render_site(input, out_dir=Path("_site.2"))
