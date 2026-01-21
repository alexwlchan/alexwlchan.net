"""
Embed posts from social media websites in my blog.

These embeds are lightweight HTML and CSS rather than native embeds,
so they don't pull in gross JavaScript tracking and are more resilient
to site outages or link rot.

To embed a post, use a tag of the form:

    {% mastodon https://code4lib.social/@linguistory/113924700205617006 %}

== How it works ==

I have a file `social_embeds.json` with data about each embedded post,
which is keyed by URL and filled in by hand.

When I use the {% social %} tag, the data from that file is combined
with a template to render the post.
"""

import base64
import glob
from io import BytesIO
import json
from pathlib import Path

from jinja2 import nodes, pass_context
from jinja2.ext import Extension
from jinja2.parser import Parser
from jinja2.runtime import Context
from PIL import Image

from mosaic.text import assert_is_invariant_under_markdown

from .pictures import render_picture
from .social_embed_models import (
    MastodonEmbed,
    MediaEntity,
    SocialEmbedData,
    TwitterEmbed,
    parse_social_embed_data,
)


with open("src/_data/social_embeds.json") as in_file:
    SOCIAL_EMBEDS_DATA = {
        url: parse_social_embed_data(data) for url, data in json.load(in_file).items()
    }


class SocialExtension(Extension):
    """
    Defines the {% social %} extension.
    """

    tags = {"bluesky", "mastodon", "tweet", "youtube"}

    def parse(self, parser: Parser) -> nodes.Node:
        """
        Parse a single URL from the tag.
        """
        first_token = next(parser.stream)
        assert first_token.value in self.tags, f"first token = {first_token!r}"

        lineno = first_token.lineno

        # Capture the next token as a string (the URL)
        url_token = next(parser.stream)
        url = nodes.Const(url_token.value)

        # Call the helper method to turn the URL into HTML
        call = self.call_method("_render_social", [url], lineno=lineno)

        # Return an Output node so it prints to the page
        return nodes.Output([call], lineno=lineno)

    @pass_context
    def _render_social(self, context: Context, post_url: str) -> str:
        """
        Render the social embed.
        """
        post_data = SOCIAL_EMBEDS_DATA[post_url]
        env = context.environment

        env.filters.update(
            {
                "avatar_url": avatar_url,
                "render_bluesky_text": render_bluesky_text,
                "render_mastodon_text": render_mastodon_text,
                "render_tweet_text": render_tweet_text,
                "replace_twemoji": replace_twemoji,
                "tweet_image": tweet_image,
            }
        )

        template = env.get_template(f"embeds/{post_data.site}.html")
        html = template.render(post_url=post_url, post_data=post_data)

        assert_is_invariant_under_markdown(html)
        return html


@pass_context
def tweet_image(context: Context, media: MediaEntity) -> str:
    """
    Render a media item on a tweet.
    """
    html = render_picture(
        context,
        filename=media.filename,
        parent="/images/social_embeds/twitter",
        alt=media.ext_alt_text or "",
        width=585,
        link_to=media.url,
    )

    html = html.replace('alt=""', "data-proofer-ignore")

    return html


def avatar_url(post_data: SocialEmbedData) -> str:
    """
    Create a data URI for an avatar.

    These images are tiny when resized properly – in most cases <4KB,
    so it's faster to embed them as base64-encoded images than serve
    them as a separate network request.
    """
    match post_data.site:
        case "mastodon":
            user_id = post_data.author.username
            post_id = post_data.id
        case "twitter":
            user_id = post_data.author.screen_name
            post_id = post_data.id
        case "bluesky":
            user_id = post_data.author.handle
            post_id = post_data.id
        case _:  # pragma: no cover
            raise ValueError(f"Unrecognised site: {post_data.site}")

    avatar_id = f"{user_id}_{post_id}"

    # TODO: Implement caching
    # TODO: Allow choosing the source directory here
    matching_avatars = glob.glob(f"src/_images/social_embeds/avatars/{avatar_id}*")

    if len(matching_avatars) != 1:  # pragma: no cover
        raise RuntimeError(f"could not find avatar for {avatar_id}")

    avatar_path = Path(matching_avatars[0])
    return create_base64_avatar(avatar_path, size=92)


