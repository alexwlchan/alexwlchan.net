#!/usr/bin/env python
"""
Cache a tweet for use by the Twitter plugin.

I render tweets as static HTML embeds to reduce page weight.  This script
will cache all the data I need to render a tweet.

I don't include this functionality in the Jekyll Docker image because I
can only do this from a machine where I have Twitter API credentials in
the keychain.  It's not required most of the time, so I don't include it
(or the required libraries) inside the Docker image.

"""

import json
import os
import re
import sys
import urllib.request

import hyperlink
import keyring
from requests_oauthlib import OAuth1Session


def get_tweet_id_from_url(tweet_url):
    u = hyperlink.URL.from_text(tweet_url)

    # A tweet status should have a path of the form
    #
    #     /:author/status/:tweet_id
    #
    # If it doesn't have three parts, it doesn't match this structure
    # so it's not a tweet URL.
    if u.host not in {"twitter.com", "mobile.twitter.com"}:
        raise ValueError(f"Not a Twitter URL: {tweet_url}")

    # If you're looking at a photo on Twitter, it appends the photo
    # number to the URL, so the path becomes:
    #
    #     /:author/status/:tweet_id/photo/:num
    #
    # We don't care about this bit, so throw it away if present.
    try:
        if u.path[-2] == "photo" and u.path[-1].isnumeric():
            u = u.replace(path=tuple(u.path[:-2]))
    except IndexError:
        pass

    # Some Twitter.com URLs have a three-part path, but they're not
    # tweets.  For example:
    #
    #     https://twitter.com/settings/account/login_verification
    #
    # Don't try to parse these as tweet URLs.
    try:
        _, status, tweet_id = u.path
    except ValueError:
        raise ValueError(f"Not a tweet URL: {tweet_url}")

    if status != "status":
        raise ValueError(f"Not a tweet status: {tweet_url}")

    if not tweet_id.isnumeric():
        raise ValueError(f"Not a numeric tweet ID: {tweet_url}")

    return tweet_id


def get_screen_name_from_url(tweet_url):
    u = hyperlink.URL.from_text(tweet_url)
    return u.path[0]


def download_avatar(*, screen_name, tweet_id, tweet):
    avatar_url = tweet["user"]["profile_image_url_https"].replace("_normal", "")

    extension = avatar_url.split(".")[-1]  # ick
    avatar_path = os.path.join(
        "src", "_tweets", f"{screen_name}_{tweet_id}.{extension}"
    )

    urllib.request.urlretrieve(avatar_url, avatar_path)


def download_media(*, tweet):
    print(tweet.keys())
    if len(tweet["entities"]["media"]) > 1:
        raise RuntimeError("Too many media entities")

    for m in tweet["entities"]["media"]:
        media_url = m["media_url_https"]
        name = hyperlink.URL.from_text(media_url).path[-1]

        image_path = os.path.join("src", "_images", "twitter", name)
        urllib.request.urlretrieve(media_url, image_path)


if __name__ == "__main__":
    try:
        tweet_url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <TWEET_URL>")

    tweet_id = get_tweet_id_from_url(tweet_url)
    screen_name = get_screen_name_from_url(tweet_url)
    cache_file = os.path.join("src", "_tweets", f"{screen_name}_{tweet_id}.json")

    if os.path.exists(cache_file):
        sys.exit(0)

    sess = OAuth1Session(
        client_key=keyring.get_password("twitter", "consumer_api_key"),
        client_secret=keyring.get_password("twitter", "consumer_api_secret_key"),
        resource_owner_key=keyring.get_password("twitter", "access_token"),
        resource_owner_secret=keyring.get_password("twitter", "access_token_secret"),
    )

    # https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-show-id.html
    resp = sess.get(
        "https://api.twitter.com/1.1/statuses/show.json",
        params={
            "id": tweet_id,
            "trim_user": False,
            "include_ext_alt_text": True,
            "tweet_mode": "extended",
        },
    )
    resp.raise_for_status()

    tweet = resp.json()

    download_avatar(screen_name=screen_name, tweet_id=tweet_id, tweet=tweet)
    download_media(tweet=tweet)

    with open(cache_file, "w") as outfile:
        outfile.write(json.dumps(tweet, indent=2, sort_keys=True))
