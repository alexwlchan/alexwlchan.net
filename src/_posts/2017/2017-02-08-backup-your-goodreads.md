---
date: 2017-02-08 20:41:00 +0000
layout: post
link: https://github.com/alexwlchan/backup-goodreads
slug: backup-your-goodreads
tags: python goodreads
title: A script for backing up your Goodreads reviews
---

Last year, I started using Goodreads to track my reading.
(I'm [alexwlchan](https://goodreads.com/alexwlchan) if you want to follow me.)
In the past, I've had a couple of hand-rolled systems for recording my books, but maintaining them often became a distraction from actually reading!

Using Goodreads is quite a bit simpler, but it means my book data is stored on somebody else's servers.
What if Goodreads goes away?
I don't want to lose that data, particularly because I'm trying to be better about writing some notes after I finish a book.

There is an [export function](https://www.goodreads.com/help/show/5-how-do-i-import-or-export-my-books) on Goodreads, but it has to be invoked by hand.
I prefer to have backup tools that can be run automatically: I can set them to run on a schedule, and I know my data is safe.
This tends to be a script or a cron job.

That's exactly what I've done for Goodreads: I've written a Python script that uses the Goodreads API to grab the same information as provided by the builtin export.
I have this configured to run once a day, and now I have daily backups of my Goodreads data.
You can find the script and installation instructions [on GitHub][gh].

This was a fun opportunity to play with the [ElementTree module][et] (normally I work with JSON), and also a reminder that the lack of `yield from` has become my most disliked feature in Python 2.

[gh]: https://github.com/alexwlchan/backup-goodreads/
[et]: https://docs.python.org/3.5/library/xml.etree.elementtree.html
