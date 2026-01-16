---
layout: til
title: Looking up posts in the Bluesky API
summary: Install the `atproto` package, construct a client with your username/password, then call the `get_post_thread` method with your `at://` URI.
date: 2025-08-10 22:53:18 +01:00
tags:
  - bluesky
  - python
---
I wanted to use the [Bluesky API][api] to get some basic information about posts.
It wasn't difficult, but there were a couple of non-obvious steps I wanted to note.

1.  **Install the [`atproto` package][atproto]:**

    ```console
    $ pip install atproto
    ```

2.  **Create an authentication session:**

    ```python
    from atproto import Client
    
    client = Client()
    client.login(username, password)
    ```
    
    The username needs to be a full domain name, e.g. `alexwlchan.bsky.social` -- I initially tried just `alexwlchan`, but that doesn't work.
    
    You can use your regular Bluesky account password, but it also supports [per-app passwords], so I used one of those instead.

3.  **Call the [`get_post_thread` method][getPostThread].**
    This method includes information about the replies and parents, but I'm just interested in a single post:

    ```python
    api_resp = client.get_post_thread(
        uri="at://discobooks.bsky.social/app.bsky.feed.post/3lvgbcnv5vs2a",
        depth=0,
        parent_height=0
    )
    ```
    
    The URI needs to be an `at://` URI, which is a URI scheme specific to [ATProto].
    I don't understand all the possibilities; I just based this on an example I found elsewhere in the docs.
    
4.  **Interpret the API response.**
    The API docs have a loose description of the output, but I found it more helpful to dump the response as JSON and inspect it by hand:
    
    ```python
    print(api_resp.model_dump_json(indent=2))
    ```
    
    This allowed me to find the fields I wanted, and extract them into a simpler structure:
    
    ```python
    from datetime import datetime
    
    post = api_resp.thread.post
    
    my_data = {
        "author": post.author.handle,
        "date_posted": datetime.fromisoformat(post.record.created_at),
        "text": post.record.text,
    }
    
    pprint(my_data)
    ```
    
    Here's an example of the output this prints:
    
    ```python
    {'author': 'discobooks.bsky.social',
     'date_posted': datetime.datetime(2025, 8, 2, 13, 26, 8, 603000, tzinfo=datetime.timezone.utc),
     'text': 'My partner just uttered the most loving words a person can utter:\n'
             '\n'
             '“You have too many books. They’re all over the place. \n'
             'I’m gonna buy you a new bookcase.”\n'
             '\n'
             'He’s a good man Savannah, a GOOD MAN.'}
    ```

[api]: https://docs.bsky.app/docs/get-started
[atproto]: https://pypi.org/project/atproto/
[per-app passwords]: https://bsky.app/settings/app-passwords
[getPostThread]: https://docs.bsky.app/docs/tutorials/viewing-threads
[ATProto]: https://en.wikipedia.org/wiki/Atproto
