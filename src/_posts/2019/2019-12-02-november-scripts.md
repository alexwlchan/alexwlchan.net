---
layout: post
date: 2019-12-02 23:21:41 +0000
title: "November 2019 scripts: downloading podcasts, retrying flaky errors, Azure and AWS"
category: Python
theme:
  minipost: true
tags: python aws
---

I do a lot of automation, and I write plenty of scripts.
Some of those get written up here as blog posts, but not all of them.
Writing a post takes time and energy, and I write code faster than I write prose.

If you're reading this blog, there's a good chance you're interested in scripting and automation, and might want to see some of those unwritten-about scripts.
I'm going to start linking to some of the scripts that don't get a full writeup.
They'll have code comments and a README file, but not a complete walkthrough.

Here's some stuff I wrote in November:

*   [A script to save the audio files for every podcast I've listened to in Overcast][overcast] (🐍).

    Sometimes I want to go back and listen to a podcast I heard a long time ago, but links rot, websites break, and episodes go offline.
    This scripts parses an OPML export from Overcast, gets the links for the MP3s of everything I've ever listened to, and downloads a local archive of my podcasts.

*   [Handling HTTP 429 errors with tenacity][tenacity_429] (🐍).

    [Tenacity] is a Python library for retrying things -- flaky connections, intermittent errors, and so on.
    I was adding retrying support to a Twitter API client, and Twitter's API does rate-limiting by returning [HTTP 429s][http_429].
    This an example of some custom Tenacity helpers for dealing with 429 errors.

*   [Getting AWS credentials with Azure AD][azure] (🦀)

    I'm dipping my toes into writing Rust again, and quite enjoying it.
    This is a very specific-to-me tool for getting AWS credentials for local development -- at work, we log in to AWS using Azure AD, and we have short-lived credentials.
    It raids the Safari cookie store (oops), then pretends to be logged in so it can get credentials using SAML.

    Not useful directly, but you might want to raid bits of the code.

Meanwhile, in the bucket of "looks useful", I've just discovered the [inquirer library][inquirer] (🐍).
It's a way to create interactive command line interfaces in Python -- choose from a list of options, multiple choice, ask questions with a text input, and so on.
I haven't tried it much yet, but what little I have tried looks good.

[overcast]: https://github.com/alexwlchan/overcast-downloader
[tenacity_429]: https://github.com/alexwlchan/handling-http-429-with-tenacity
[Tenacity]: https://tenacity.readthedocs.io/en/latest/
[azure]: https://github.com/alexwlchan/azure-aws-credentials
[http_429]: https://tools.ietf.org/html/rfc6585
[inquirer]: https://pypi.org/project/inquirer/
