"""
Models for the social media embed data in `social_embeds.json`.
"""

from typing import Any, Literal, Optional

from pydantic import BaseModel


__all__ = [
    "BlueskyEmbed",
    "MastodonEmbed",
    "MediaEntity",
    "SocialEmbedData",
    "TwitterEmbed",
    "parse_social_embed_data",
]


class MediaEntity(BaseModel):
    """
    A media entity on a microblog post.
    """

    filename: str
    url: str
    type: Literal["photo"]

    # TODO: This should just be `alt_text` or similar
    ext_alt_text: str | None = None


class UrlEntity(BaseModel):
    """
    A URL entity on a microblog post.
    """

    url: str
    display_url: str


class Entities(BaseModel):
    """
    Entities on a microblog post.
    """

    hashtags: list[str]
    media: list[MediaEntity]
    urls: list[UrlEntity]
    user_mentions: list[str]


class BlueskyUser(BaseModel):
    """
    Information about a user on Bluesky.
    """

    name: str
    handle: str


class BlueskyEmbed(BaseModel):
    """
    Post data for an embedded Bluesky skeet.
    """

    site: Literal["bluesky"]
    id: str
    author: BlueskyUser
    date_posted: str
    text: str
    quoted_post: Optional["BlueskyEmbed"] = None


class MastodonUser(BaseModel):
    """
    Information about a user on Mastodon.
    """

    server: str
    display_name: str
    username: str


class MastodonUserMention(BaseModel):
    """
    A user who's @-mentioned in a Mastodon post.
    """

    label: str
    profile_url: str


class MastodonEntities(BaseModel):
    """
    Entities on a Mastodon post.
    """

    hashtags: list[str]
    media: list[MediaEntity]
    urls: list[UrlEntity]
    user_mentions: list[MastodonUserMention]


class MastodonEmbed(BaseModel):
    """
    Post data for an embedded Mastodon toot.
    """

    site: Literal["mastodon"]
    id: str
    author: MastodonUser
    date_posted: str
    text: str
    entities: MastodonEntities | None = None


class TwitterUser(BaseModel):
    """
    Information about a user on Twitter.
    """

    name: str
    screen_name: str


class TwitterEmbed(BaseModel):
    """
    Post data for an embedded tweet.
    """

    site: Literal["twitter"]
    id: str
    author: TwitterUser
    date_posted: str
    text: str
    entities: Entities | None = None
    quoted_status: Optional["TwitterEmbed"] = None


class YouTubeEmbed(BaseModel):
    """
    Post data for an embedded YouTube video.
    """

    site: Literal["youtube"]
    title: str


SocialEmbedData = BlueskyEmbed | MastodonEmbed | TwitterEmbed | YouTubeEmbed


def parse_social_embed_data(data: Any) -> SocialEmbedData:
    """
    Parse a blob of social embed data from JSON.
    """
    match data["site"]:
        case "bluesky":
            return BlueskyEmbed(**data)
        case "mastodon":
            return MastodonEmbed(**data)
        case "twitter":
            return TwitterEmbed(**data)
        case "youtube":
            return YouTubeEmbed(**data)
        case _:  # pragma: no cover
            raise ValueError(f"unrecognised site: {data['site']!r}")
