---
layout: post
date: 2020-04-12 14:27:01 +0000
title: A snippet for downloading files with Python
category: Python
tags: python
---

Back in February, I wrote about the [new storage service][storage] I've been helping to build at Wellcome.
Since then, we've migrated almost everything from the old system into the new service.
Before we can decommission the old system, we need to check that every one of the 42&nbsp;million files it was storing was either been migrated successfully, or we're happy to delete it (for example, material that was ingested as part of a system test).

[storage]: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e

We've verified about 99.5% of the files so far, and it's just the remaining half a percent that need to be checked.
The best way to process the last few files is to download them and do some manual inspection, to understand whether a given set of files should be saved or deleted.
I don't want to download the files by hand, so I've written some Python scripts to automate the process.

The files are available over HTTP from a server that's in the office -- but of course, we're not working from the office right now.
I have to download files to a laptop at home, using a VPN.
The server is quite underpowered; timeouts or dropped connections aren't uncommon.
If I get all the bytes, they're correct, but the download often fails midway.

This is a common problem I have to solve in a lot of my scripts:

*   I'm downloading files over HTTP
*   The server or connection is unreliable, and downloads might fail in a non-deterministic way
*   The content of each URL is [idempotent]: if I request the same URL more than once, I always get the same bytes

[idempotent]: https://en.wikipedia.org/wiki/Idempotence

Because I do this so often, I've tidied up and extracted the function I use to download files.
The next time I have to do this, I won't have to write it from scratch:

```python
import os
import sys
import uuid

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
import urllib3.exceptions


@retry(
    retry=(
        retry_if_exception_type(httpx.HTTPError) |
        retry_if_exception_type(urllib3.exceptions.HTTPError)
    ),
    stop=stop_after_attempt(10),
    wait=wait_fixed(60),
)
def download_file(*, url, path, client=None):
    """
    Atomically download a file from ``url`` to ``path``.

    If ``path`` already exists, the file will not be downloaded again.
    This means that different URLs should be saved to different paths.

    This function is meant to be used in cases where the contents of ``url``
    is immutable -- calling it more than once should always return the same bytes.

    Returns the download path.

    """
    # If the URL has already been downloaded, we can skip downloading it again.
    if os.path.exists(path):
        return path

    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    if client is None:
        client = httpx.Client()

    try:
        with client.stream("GET", url) as resp:
            resp.raise_for_status()

            # Download to a temporary path first.  That way, we only get
            # something at the destination path if the download is successful.
            #
            # We download to a path in the same directory so we can do an
            # atomic ``os.rename()`` later -- atomic renames don't work
            # across filesystem boundaries.
            tmp_path = f"{path}.{uuid.uuid4()}.tmp"

            with open(tmp_path, "wb") as out_file:
                for chunk in resp.iter_raw():
                    out_file.write(chunk)

    # If something goes wrong, it will probably be retried by tenacity.
    # Log the exception in case a programming bug has been introduced in
    # the ``try`` block or there's a persistent error.
    except Exception as exc:
        print(exc, file=sys.stderr)
        raise

    os.rename(tmp_path, path)
    return path
```

This is more involved than just using [`urlretrieve`][urlretrieve] in the standard library, but gets me several improvements:

[urlretrieve]: https://docs.python.org/3/library/urllib.request.html#urllib.request.urlretrieve

*   Because I know URLs are idempotent, I can skip downloading a URL if I've saved it already.
    (Assuming I have a 1:1 mapping between URLs and download paths.)

    This saves bandwidth and server load if I run a script multiple times.
    If I have a long-running script, I can interrupt it midway through and not have to re-download everything.

    To make this work, I've had to implement [atomic] downloads -- download to a temporary path first, then an atomic rename to the final path.
    If there's a file at the final path, then it's the complete file -- it will never be something that's only partially downloaded.

*   I'm often dealing with servers that need authentication or special headers.
    I find it easier to configure that sort of thing with [an httpx `Client`][httpx] than in urllib.

*   Adding [tenacity] means downloads will automatically get retried if they fail, rather than relying on me to restart the whole script.
    I tweak the exact retry behaviour depending on the flakiness I'm dealing with -- an exponential backoff is more common, but the server I'm currently using tends to need a fixed minute-long wait before it can serve another request.

[atomic]: https://en.wikipedia.org/wiki/Atomicity_(database_systems)
[httpx]: https://www.python-httpx.org/advanced/
[tenacity]: https://tenacity.readthedocs.io/en/latest/

I don't have any tests for this right now, but I've tested in the past, and I've variants of this code to download thousands of files successfully.

Next time I need to write a script that needs to download files, I'll copy-paste this code into the project.
It's not the most complicated thing in the world, but it's one less thing I'll have to write from fresh next time.
If this would be useful to you, feel free to copy it into your own code as well.
