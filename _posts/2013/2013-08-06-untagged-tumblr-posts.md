---
date: 2013-08-06 09:52:00 +0000
layout: post
slug: untagged-tumblr-posts
tags: tumblr, python
title: Finding untagged posts on Tumblr
---

Yesterday one of my friends was going through her old Tumblr posts, trying to add tags to every post. If you have any more than a handful of posts, then this becomes tedious and difficult, and you've no guarantee that you tagged them all when you're done. Tumblr doesn't have a built-in way to list all of your untagged posts, so I wrote a script to poll the [Tumblr API][api], and get a list of post URLs which didn't have tags.

Doing a Google search for this topic, it seems that this is a fairly common problem, so I thought I'd post the script here for other people to use.

<!-- summary -->

The script itself is fairly simple:

```python
import urllib2
import json

hostname = "example.tumblr.com"
api_key = "abcdefg"

url = "http://api.tumblr.com/v2/blog/{host}/posts?api_key={key}".format(host=hostname, key=api_key)

def api_response(url):
    req = urllib2.urlopen(url)
    return json.loads(req.read())

jsonresponse = api_response(url)
post_count = jsonresponse["response"]["total_posts"]
increments = (post_count + 20) / 20

for i in range(0, increments):
    jsonresponse = api_response("{url}&offset={count}".format(url=url, count=i * 20))
    posts = jsonresponse["response"]["posts"]

    for i in range (0, len(posts)):
        if not posts[i]["tags"]:
            print posts[i]["post_url"]

print "All finished!"
```

The only notable feature of the script is that it gets posts in batches of 20, because the Tumblr API only returns up to 20 posts at a time. Everything else is either standard Python or follows from the way that Tumblr structure their API responses.

To use the script, you need to [download it](/files/untagged-posts.py) and change the parameters in lines 6 and&nbsp;7. The hostname is the URL of your Tumblr site. Quoting directly from the [Tumblr API documentation][api]:

> Each blog has a unique hostname. The hostname can be standard or custom.
>
> * Standard hostname: the blog short name + `.tumblr.com`.
Example: `greentype.tumblr.com`
> * Custom hostname: Anything at all, as determined by a DNS CNAME entry.
Example: `www.davidslog.com`

Make sure you type it in exactly, and wrap it in quote marks.

Then you need to add an API key. This is what authenticates you to Tumblr, and lets you download your post data. To get an API key, first make sure you're logged into Tumblr, then go to the [OAuth registration page][oauth] on Tumblr. Click **Register Application**, and fill in the following details:

* **Application name:** Untagged post finder
* **Application description:** Finds untagged posts on a blog
* **Default callback URL:** `/`

Once you click **Register**, you'll be taken back to the previous page, and you'll see something like this:

![](/images/2013/tumblr_api_keys.png)

Copy and paste the **OAuth Consumer Key** into line 7 of the script, and remember to wrap it in quote marks.

Once that's done, you just run the Python script (if you haven't done that before, then there are plenty of helpful guides on Google), and you will shortly have a list of all your posts which don't have tags. This isn't quite a “one-click” solution to the problem, but I think it’s better than searching through your posts by hand.

{% update 2014-05-20 %}
  I ran across a [Stack Overflow](http://stackoverflow.com/q/21743112) question asking about this script. One thing I should have made clear is that this is a **Python 2** script, not Python 3. If you want to use Python 3, then the answer to that question has a version of the script compatible with Python 3.
{% endupdate %}

{% update 2014-06-13 %}
  This has been superceded by a much cleaner, turnkey solution. For most people, my new [one-page, one-click solution](http://alexwlchan.net/2014/06/untagged-tumblr-posts-redux/) should be much easier and simpler.

  You'll still need to use this method if you have a private blog, but anybody else should check out the new way.
{% endupdate %}

{% update 2015-08-02 %}
  This script is almost two years old, and it continues to get a lot of hits.
  Normally I try not to revisit old code, but since this is so popular, I've posted a slightly improved version [as a Gist](https://gist.github.com/alexwlchan/4502860fd9ff014dc178).
{% endupdate %}

[api]: https://www.tumblr.com/docs/en/api/v2#hostname
[oauth]: http://www.tumblr.com/oauth/apps
