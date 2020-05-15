---
layout: post
title: Downloading the AO3 fics that I've saved in Pinboard
summary: A script that downloads the nicely formatted AO3 downloads for everything I've saved in Pinboard.
category: Python
---

A couple of days ago, I tweeted about one of my scripts:

{% tweet https://twitter.com/alexwlchan/status/1260225157672697858 %}

I got a fair amount of interest, so in this post I'm going to walk through the script and how it works.
If you'd rather just get the code, you can [skip to the end](#the-final-script).

Pinboard (<https://pinboard.in/>) is a bookmarking site that I've used for many years.
You can use it to save links so you can find them later, and [if you pay extra for an archival account](https://pinboard.in/tour/#archive), Pinboard will crawl and save a copy of every bookmark in your account.
If the original site breaks or changes, you can still see the archived copy.

AO3 (the Archive of Our Own, <https://archiveofourown.org/>) is a site that hosts fanworks, primarily fanfiction.
I save a lot of fic from AO3 in my Pinboard account, and I know I'm not the only one -- a lot of other fannish folk use Pinboard to save bookmarks, in part because Maciej (who runs Pinboard) has made concerted efforts [to win them over](https://idlewords.com/talks/fan_is_a_tool_using_animal.htm).

If you save an AO3 fic to Pinboard, and let the archival account keep an archived copy, it saves the fic as it appears on the web -- embedded in a larger page, including navigation and CSS.
As a backup, that's good, but better would be to use the exports that AO3 provides:

<img src="/images/2020/ao3_download_button.png" alt="A button labelled 'Download', highlighted in red. Below it are several other buttons labelled AZW3, EPUB, MOBI, PDF and HTML." style="width: 389px;">

These allow you to download a fic without all the page ornaments.
It means you can read fic offline or with something like an e-reader; they also serve as much more usable backup copies.

Downloading the exports for every fic you've saved would be very tedious and manually; scripting makes it much faster.

I do most of my scripting in Python, and that's what I'm going to do here.



## Getting a copy of my Pinboard bookmarks




## The final script
