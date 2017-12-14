---
layout: post
date: 2015-12-10 08:15:00 +0000
link: http://leancrew.com/all-this/2015/11/simpler-syndication/
tags: python
title: Simpler syndication, by Dr. Drang
---

A fortnight ago, Dr. Drang wrote about his new RSS service: a Python script that polls his subscriptions once every five minutes, and renders the output as a static HTML page.
Reading it was one of those "doh" moments, an idea so simple that I'm annoyed I hadn't thought of it myself.

I'm a very light RSS user – I only subscribe to a handful of feeds, and I don't need any of the advanced syncing stuff.  (Indeed, managing unread status is almost more work than it's worth for me.)  A Python script that I can modify as much as I want is a much better fit for my needs.

The nice thing about a Python script is that it gives me arbitrary control over the posts.  Most RSS services already support basic keyword filtering to hide posts, but with a script I can write whatever rules I like.  And I can modify or extend post content before it gets displayed – for example, on sites that only offer a truncated RSS feed.

(I'm probably the only person who cares about this level of tweaking, but I enjoy fixing small distractions in my RSS reader.)

I also made some cosmetic tweaks, mostly reusing the templates and CSS from this blog (albeit with a different colour scheme).  This includes dating every post, and better support for linkposts.

This is what the revised version looks like on my Mac:

![](/images/2015/drangreader.png)

and on my iPhone:

![](/images/2015/drangreader-iphone.png)

My updated code is [in a Gist](https://gist.github.com/alexwlchan/01cec115a6f51d35ab26).
