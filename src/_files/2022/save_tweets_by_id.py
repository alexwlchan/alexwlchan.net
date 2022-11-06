#!/usr/bin/env python3

import itertools
import json

# requests-oauthlib==1.3.0
from requests_oauthlib import OAuth1Session


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


if __name__ == "__main__":
    # Fill in Twitter API v1 credentials
    sess = OAuth1Session(
        client_key=CONSUMER_API_KEY,
        client_secret=CONSUMER_API_SECRET_KEY,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_TOKEN_SECRET,
    )
    
    # Fetch the tweet IDs from a file, or a hard-coded list, or some other function
    TWEET_IDS = []

    with open("tweets.json", "w") as outfile:
        # You can get up to 100 tweets at once with the statuses/lookup API.
        # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-statuses-lookup
        for batch in chunked_iterable(TWEET_IDS, size=100):

            params = {
                "id": ",".join(batch),
                "trim_user": True,
                "include_ext_alt_text": True,
                "tweet_mode": "extended",
            }
            resp = sess.get(
                "https://api.twitter.com/1.1/statuses/lookup.json", params=params
            )
            resp.raise_for_status()

            for tweet in resp.json():
                outfile.write(json.dumps(tweet) + "\n")
