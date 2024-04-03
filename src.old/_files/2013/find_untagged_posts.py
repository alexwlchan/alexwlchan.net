#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
find_untagged_posts.py
~~~~~~~~~~~~~~~~~~~~~~

This is a Python script for finding untagged posts on Tumblr.  You can
download it from my website: http://alexwlchan.net/2013/08/untagged-tumblr-posts/
which also has usage and configuration instructions.

Copyright 2013 Alex Chan.
MIT License.
"""

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