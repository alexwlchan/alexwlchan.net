---
layout: post
date: 2018-08-07 15:48:53 +0000
title: Finding slow builds in Travis
summary: A Python snippet for using the Travis CI API to track build times.
tags: travis python
category: Programming and code
---

For a while, I've been whinging on Twitter about Scala compile times -- mostly driven by the ever-increasing length of the Travis builds at work.

Somebody made a comment on Friday about how we don't really track our build times, just our gut feeling.
*"They seem to be getting slower."*
Since the [Travis API][api] provides a whole heap of information about builds, I decided to dig into the data to find a pattern.

This post contains the code I used, in case it's useful to somebody else.

<!-- summary -->

## A helper for the Travis API

First I wrote a helper for accessing the Travis API.
This is what it looks like:

```python
import requests


class TravisSession:

    def __init__(self, token, user_agent):
        self.sess = requests.Session()

        # https://developer.travis-ci.com/gettingstarted
        self.sess.headers = {
            'Travis-API-Version': '3',
            'User-Agent': user_agent,
            'Authorization': f'token {token}',
        }

        def check_for_error(resp, *args, **kwargs):
            resp.raise_for_status()

        self.sess.hooks['response'].append(check_for_error)

    def get(self, endpoint, *args, **kwargs):
        url = f'https://api.travis-ci.org/{endpoint.lstrip("/")}'
        return self.sess.get(url, *args, **kwargs).json()
```

The `__init__` method creates a [requests.Session instance][session], which gives you nice behaviour like shared headers and persistent connections.
In particular, I can set the [required headers][headers] once, and then I get them on every request.
The headers include an access token from the [Travis client][client], and a user agent string that identifies the requests.

I'm also setting a hook to throw an exception if I get a bad response from the API -- I've [written about requests' hooks][hooks] before.

Then the `get()` method mimics `requests.get()`, but prepends the API URL for me, and unwraps the JSON response as a Python dict with `.json()`.

Here's how you might use this class:

```python
sess = TravisSession(
    token='abcdefghij',
    user_agent='example_script.py by alexwlchan')

sess.get('/repo/wellcometrust%2Fplatform/builds')
```

This exam,ple would tell you about the builds in the platform repo.

## An iterator for all builds

Next up is to use the [builds API][builds] to get a list of builds from the repository.
This function takes the Travis client above, and iterates over all the builds:

```python
from urllib.parse import quote_plus


def all_builds(sess, repo_name):
    params = {}
    while True:
        resp = sess.get(f'/repo/{quote_plus(repo_name)}/builds', params=params)
        yield from resp['builds']
        params['offset'] = params.get('offset', 0) + len(resp['builds'])
        if resp['@pagination']['is_last']:
            break
```

The Travis API is paginated, but this function hides that detail -- to the caller, it's just a continuous stream of individual builds.

In a nice detail I haven't seen before, the Travis API also saves me doing any pagination logic, by exposing an `is_last` boolean that I can use to terminate my loop.

## Putting it together

With these two helpers in hand, I got a list of build times like so:

```python
sess = TravisSession(
    token=TOKEN,
    user_agent='track_build_times.py by alexwlchan'
)

for build in all_builds(sess=sess, repo_name='wellcometrust/platform'):
    if build['event_type'] != 'cron':
        continue
    print((build['finished_at'], build['duration']))
```

Our overnight cron jobs run a consistent suite of tests (PRs and pushes have some early-finish logic that makes their build times hard to compare).
They also run late in the evening, outside our normal working hours, so there's no contention for Travis build workers.

Skimming the results quickly showed that, yes, our builds have slowed down recently:

```
('2018-06-27T21:38:35Z', 10244)
('2018-06-26T21:40:41Z', 10600)
('2018-06-26T09:17:20Z', 10858)
('2018-06-24T21:23:18Z',  4621)
('2018-06-23T21:38:08Z',  4578)
('2018-06-22T21:31:51Z',  4634)
```

The results also give us an idea of where we introduced a slowdown, and we can start reviewing changes from around that time to identify the cause.
We haven't found a definite cause yet, but we're a lot closer than we were before.

[api]: https://developer.travis-ci.com/
[session]: http://docs.python-requests.org/en/master/user/advanced/#session-objects
[headers]: https://developer.travis-ci.com/gettingstarted
[client]: https://developer.travis-ci.com/authentication
[hooks]: /2017/10/requests-hooks/
[builds]: https://developer.travis-ci.com/resource/builds#Builds
