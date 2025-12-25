"""
The embed extension is for embedding social media.
"""

import base64
from datetime import datetime
import glob
from io import BytesIO
import json
from pathlib import Path

from jinja2 import nodes, pass_context
from jinja2.ext import Extension
from jinja2.runtime import Context
from PIL import Image

from .pictures import render_picture


with open("data/social_embeds.json") as in_file:
    EMBED_DATA = json.load(in_file)

    for p in EMBED_DATA.values():
        if "date_posted" in p:
            p["date_posted"] = datetime.fromisoformat(p["date_posted"])


class EmbedExtension(Extension):
    tags = {"bluesky", "mastodon", "tweet", "youtube"}

    def parse(self, parser):
        # The first token should be the name of the tag, e.g. "picture"
        first_token = next(parser.stream)

        # Parse the next expression (the URL string)
        url = parser.parse_expression()

        kwargs = [nodes.Keyword("url", url)]

        return nodes.CallBlock(
            self.call_method("render_embed", kwargs=kwargs), [], [], []
        ).set_lineno(first_token.lineno)

    @pass_context
    def render_embed(self, context: Context, url: str, **kwargs) -> str:
        # Look up the embed data in data/social_embeds.json, which
        # is keyed by URL.
        post_data = EMBED_DATA[url]

        env = context.environment

        if "avatar_url" not in env.filters:
            env.filters.update({
                "avatar_url": avatar_url,
                "replace_twemoji": replace_twemoji,
                "render_mastodon_text": render_mastodon_text,
                "render_tweet_text": render_tweet_text,
                "tweet_image": lambda m: tweet_image(context, m),
            })

        template = env.get_template(f"embeds/{post_data['site']}.html")
        try:
            return template.render(post_data=post_data, post_url=url, **context)
        except Exception as e:
            print(post_data, e)
            raise


def avatar_url(post_data):
    """
    Create a data URI for the avatar.

    These images are tiny when resized properly – in most cases <4KB,
    so it's faster to embed them as base64-encoded images than serve
    them as a separate network request.
    """
    # Avatars are stored in the _images/social_embeds/avatars directory,
    # combining the site, user ID, and post ID.
    if post_data["site"] == "mastodon":
        user_id = post_data["author"]["username"]
        post_id = post_data["id"]
    elif post_data["site"] == "twitter":
        user_id = post_data['author']['screen_name']
        post_id = post_data['id']
    elif post_data["site"] == 'bluesky':
        user_id = post_data['author']['handle']
        post_id = post_data['id']
    else:
        raise ValueError(f'Unrecognised site: {post_data["site"]}')

    avatar_id = f"{user_id}_{post_id}"

    matching_avatars = glob.glob(
        f"src/_images/social_embeds/avatars/{avatar_id}*"
    )
    if len(matching_avatars) != 1:
        raise RuntimeError(f"Could not find avatar for {avatar_id}")

    avatar_path = matching_avatars[0]

    with Image.open(avatar_path) as im:
        if im.width != im.height:
            raise ValueError(f"avatar is not square: {avatar_path}")

        resized = im.resize((92, 92))

        # Write the image to a buffer, and convert it to base64.
        #
        # Preserve the original format, assuming that's the most efficient
        # encoding for this image.
        buffer = BytesIO()
        resized.save(buffer, format=im.format)
        image_uri = base64.b64encode(buffer.getvalue()).decode("ascii")

        if im.format == "JPEG":
            return f"data:image/jpeg;base64,{image_uri}"
        elif im.format == "PNG":
            return f"data:image/png;base64,{image_uri}"
        else:
            raise ValueError(f"unrecognised avatar format: {avatar_path}")


def replace_twemoji(text: str) -> str:
    """
    Replace emoji in tweets with their "twemoji" counterparts.

    Rather than record the entire twemoji set here, I just have a
    hard-coded set of rules for the twemoji I know I'm using.
    """
    twemoji = {
    '😎': '1f60e.svg',
    '👌': '1f44c.svg',
    '🐦': '1f426.svg',
    '💻': '1f4bb.svg',
    '🥳': '1f973.svg',
    # NOTE: this is a surfer emoji with skin tone/gender modifiers
    '🏄🏻‍♂️': '1f3c4-1f3fb-200d-2642-fe0f.svg',
    '📈': '1f4c8.svg',
    '💞': '1f49e.svg',
    '🧵': '1f9f5.svg',
    '✨': '2728.svg'
    }

    for orig, svg_name in twemoji.items():
        if orig not in text:
            continue

        buffer = (Path("src/_images/social_embeds/twemoji") / svg_name).read_bytes()
        image_uri = base64.b64encode(buffer).decode("ascii")
        data_uri = f"data:image/svg+xml;base64,{image_uri}"

        # Construct the <img> tag.  Notes:
        #
        #   - the `twemoji` class is used for styling
        #   - the `width`/`height` attributes are for when styles don't load
        #     properly -- they stop the emoji completely blowing up in size.
        #
        text = text.replace(
            orig,
            f'<img class="twemoji" width="20px" height="20px" alt="{orig}" src="{data_uri}"/>'
        )

    return text


def render_mastodon_text(post_data) -> str:
    """
    render_mastodon_text renders the text of a Mastodon post as HTML.

    This includes:

      - Expanding newlines
      - Adding hashtags

    """
    text = post_data['text']
    entities = post_data.get("entities", {})

    # Newlines aren't significant in HTML; convert them to <br> tags.
    text = text.replace("\n", '<br>')

    server = post_data['author']['server']
    for h in entities.get("hashtags", []):
        text = text.replace(
          f"#{h}",
          f"<a href=\"https://{server}/tags/{h}\">#{h}</a>"
        )

    for u in entities.get("urls", []):
        text = text.replace(
          u['url'],
          f"<a href=\"{u['url']}\">{u['display_url']}</a>"
        )

    for um in entities.get("user_mentions", []):
        text = text.replace(
          f"@{um['label']}",
          f"<a href=\"{um['profile_url']}\">@{um['label']}</a>"
        )

    return text.strip()


def render_tweet_text(post_data):
    """
    Renders the text of a tweet as HTML.

    This includes:

    * Expanding any newlines
    * Replacing URLs and @-mentions
    * Replacing native emoji with Twitter's "twemoji" SVGs

    """
    text = post_data['text']
    entities = post_data.get("entities", {})

    # Newlines aren't significant in HTML; convert them to <br> tags.
    text = text.replace("\n", '<br>')

    # Expand any t.co URLs in the text with the actual link, which means
    # those links don't rely on Twitter or their link shortener.
    for u in entities.get("urls", []):
        text = text.replace(
          u['url'],
          f"<a href=\"{u['url']}\">{u['display_url']}</a>"
        )

    for um in entities.get("user_mentions", []):
        text = text.replace(
              f"@{um}",
              f"<a href=\"https://twitter.com/{um}\">@{um}</a>"
            )

    for h in entities.get("hashtags", []):
        text = text.replace(
          f"#{h}",
          f"<a href=\"https://twitter.com/hashtag/{h}\">#{h}</a>"
        )

    return text.strip()


def tweet_image(context, media) -> str:
    """
    Create a picture tag to show a media item on a tweet.
    """
    return render_picture(
        context,
        filename=media["filename"],
        images_subdir="social_embeds/twitter",
        alt=media.get("alt", ""),
        link_to=media["url"],
        width=585
    )