def create_base64_avatar(avatar_path: Path, *, size: int) -> str:
    """
    Converts a square avatar to a base64-encoded data URI at the given size.
    """
    with Image.open(avatar_path) as im:
        assert im.width == im.height
        assert im.width >= size

        resized = im.resize((size, size))

        buffer = BytesIO()
        resized.save(buffer, format=im.format)

    base64_string = base64.b64encode(buffer.getvalue()).decode("utf8")

    match im.format:
        case "JPEG":
            return f"data:image/jpeg;base64,{base64_string}"
        case "PNG":
            return f"data:image/png;base64,{base64_string}"
        case _:  # pragma: no cover
            raise RuntimeError(f"unsupported avatar format: {im.format}")


def render_bluesky_text(post_data: TwitterEmbed) -> str:
    """
    Render the text of a Bluesky post as HTML.
    """
    text = post_data.text

    # Newlines aren't significant in HTML; convert them to <br> tags
    # so they render correctly.
    text = text.replace("\n", "<br>")

    return text


def render_mastodon_text(post_data: MastodonEmbed) -> str:
    """
    Render the text of a Mastodon post as HTML.
    """
    text = post_data.text

    # Newlines aren't significant in HTML; convert them to <br> tags
    # so they render correctly.
    text = text.replace("\n", "<br>")

    if post_data.entities is None:
        return text

    server = post_data.author.server

    for h in post_data.entities.hashtags:
        text = text.replace(f"#{h}", f'<a href="https://{server}/tags/{h}">#{h}</a>')

    for um in post_data.entities.user_mentions:
        text = text.replace(
            f"@{um.label}", f'<a href="{um.profile_url}">@{um.label}</a>'
        )

    for u in post_data.entities.urls:
        text = text.replace(u.url, f'<a href="{u.url}">{u.display_url}</a>')

    return text


def render_tweet_text(post_data: TwitterEmbed) -> str:
    """
    Render the text of a tweet as HTML.
    """
    text = post_data.text

    # Newlines aren't significant in HTML; convert them to <br> tags
    # so they render correctly.
    text = text.replace("\n", "<br>")

    if post_data.entities is None:
        return text

    for h in post_data.entities.hashtags:
        text = text.replace(
            f"#{h}", f'<a href="https://twitter.com/hashtag/{h}">#{h}</a>'
        )

    for um in post_data.entities.user_mentions:
        text = text.replace(f"@{um}", f'<a href="https://twitter.com/{um}">@{um}</a>')

    for u in post_data.entities.urls:
        text = text.replace(u.url, f'<a href="{u.url}">{u.display_url}</a>')

    return text


def replace_twemoji(text: str) -> str:
    """
    Replace emoji in tweets with their "twemoji" counterparts.
    """
    # Rather than record the entire twemoji set here, I just have a
    # hard-coded set of rules for the twemoji I know I'm using.
    twemoji = {
        "😎": "1f60e.svg",
        "👌": "1f44c.svg",
        "🐦": "1f426.svg",
        "💻": "1f4bb.svg",
        "🥳": "1f973.svg",
        # NOTE: this is a surfer emoji with skin tone/gender modifiers
        "🏄🏻‍♂️": "1f3c4-1f3fb-200d-2642-fe0f.svg",
        "📈": "1f4c8.svg",
        "💞": "1f49e.svg",
        "🧵": "1f9f5.svg",
        "✨": "2728.svg",
    }

    for orig, svg_name in twemoji.items():
        if orig not in text:
            continue

        # TODO: Allow choosing the source directory
        svg_path = Path("src/_images/social_embeds/twemoji") / svg_name
        base64_string = base64.b64encode(svg_path.read_bytes()).decode("ascii")
        data_uri = f"data:image/svg+xml;base64,{base64_string}"

        # Construct the <img> tag.  Notes:
        #
        #   - the `twemoji` class is used for styling
        #   - the `width`/`height` attributes are meant for when styles
        #     don't load properly -- they stop the emoji completely blowing
        #     up in size.
        #
        text = text.replace(
            orig,
            f'<img class="twemoji" width="20px" height="20px" alt="{orig}" '
            f'src="{data_uri}"/>',
        )

    return text
