---
layout: post
title: Downloading the AO3 fics that I've saved in Pinboard
summary: A script that downloads the nicely formatted AO3 downloads for everything I've saved in Pinboard.
category: Python
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

```python
#!/usr/bin/env python
"""
Download all the fic you've saved in Pinboard.

This saves the ebook, PDF and HTML copies available through the "Download" button.

"""

from __future__ import print_function

import cgi
import errno
import getpass
import json
import os
import re
import sys

try:
    from urllib.error import HTTPError
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
    from urllib2 import HTTPError


def get_bookmarks(api_token):
    """
    Download your Pinboard bookmarks using the API.
    https://pinboard.in/api#posts_all

    Get an API token from https://pinboard.in/settings/password

    """
    local_filename, _ = urlretrieve(
        "https://api.pinboard.in/v1/posts/all?format=json&auth_token=%s" % api_token
    )

    return json.load(open(local_filename))


def get_ao3_identifiers(bookmarks):
    """
    Given the output from Pinboard's /posts/all API, return all the unique AO3
    identifiers.  This is the numeric ID after /works.

    e.g. The ID in https://archiveofourown.org/works/1160745 is 1160745
    """
    saved_urls = [bk["href"] for bk in bookmarks]

    AO3_LINK_RE = re.compile(
        r"^https?://archiveofourown\.org/works/(?P<work_id>\d+)"
    )

    ao3_identifiers = set()

    for saved_bookmark in bookmarks:
        url = saved_bookmark["href"]
        match = AO3_LINK_RE.match(url)

        if match is None:
            continue

        ao3_identifiers.add(match.group("work_id"))

    return ao3_identifiers


def mkdir_p(path):
    """
    Create a directory if it doesn't already exist.
    """
    # https://stackoverflow.com/a/600612/1558022
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def download_work_exports(ao3_id):
    """
    Download all the exports for a given work.
    """
    # AO3 returns the original filename, including the fic title, in the
    # Content-Disposition header.
    try:
        _, headers = urlretrieve(
            "https://www.archiveofourown.org/downloads/%s/a.azw3" % ao3_id
        )
    except HTTPError as err:
        print(
            "Error downloading https://www.archiveofourown.org/downloads/%s/a.azw3: %s"
            % (ao3_id, err)
        )
        return

    content_disposition_header = headers["Content-Disposition"]
    _, params = cgi.parse_header(content_disposition_header)
    title = params["filename"][:-len(".azw3")]

    print("Downloading %s (%s)" % (title, ao3_id))

    dirname = os.path.join("ao3", "%s (%s)" % (title, ao3_id))
    mkdir_p(dirname)

    # Download every available export for this fic.
    for extension in ["azw3", "epub", "mobi", "pdf", "html"]:
        out_path = os.path.join(dirname, "%s.%s" % (title, extension))

        if os.path.exists(out_path):
            continue

        urlretrieve(
            "https://www.archiveofourown.org/downloads/%s/a.%s" % (ao3_id, extension),
            filename=out_path
        )


if __name__ == "__main__":
    api_token = getpass.getpass(
        "What is your Pinboard API token? "
        "Get it from https://pinboard.in/settings/password\n> "
    )

    bookmarks = get_bookmarks(api_token=api_token)

    ao3_identifiers = get_ao3_identifiers(bookmarks=bookmarks)

    for ao3_id in sorted(ao3_identifiers):
        download_work_exports(ao3_id=ao3_id)
```
