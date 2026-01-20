"""
Models for the social media embed data in `social_embeds.json`.
"""

from typing import Literal, NotRequired, TypedDict


__all__ = [
    "BlueskyEmbed",
    "MastodonEmbed",
    "MediaEntity",
    "SocialEmbedData",
    "TwitterEmbed",
]


class MediaEntity(TypedDict):
    """
    A media entity on a microblog post.
    """

    filename: str
    url: str
    type: Literal["photo"]

    # TODO: This should just be `alt_text` or similar
    ext_alt_text: NotRequired[str]


class UrlEntity(TypedDict):
    """
    A URL entity on a microblog post.
    """

    url: str
    display_url: str


class Entities(TypedDict):
    """
    Entities on a microblog post.
    """

    hashtags: list[str]
    media: list[MediaEntity]
    urls: list[UrlEntity]
    user_mentions: list[str]


class BlueskyUser(TypedDict):
    """
    Information about a user on Bluesky.
    """

    name: str
    handle: str


class BlueskyEmbed(TypedDict):
    """
    Post data for an embedded Bluesky skeet.
    """

    site: Literal["bluesky"]
    id: str
    author: BlueskyUser
    date_posted: str
    text: str
    quoted_post: NotRequired["BlueskyEmbed"]


class MastodonUser(TypedDict):
    """
    Information about a user on Mastodon.
    """

    server: str
    display_name: str
    username: str


MastodonUserMention = TypedDict(
    "MastodonUserMention", {"label": str, "profile_url": str}
)


class MastodonEntities(TypedDict):
    """
    Entities on a Mastodon post.
    """

    hashtags: list[str]
    media: list[MediaEntity]
    urls: list[UrlEntity]
    user_mentions: list[MastodonUserMention]


class MastodonEmbed(TypedDict):
    """
    Post data for an embedded Mastodon toot.
    """

    site: Literal["mastodon"]
    id: str
    author: MastodonUser
    date_posted: str
    text: str
    entities: NotRequired[MastodonEntities]


class TwitterUser(TypedDict):
    """
    Information about a user on Twitter.
    """

    name: str
    screen_name: str


class TwitterEmbed(TypedDict):
    """
    Post data for an embedded tweet.
    """

    site: Literal["twitter"]
    id: str
    author: TwitterUser
    date_posted: str
    text: str
    entities: NotRequired[Entities]
    quoted_status: NotRequired["TwitterEmbed"]


class YouTubeEmbed(TypedDict):
    """
    Post data for an embedded YouTube video.
    """

    site: Literal["youtube"]
    title: str


SocialEmbedData = BlueskyEmbed | MastodonEmbed | TwitterEmbed | YouTubeEmbed
