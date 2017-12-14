---
layout: post
date: 2017-01-14 16:09:00 +0000
link: https://github.com/alexwlchan/ao3
summary: AO3 doesn't have an official API for scraping data - but with a bit of Python,
  it might not be necessary.
tags: python fandom
title: A Python interface to AO3
---

In [my last post][previous], I talked about some work I'd been doing to scrape data from AO3 using Python.
I haven't made any more progress, but I've tidied up what I had and posted it to GitHub.

Currently this gives you a way to get metadata about works (word count, title, author, that sort of thing), along with your complete reading history.
This latter is particularly interesting because it allows you to get a complete list of works where you've left kudos.

Instructions are in the README, and you can install it from PyPI (`pip install ao3`).

I'm not actively working on this (I have what I need for now), but this code might be useful for somebody else.
Enjoy!

[previous]: /2017/01/experiments-with-ao3-and-python/
