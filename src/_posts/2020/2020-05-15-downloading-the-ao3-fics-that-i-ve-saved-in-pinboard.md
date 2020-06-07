---
layout: post
date: 2020-05-15 18:59:26 +0000
title: Downloading the AO3 fics that I've saved in Pinboard
summary: A script that downloads the nicely formatted AO3 downloads for everything I've saved in Pinboard.
category: Python
tags: python pinboard
---

A couple of days ago, I tweeted about one of my scripts:

{% tweet https://twitter.com/alexwlchan/status/1260225157672697858 %}

The tweet got a fair amount of interest, so in this post I'm going to share that script.

Pinboard (<https://pinboard.in/>) is a bookmarking service that I've used for many years.
You can use it to save links so you can find them later, and [if you pay extra for an archival account](https://pinboard.in/tour/#archive), Pinboard will crawl and save a copy of every bookmark in your account.
If the original site breaks or changes, you can still see the archived copy.

AO3 (the Archive of Our Own, <https://archiveofourown.org/>) is a site that hosts fanworks, primarily fanfiction.
I save a lot of fic from AO3 in my Pinboard account, and I know I'm not the only one -- a lot of other fannish folk use Pinboard to save bookmarks, in part because Maciej (who runs Pinboard) has made concerted efforts [to win them over](https://idlewords.com/talks/fan_is_a_tool_using_animal.htm).

If you save an AO3 fic to Pinboard, and let the archival account keep an archived copy, it saves the fic as it appears on the web -- embedded in a larger page, including navigation and CSS.
As a backup, that's good, but better would be to use the exports that AO3 provides:

<img src="/images/2020/ao3_download_button.png" alt="A button labelled 'Download', highlighted in red. Below it are several other buttons labelled AZW3, EPUB, MOBI, PDF and HTML." style="width: 389px;">

These allow you to download a fic without all the page ornaments -- just the text, nothing more.
It means you can read fic offline or with a device like an e-reader; these exports also serve as much more usable backup copies.

Downloading the exports for every fic you've saved would be very tedious and manual; scripting makes it much faster.

I do most of my scripting in Python, and that's what I used here.
Specifically, I'm using the [Pinboard API](https://pinboard.in/api) to get a list of my bookmarks, and then going through to find the AO3 links and download all the nicely-formatted exports.

To use it, [download the script](/files/2020/download_ao3_bookmarks_from_pinboard.py) or copy/paste the code below to a file.
Run the file with Python in a terminal (for example, `python download_bookmarks.py`), enter the API token from [your settings page](https://pinboard.in/settings/password), and watch as a folder fills up with downloaded fic.

If you have issues running this code, get in touch [on Twitter](https://twitter.com/alexwlchan).

{% update 2020-05-17 %}
Thanks for all the kind comments!
It's really nice to know that people find my code useful.

I've made a couple of changes based on feedback from Twitter and Dreamwidth:

-   You can choose to download everything, or just bookmarks with a specific tag.
-   You can choose to download every available format, or just a single format if that's all you need.
-   The script gives a better error if you pass it something that doesn't look like a Pinboard API token.
-   The script shouldn't crash if it tries to download a fic that has since been deleted from AO3.

{% endupdate %}

{% details %}
<summary>download_ao3_bookmarks_from_pinboard.py</summary>
{% inline_code python _files/2020/download_ao3_bookmarks_from_pinboard.py %}
{% enddetails %}
