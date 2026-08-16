"""
Functions for rendering and manipulating HTML.
"""

from html.parser import HTMLParser
from typing import TypeAlias, TypedDict

from bs4 import BeautifulSoup, Comment, Tag
import minify_html as minify_html_lib

from mosaic import cache


__all__ = ["fix_html_for_feed_readers", "minify_html", "parse_html_headings"]


def minify_html(html: str) -> str:
    """
    Minify an HTML string.
    """
    return minify_html_lib.minify(
        html,
        keep_html_and_head_opening_tags=True,
        keep_closing_tags=True,
        minify_css=True,
        minify_js=True,
    )


class Subheading(TypedDict):
    """A sub-heading in an HTML document."""

    id: str
    label: str


class Heading(TypedDict):
    """A top-level heading in an HTML document."""

    id: str
    label: str
    sub_headings: list[Subheading]


HTMLAttrs: TypeAlias = list[tuple[str, str | None]]


class HeadingParser(HTMLParser):
    """
    An HTML parser that looks for heading tags (<h2> and <h3>).
    """

    def __init__(self) -> None:
        super().__init__()
        self.result: list[Heading] = []
        self.last_seen_tag: str | None = None
        self.last_seen_id: str | None = None
        self.accumulator: list[str] = []

    def handle_starttag(self, tag: str, attrs: HTMLAttrs) -> None:
        """
        If this is an opening heading tag, record the heading level and ID
        and start a new state.
        """
        if tag in {"h2", "h3"}:
            attr_dict = dict(attrs)
            self.last_seen_tag = tag
            self.last_seen_id = attr_dict["id"]
            assert isinstance(self.last_seen_id, str)
            self.accumulator = []

    def handle_data(self, data: str) -> None:
        """
        If we're in the middle of a heading tag, add the data we've
        received to the accumulator.
        """
        if self.last_seen_tag:
            self.accumulator.append(data)

    def handle_endtag(self, tag: str) -> None:
        """
        If this is a closing heading tag, process all the data we've
        received until this point, append the result, then reset the state.
        """
        if tag == self.last_seen_tag:
            label = "".join(self.accumulator).strip()
            heading_id = self.last_seen_id
            assert isinstance(heading_id, str)

            if tag == "h2":
                self.result.append(
                    {"id": heading_id, "label": label, "sub_headings": []}
                )
            elif tag == "h3":
                self.result[-1]["sub_headings"].append(
                    {"id": heading_id, "label": label}
                )
            else:  # pragma: no cover
                assert 0, "unreachable"

            self.last_seen_tag = None
            self.last_seen_id = None


def parse_html_headings(md: str) -> list[Heading]:
    """
    Extract all the headings from a Markdown document.
    """
    from .markdown import markdownify

    html = markdownify(md)
    parser = HeadingParser()
    parser.feed(html)
    return parser.result


@cache.register
def fix_html_for_feed_readers(html: str) -> str:
    """
    Apply some clean-ups for HTML embedded in the RSS feed.
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1. Remove all tags which aren't appropriate in an RSS feed.
    for tag in soup.find_all(["link", "script", "style"]):
        tag.extract()

    # 2. Remove specific attributes: style, controls, aria-hidden
    #
    # According to https://github.com/rubys/feedvalidator, these aren't
    # allowed in an RSS feed.
    bad_attrs = ["style", "controls", "aria-hidden", "title", "onchange", "onclick"]
    for tag in soup.find_all(True):  # True finds all tags
        for attr in bad_attrs:
            if tag.has_attr(attr):
                del tag[attr]

    # 3. Delete the logo and avatars from embedded social media posts.
    for embed in soup.select("blockquote.embed"):
        for logo in embed.select("svg.logo"):
            logo.decompose()
        for avatar in embed.select("img.avatar"):
            avatar.decompose()

    # 4. Replace twemoji SVGs with their alt text (the emoji itself)
    for emoji in soup.select("img.twemoji"):
        assert isinstance(emoji["alt"], str)
        emoji.replace_with(emoji["alt"])

    # 5. Replace relative URLs with absolute URLs.
    link_elements = [
        {"selector": "img", "attr": "src"},
        {"selector": "a", "attr": "href"},
        {"selector": "source", "attr": "srcset"},
        {"selector": "image", "attr": "src"},  # For inline SVGs
    ]

    for config in link_elements:
        for tag in soup.select(config["selector"]):
            fix_relative_url(tag, config["attr"])

    # 6. Remove comments.
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # 7. Replace YouTube <iframes> with links.
    #
    # This is based on https://github.com/rubys/feedvalidator, which says
    # that embedding an <iframe> in an RSS feed can be a security risk.
    for iframe in soup.find_all("iframe", attrs={"class": "youtube"}):
        iframe_id = iframe.attrs["id"]
        assert isinstance(iframe_id, str)
        video_id = iframe_id.replace("youtube_", "")
        url = f"https://www.youtube.com/watch?v={video_id}"

        paragraph = soup.new_tag("p")
        link = soup.new_tag("a", href=url)
        link.string = url
        paragraph.append(link)

        iframe.replace_with(paragraph)

    # 7. Convert back to string and remove empty paragraphs
    # We use .decode_contents() to get just the inner HTML without
    # the body tags
    output = soup.body.decode_contents() if soup.body else str(soup)
    return output.replace("<p></p>", "").strip()


def fix_relative_url(tag: Tag, attribute_name: str) -> None:
    """
    Convert a URL to be an absolute URL.
    """
    existing_value = tag.get(attribute_name)
    if not existing_value:
        return

    # Handle comma-separated values (common in srcset)
    values = [v.strip() for v in str(existing_value).split(",")]
    new_values = []

    for v in values:
        if v.startswith("/"):
            new_values.append(f"https://alexwlchan.net{v}")
        else:
            new_values.append(v)

    tag[attribute_name] = ", ".join(new_values)
