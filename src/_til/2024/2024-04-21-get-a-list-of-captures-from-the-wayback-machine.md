---
layout: til
date: 2024-04-21 10:11:02 +0100
date_updated: 2024-11-26 07:26:14 +0000
title: How to get a list of captures from the Wayback Machine
summary: |
  Use the CDX Server API to get a list of captures for a particular URL.
tags:
  - wayback machine
---
As part of my [daily screenshots project][daily_screenshots], I wanted to get a list of all the versions of my sites that are saved in the Wayback Machine.

I started by copy/pasting URLs out of the Wayback Machine's web interface, but that's very slow and cumbersome even for a small site.
Surely there's a better way?

I looked in Google, and several pages pointed me to the [CDX Server API][api].
(It's named CDX because that's the name of [the file format][cdx] used in the index.)
This is precisely the API I wanted -- you give it a URL, and it returns a list of captures.

I wrapped this API in a Python function for ease of use:

```python
import datetime

import httpx


def get_wayback_machine_captures(url: str):
    """
    Get a list of all the captures for a given URL in the Wayback Machine.
    """
    resp = httpx.get(
        "http://web.archive.org/cdx/search/cdx",
        params={"url": url, "output": "json"},
        timeout=30
    )
    resp.raise_for_status()

    # What if we don't get any results?
    if resp.json() == []:
        return []

    fields, *remainder = resp.json()

    for row in remainder:
        data = dict(zip(fields, row))

        data["length"] = int(data["length"])

        # The format used for Wayback captures is yyyyMMddhhmmss
        # e.g. 20200814072506
        data["time"] = datetime.datetime.strptime(data["timestamp"], "%Y%m%d%H%M%S")

        # The capture URL is of the format:
        # https://web.archive.org/web/{timestamp}/{original}
        #
        # TODO: What does the `if_` parameter mean?
        data["raw_url"] = f"https://web.archive.org/web/{data['timestamp']}if_/{data['original']}"
        data["web_url"] = f"https://web.archive.org/web/{data['timestamp']}/{data['original']}"

        yield data


for capture in get_wayback_machine_captures(url="alexwlchan.net"):
    print(capture)
```

You can use wildcards in the `url` parameter, e.g. `alexwlchan.net` just returns captures of the homepage, whereas `alexwlchan.net*` returns captures of any page.

Here's what a single capture looks like:

```python
{'digest': '6UITANF4TVK33JJ55VT4CETNR5CLBWPN',
 'length': 5324,
 'mimetype': 'text/html',
 'original': 'http://www.alexwlchan.net:80/',
 'statuscode': '200',
 'time': datetime.datetime(2013, 4, 9, 4, 38, 52),
 'timestamp': '20130409043852',
 'urlkey': 'net,alexwlchan)/',
 'raw_url': 'https://web.archive.org/web/20130409043852if_/http://www.alexwlchan.net:80/',
 'web_url': 'https://web.archive.org/web/20130409043852/http://www.alexwlchan.net:80/',
}
```

This is only based on the "Basic Usage" section of the API.
There are things like pagination in the "Advanced Usage", which I should read more carefully if I was using this for more than a one-off.

[daily_screenshots]: https://github.com/alexwlchan/daily-screenshots
[api]: https://archive.org/developers/wayback-cdx-server.html
[cdx]: https://archive.org/web/researcher/cdx_file_format.php
