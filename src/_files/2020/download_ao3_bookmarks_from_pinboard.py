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
