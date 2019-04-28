---
layout: post
title: Reversing a t.co URL to the original tweet
summary: Twitter uses t.co to shorten links in tweets, so I wrote some Python to take a t.co URL and find the original tweet.
tags:
---

If you post a link on Twitter, it goes through Twitter's [t.co link-shortening service][tco].
The link in the tweet text is replaced with a t.co URL, and that URL redirects to the original destination.

{%
  image
  :filename => "tco_urls.png",
  :alt => "A flow chart: A tweet contains a t.co URL, and a t.co URL redirects to the destination.",
  :use_href => false,
  :style => "width: 719px;"
%}

If you're just reading Twitter, the presence of t.co is mostly invisible -- it's not shown in the interface, and if you click on a URL you get to the original destination.

A t.co URL is an [HTTP 301 Redirect][http_301] to the destination, which any browser or HTTP client can follow (as long as Twitter keeps running the service).
For example:

```pycon
>>> import requests
>>> resp = requests.head("https://t.co/mtXLLfYOYE")
>>> resp.status_code
301
>>> resp.headers["Location"]
'https://www.bbc.co.uk/news/blogs-trending-47975564'
```

But what if you only have the t.co URL, and you want to find the original tweet?
For example, I see t.co URLs in my referrer logs -- people linking to my blog -- and I want to know what they're saying about me!

Twitter don't provide a public API for doing this, so there's no perfect way to reverse a t.co URL back to its source.
I have found a couple of ways to do it, and in this post I'll explain how.

[tco]: https://help.twitter.com/en/using-twitter/url-shortener
[http_301]: https://en.wikipedia.org/wiki/HTTP_301



## The manual approach

If you search for a t.co URL in Twitter, you can see tweets which include it.
If the twet is recent and visible to you, it shows up in the results:

{%
  image
  :filename => "twitter_search_single.png",
  :alt => "Searching for a t.co URL with a single result.",
  :override_href => "https://twitter.com/search?q=https%3A%2F%2Ft.co%2F1AbEHY2P6b",
  :style => "width: 597px;"
%}

Sometimes you might find multiple tweets that include the same URL.
I've seen this happen when somebody posts the same link several times:

{%
  image
  :filename => "twitter_search_multiple.png",
  :alt => "Searching for a t.co URL with multiple results.",
  :override_href => "https://twitter.com/search?q=https%3A%2F%2Ft.co%2FFACNrWdMu4",
  :style => "width: 597px;"
%}

If you only need to search for a couple of URLs, this is probably fine.



## The Python approach

Because I need to do this a lot, I wanted to automate the process
Twitter have a [search API] which provides similar data to the Twitter website, so by calling this API we can mimic the search interface.
I wrote a Python script to do it for me, which I'll walk through below

First we need to authenticate with the Twitter API.
You'll need some Twitter API credentials, which you can get through [Twitter's developer site].

In the past I used [tweepy] to connect to the Twitter APIs, but these days I prefer to use the [requests-oauthlib library] and make direct requests.
We create an OAuth session:

```python
from requests_oauthlib import OAuth1Session

sess = OAuth1Session(
    client_key=TWITTER_CONSUMER_KEY,
    client_secret=TWITTER_CONSUMER_SECRET,
    resource_owner_key=TWITTER_ACCESS_TOKEN,
    resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET
)
```

Then we can call the search API like so:

```python
resp = sess.get(
    "https://api.twitter.com/1.1/search/tweets.json",
    params={
        "q": TCO_URL,
        "count": 100,
    }
)
```

The `q` parameter is the search query, which in this case is the t.co URL.
We get as many tweets as possible (you're allowed up to 100 tweets in a single request).

We extract the tweets like so:

```python
statuses = resp.json()["statuses"]
```

The API represents every retweet as an individual status, so a tweet with three retweets would have four entries in this response -- one for the original tweet, and three more for each of the retweets.
The Twitter web UI handles that for us, and consolidates them into a single result.
We have to do that manually.

If a tweet from the API is a retweet, it has a `retweeted_status` key that contains the original tweet.
Let's look for that, and build tweet URLs accordingly:

```python
tweet_urls = set()

for status in statuses:
    try:
        tweet = status["retweeted_status"]
    except KeyError:
        tweet = status

    url = "https://twitter.com/%s/status/%s" % (
        tweet["user"]["screen_name"], tweet["id_str"]
    )

    tweet_urls.add(url)
```

This gives us the URLs for tweets that use or mention the t.co URL we were looking for.

If we want to be stricter, we could check that these tweets include the t.co short URL in their URL entities.
(In the Twitter API, an "entity" is metadata or extra context for the tweet -- images, videos, URLs, that sort of thing.)
We add `"include_entities": True` to the parameters in our API call, then modify our `for` loop slightly:

```python
for status in statuses:
    ...

    if not any(u["url"] == TCO_URL for u in tweet["entities"]["urls"]):
        continue

    url = "..."
```

Putting this all together gives us the following function:

```python
from requests_oauthlib import OAuth1Session


sess = OAuth1Session(
    client_key=TWITTER_CONSUMER_KEY,
    client_secret=TWITTER_CONSUMER_SECRET,
    resource_owner_key=TWITTER_ACCESS_TOKEN,
    resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET
)


def find_tweets_using_tco(tco_url):
    """
    Given a shortened t.co URL, return a set of URLs for tweets that use this URL.
    """
    # See https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
    resp = sess.get(
        "https://api.twitter.com/1.1/search/tweets.json",
        params={
            "q": tco_url,
            "count": 100,
            "include_entities": True
        }
    )

    statuses = resp.json()["statuses"]

    tweet_urls = set()

    for status in statuses:
        # A retweet shows up as a new status in the Twitter API, but we're only
        # interested in the original tweet.  If this is a retweet, look through
        # to the original.
        try:
            tweet = status["retweeted_status"]
        except KeyError:
            tweet = status

        # If this tweet shows up in the search results for a reason other than
        # "it has this t.co URL as a short link", it's not interesting.
        if not any(u["url"] == tco_url for u in tweet["entities"]["urls"]):
            continue

        url = "https://twitter.com/%s/status/%s" % (
            tweet["user"]["screen_name"], tweet["id_str"]
        )

        tweet_urls.add(url)

    return tweet_urls
```

I've been using this code to reverse t.co URLs that appear in my web analytics for a while now.
It works about as well as the website but I find it quicker to use.

[search API]: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
[Twitter's developer site]: https://developer.twitter.com/en/apps
[tweepy]: https://github.com/tweepy/tweepy
[requests-oauthlib library]: https://github.com/requests/requests-oauthlib



## Limitations

Not all t.co URLs come from a tweet.

If you post a link in your profile, that gets shortened as well.
But as far as I can tell, there's no way to go from a shortened profile link back to the original profile page.
If you search for the shortened URL, you don't find anything.

Also, if the original tweet is an account you can't see (maybe they're private or they've blocked you), their tweet won't show up in your searches.


