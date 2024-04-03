"""
The source code for KempisBot, a Twitter bot to post "The Imitation of Christ" as a
series of tweets.

This isn't the exact code running on the server -- I've tidied it up a bit, added
some comments, and removed some uninteresting code related to my particular server.
The point of sharing this is to give you ideas for your own scripts, not to be
something you run unmodified.

Inputs:

*   A set of Twitter API credentials with write permissions.  I used ``oauth_dance()``
    from the Python ``twitter`` library to get the credentials used by the bot, then
    keyring to securely store/load the credentials.

*   A file full of tweets, with each new tweet separated by three dashes, e.g.

        ‘The Imitation of Christ’, by Thomas à Kempis
        ---
        THE FIRST BOOK: Admonitions Profitable For The Spiritual Life
        ---
        CHAPTER I: Of the imitation of Christ, and of contempt of the world and all its vanities

"""

import datetime
import json
import os
import sys

# `pip install keyring` ~ for credentials management
# See https://alexwlchan.net/2016/11/you-should-use-keyring/
import keyring

# `pip install twitter` ~ for connecting to the Twitter API
import twitter


if __name__ == "__main__":
    print("---")
    print(f"Running at {datetime.datetime.now().isoformat()}")

    twitter = twitter.Twitter(
        auth=twitter.OAuth(
            consumer_key=keyring.get_password("KempisBot", "consumer_key"),
            consumer_secret=keyring.get_password("KempisBot", "consumer_secret"),
            token=keyring.get_password("KempisBot", "token"),
            token_secret=keyring.get_password("KempisBot", "token_secret"),
        )
    )

    # Read all the tweets from the file.
    DIR = os.path.dirname(__file__)

    tweets = [
        t.strip()
        for t in open(os.path.join(DIR, "tweets.txt"))
        .read()
        .split("---")
    ]

    # I considered using a proper database to coordinate different tweets, but this
    # script only runs on a persistent, always-on machine.
    #
    # You could do something fancy with serverless, but a text file that records the
    # last tweet posted is good enough.
    try:
        last_posted = open(os.path.join(DIR, "last_posted.txt")).read().strip()
        assert last_posted in tweets
        next_tweet_idx = tweets.index(last_posted) + 1
    except FileNotFoundError:
        next_tweet_idx = 0

    try:
        next_tweet = tweets[next_tweet_idx]
    except IndexError:
        print("No more tweets!")
        sys.exit(0)

    print(f"About to post:\n{next_tweet!r}")
    assert len(next_tweet) <= 280

    resp = twitter.statuses.update(status=next_tweet)
    with open(os.path.join(DIR, "last_posted.txt"), "w") as outfile:
        outfile.write(next_tweet)
    print(f"Response from Twitter: {json.dumps(resp)}")