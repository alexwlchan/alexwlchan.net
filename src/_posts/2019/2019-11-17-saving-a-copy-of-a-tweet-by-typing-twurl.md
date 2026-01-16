---
layout: post
date: 2019-11-17 11:38:06 +00:00
title: Saving a copy of a tweet by typing ;twurl
tags:
  - twitter
  - python
---

For years, I've been using a [Keyboard Maestro][km] snippet for getting the front URL from my running web browser.
If I type `;furl` anywhere on my Mac, it gets replaced with the URL of the frontmost browser window.
It saves me a few clicks, and it's an idea I originally stole [from Dr. Drang][drang].

I have a couple of variations on this snippet, and I recently added another one to the mix:

{% tweet https://twitter.com/alexwlchan/status/1188721070234394626 %}

[km]: https://www.keyboardmaestro.com/main/
[drang]: https://leancrew.com/all-this/2010/10/textexpander-snippets-for-google-chrome/

I often refer to tweets in notes -- for example, if I've seen something interesting that I want to look up later.
Tweet URLs only contain a username and a tweet ID, without any context, so they're hard to search for, and if the tweet is deleted, the URL becomes useless.
Adding a blockquote makes it easier to search for, and I know what the tweet was about if it gets deleted later.

What I want is something like this (in [Markdown][md] syntax):

{% code wrap="true" %}
https://twitter.com/alexwlchan/status/1188721070234394626:

> Today’s tiny automation win: if I’m looking at a tweet in my browser, I can type “;twurl” and get a link and blockquote with the text of the tweet wherever I’m typing.
>
> As a bonus, it automatically replaces t.​co URLs with the original URLs.
>
> 🐦 + 💻 + 🥳
{% endcode %}

[md]: https://daringfireball.net/projects/markdown/

I could create this with copy and paste, but I do it regularly and a script makes it a bit faster each time.
In this post, I'll explain how the script works: it's a nice example of how to use the Twitter API.



## Connecting to the Twitter API

If you want to connect to the Twitter API, you need to use OAuth.
You can apply for a developer account through Twitter's [developer portal](https://developer.twitter.com/en.html), then create an app with read-only access to your account.
That should give you some credentials for connecting to the API.
The credentials include a consumer API key and secret, and an access token and secret.

I recommend storing the credentials securely (using [keyring][keyring], for example).

Once we have the credentials, we can set up an OAuth session using [requests-oauthlib][rolib]:

{% code lang="python" names="0:keyring 1:get_password 2:requests_oauthlib 3:OAuth1Session 4:credentials 9:twitter_session" %}
from keyring import get_password
from requests_oauthlib import OAuth1Session


credentials = {
    "client_key":            get_password("twitter", "consumer_api_key"),
    "client_secret":         get_password("twitter", "consumer_api_secret"),
    "resource_owner_key":    get_password("twitter", "access_token"),
    "resource_owner_secret": get_password("twitter", "access_token_secret"),
}

twitter_session = OAuth1Session(**credentials)
{% endcode %}

If we make a request with this session, it will be authenticated using OAuth and our credentials.
For example, we can [check our credentials are correct][creds]:

{% code lang="python" names="0:resp" %}
resp = twitter_session.get(
    "https://api.twitter.com/1.1/account/verify_credentials.json"
)

print(resp)
# <Response [200]>

print(resp.text)
# {"id":66351897,"id_str":"66351897","name":"Alex Chan"...
{% endcode %}

Now we can talk to the Twitter API.

[keyring]: https://pypi.org/project/keyring/
[rolib]: https://pypi.org/project/requests-oauthlib/
[creds]: https://developer.twitter.com/en/docs/accounts-and-users/manage-account-settings/api-reference/get-account-verify_credentials



## Fetching a single tweet from the Twitter API

There's [an API endpoint][endpoint] that lets us look up a single tweet (or as the Twitter API calls it, "status").
We have to pass an `id` parameter with the numeric ID of the tweet.
Here's what that looks like:

{% code lang="python" names="0:get_tweet 1:twitter_session 2:tweet_id 3:resp 12:tweet" %}
def get_tweet(twitter_session, *, tweet_id):
    resp = twitter_session.get(
        "https://api.twitter.com/1.1/statuses/show.json",
        params={"id": tweet_id}
    )

    resp.raise_for_status()
    return resp.json()


tweet = get_tweet(twitter_session, tweet_id="1188721070234394626")
print(tweet)
# {'id': 1188721070234394626, ...
{% endcode %}

This makes the request, checks it was a 200 OK (that's the `raise_for_status` line), and if all is well, parses the JSON body and returns a Python dict.
I'm using Python 3's [keyword-only arguments][kwargs] (the `*`) to force callers to pass the `tweet_id` parameter explicitly.

If you look carefully at the response, you'll see you only get half the text of the tweet:

{% code lang="python" %}
{
  'id': 1188721070234394626,
  'text': 'Today’s tiny automation win: if I’m looking at a tweet in my browser, I can type “;twurl” and get a link and blockq… https://t.co/Z0OB84aNFZ',
  'truncated': True,
  ...
{% endcode %}

About two years ago, Twitter doubled the character limit of tweets from 140 to 280.
Some of their APIs return tweets truncated to 140 characters, so they don't break older clients which weren't updated for this change.
If you want to get the longer tweets, you have to opt in, by passing `tweet_mode=extended`:

{% code lang="python" names="0:get_tweet 1:twitter_session 2:tweet_id 3:resp 12:tweet" %}
def get_tweet(twitter_session, *, tweet_id):
    resp = twitter_session.get(
        "https://api.twitter.com/1.1/statuses/show.json",
        params={"id": tweet_id, "tweet_mode": "extended"}
    )

    resp.raise_for_status()
    return resp.json()


tweet = get_tweet(twitter_session, tweet_id="1188721070234394626")
print(tweet["truncated"])
# False
{% endcode %}

I'm not sure how you're meant to discover this -- there are [some docs for this parameter][extended], but it's not mentioned in the list of parameters for the "lookup tweet" endpoint.
I remember seeing this when the change first happened, and I've been copying it among my Twitter scripts ever since, but it seems non-obvious to a newcomer.

There are other parameters you can pass to this API endpoint, but the ID and tweet mode are all we need for this particular script.

[endpoint]: https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-show-id
[extended]: https://developer.twitter.com/en/docs/tweets/tweet-updates
[kwargs]: https://www.python.org/dev/peps/pep-3102/



## Getting the tweet ID from a URL

We get a URL from our web browser, but what the Twitter API wants is a numeric tweet ID.
We need to extract that ID from the URL.

There are lots of ways to do this; personally I reach for the [hyperlink] library, which is a great little Python library for manipulating URLs:

{% code lang="python" names="0:hyperlink 1:get_tweet_id 2:url 3:u 14:tweet_id 25:tweet_id" %}
import hyperlink


def get_tweet_id(url):
    u = hyperlink.URL.from_text(url)

    if u.host not in {"twitter.com", "mobile.twitter.com"}:
        raise ValueError("Not a Twitter URL: %s" % url)

    # A tweet status should have a path of the form
    #
    #     /:author/status/:tweet_id
    #
    # If it doesn't have three parts, it doesn't match this structure
    # so it's not a tweet URL.
    try:
        _, _, tweet_id = u.path
    except IndexError:
        raise ValueError("Not a tweet URL: %s" % url)

    # Some Twitter.com URLs have a three-part path, but they're not
    # tweets.  For example:
    #
    #     https://twitter.com/settings/account/login_verification
    #
    # Don't try to parse these as tweet URLs.
    if not tweet_id.isnumeric():
        raise ValueError("Not a tweet URL: %s" % url)

    return tweet_id


tweet_id = get_tweet_id(
    url="https://twitter.com/alexwlchan/status/1188721070234394626"
)
print(tweet_id)
# 1188721070234394626
{% endcode %}

I've tried to be a bit defensive here, and spot when I've accidentally passed in something which isn't a tweet URL.
You could be even stricter -- for example, checking for `/status/` in the URL, or checking the numeric ID is the correct length -- but since this is a script that will only run on my computer with URLs from my web browser, it's good enough.
It'll spot mistakes, without being too complicated.

[hyperlink]: https://pypi.org/project/hyperlink/



## Rendering the tweet as Markdown

So now we have the tweet response, let's render it as Markdown.

We can start by getting the tweet URL, and prefixing the text of the tweet with angle brackets to make a blockquote:

{% code lang="python" names="0:render_tweet 1:tweet 2:user 4:tweet_id 6:tweet_text 8:url 11:lines 13:tweet_line" %}
def render_tweet(tweet):
    user = tweet["user"]["screen_name"]
    tweet_id = tweet["id"]
    tweet_text = tweet["full_text"]

    url = f"https://twitter.com/{user}/status/{tweet_id}"

    lines = [
        f"{url}:",
        "",
    ]

    for tweet_line in tweet_text.splitlines():
        lines.append(f"> {tweet_line}")

    return "\n".join(lines)
{% endcode %}

Note that this function returns a string, rather than printing it directly -- this lets the caller decide what to do with the string.
Maybe they'll print it, or maybe they'll save it to a file, or a database, or something else.

If the text of the tweet includes a link, it will be a t.co link from Twitter's [link-shortening service][tco].
It's more useful to replace those links with the original link, both for readability and long-term usefulness.
Handily, the Twitter API response includes both the t.co URL and the URL that it points to.

We can add them to the text like so:

{% code lang="python" names="0:render_tweet 1:tweet 2:width 3:all_entities 10:entity 17:tweet_line" %}
def render_tweet(tweet, width=72):
    ...

    all_entities = (
        tweet["entities"]["urls"] +
        tweet["entities"].get("media", []) +
        tweet.get("extended_entities", {}).get("media", [])
    )

    for entity in all_entities:
        tweet_text = tweet_text.replace(
            entity["url"], entity["expanded_url"]
        )

    for tweet_line in tweet_text.splitlines():
    ...
{% endcode %}

Only the length of the t.co URL counts against your character limit, regardless of how long the original URL is.
That wasn't always the case -- the full URL used to count against the limit, so people used other shorteners like [TinyURL] or [Bitly] to shorten their links.
If you wanted to unwrap those links as well, this would be a good place to do it.
In practice, I don't see tweets like that any more, so I haven't implemented that here.

[TinyURL]: https://en.wikipedia.org/wiki/TinyURL
[Bitly]: https://en.wikipedia.org/wiki/Bitly
[tco]: https://en.wikipedia.org/wiki/Twitter#URL_shortener



## Putting it all together

This is the final version of the script:

{% code lang="python" names="0:sys 1:hyperlink 2:keyring 3:get_password 4:requests_oauthlib 5:OAuth1Session 6:create_twitter_session 7:credentials 14:get_tweet 15:twitter_session 16:tweet_id 17:resp 26:get_tweet_id 27:url 28:u 39:tweet_id 50:render_tweet 51:tweet 52:width 53:user 55:tweet_id 57:tweet_text 59:url 62:lines 64:all_entities 71:entity 78:tweet_line 87:tweet_url 94:twitter_session 96:tweet_id 99:tweet" %}
import sys

import hyperlink
from keyring import get_password
from requests_oauthlib import OAuth1Session


def create_twitter_session():
    """
    Creates an OAuth session that authenticates with the Twitter API.
    """
    credentials = {
        "client_key":            get_password("twitter", "consumer_api_key"),
        "client_secret":         get_password("twitter", "consumer_api_secret"),
        "resource_owner_key":    get_password("twitter", "access_token"),
        "resource_owner_secret": get_password("twitter", "access_token_secret"),
    }

    return OAuth1Session(**credentials)


def get_tweet(twitter_session, *, tweet_id):
    """
    Fetch a single tweet from the Twitter API.
    """
    # We have to pass tweet_mode=extended, or we get truncated text
    # from the Twitter API.
    # See https://developer.twitter.com/en/docs/tweets/tweet-updates
    resp = twitter_session.get(
        "https://api.twitter.com/1.1/statuses/show.json",
        params={"id": tweet_id, "tweet_mode": "extended"}
    )

    resp.raise_for_status()
    return resp.json()


def get_tweet_id(url):
    """
    Given the URL of a tweet, return its numeric tweet ID.
    """
    u = hyperlink.URL.from_text(url)

    # A tweet status should have a path of the form
    #
    #     /:author/status/:tweet_id
    #
    # If it doesn't have three parts, it doesn't match this structure
    # so it's not a tweet URL.
    if u.host not in {"twitter.com", "mobile.twitter.com"}:
        raise ValueError("Not a Twitter URL: %s" % url)

    # Some Twitter.com URLs have a three-part path, but they're not
    # tweets.  For example:
    #
    #     https://twitter.com/settings/account/login_verification
    #
    # Don't try to parse these as tweet URLs.
    try:
        _, _, tweet_id = u.path
    except IndexError:
        raise ValueError("Not a tweet URL: %s" % url)

    if not tweet_id.isnumeric():
        raise ValueError("Not a tweet URL: %s" % url)

    return tweet_id


def render_tweet(tweet, width=72):
    """
    Given a tweet from the Twitter API, render it in Markdown.
    """
    user = tweet["user"]["screen_name"]
    tweet_id = tweet["id"]
    tweet_text = tweet["full_text"]

    url = f"https://twitter.com/{user}/status/{tweet_id}"

    lines = [
        f"{url}:",
        ""
    ]

    # Replace any t.co short URLs in the text of the tweet with
    # the original URLs that they point to.
    all_entities = (
        tweet["entities"]["urls"] +
        tweet["entities"].get("media", []) +
        tweet.get("extended_entities", {}).get("media", [])
    )

    for entity in all_entities:
        tweet_text = tweet_text.replace(
            entity["url"], entity["expanded_url"]
        )

    for tweet_line in tweet_text.splitlines():
        lines.append(f"> {tweet_line}")

    return "\n".join(lines)


if __name__ == '__main__':
    try:
        tweet_url = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <TWEET_URL>")

    twitter_session = create_twitter_session()
    tweet_id = get_tweet_id(tweet_url)
    tweet = get_tweet(twitter_session, tweet_id=tweet_id)
    print(render_tweet(tweet))
{% endcode %}

It's divided up into small functions, so I can copy/paste bits into another script if it's useful.
I invoke it by running the script with the tweet URL as a single argument:

{% code lang="console?prompt=$" wrap="true" %}
$ python get_tweet_md.py "twitter.com/alexwlchan/status/1188721070234394626"
https://twitter.com/alexwlchan/status/1188721070234394626:

> Today’s tiny automation win: if I’m looking at a tweet in my browser, I can type “;twurl” and get a link and blockquote with the text of the tweet wherever I’m typing.
>
> As a bonus, it automatically replaces t.​co URLs with the original URLs.
>
> 🐦 + 💻 + 🥳
{% endcode %}

This is then wired up using Keyboard Maestro, so typing `;twurl` runs the script with the frontmost browser window as the argument.
I've already used it a bunch of times to write down something to look at later (most recently, [Rust apps on Glitch](https://twitter.com/Sunjay03/status/1195013347281788928)), and I expect to keep using it as I save things from Twitter.

As always, writing out this code in detail made it better.
There were several parts of the original code that were unclear, and now it has some comments and docstrings around the fiddly bits.
I also looked at the [textwrap module] and learnt how that worked, even though I didn't use any of it.
If you ever want to understand something in detail, explain it to somebody else.

[textwrap module]: https://docs.python.org/3/library/textwrap.html
