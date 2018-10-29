#!/usr/bin/env python
# -*- encoding: utf-8

import filecmp
import json
import os
import shutil
import subprocess
import sys
from xml.etree import ElementTree as ET

from flickrapi import FlickrAPI


ROOT = subprocess.check_output([
    "git", "rev-parse", "--show-toplevel"]).decode("utf8").strip()


def upload_photo(api, filename):
    title = os.path.splitext(os.path.basename(filename))[0]
    resp = api.upload(
        filename=filename,
        title=title,

        # Make the image private
        is_public=0,

        # Hide from public searches
        hidden=2,

        format='etree'
    )

    photo_id = resp.find('photoid').text

    # Set the licence as CC-BY.
    resp = api.do_flickr_call(
        "flickr.photos.licenses.setLicense",
        photo_id=photo_id,
        license_id="4"
    )
    assert ET.tostring(resp) == b'<rsp stat="ok">\n</rsp>'

    return photo_id


def flickr_dir(name):
    return os.path.join(os.environ["HOME"], ".flickr", name)


def get_user_id():
    flickr_api_creds = json.load(open(flickr_dir("api_credentials.json")))
    return flickr_api_creds["user_id"]


def get_flickr_api():
    flickr_api_creds = json.load(open(flickr_dir("api_credentials.json")))
    return FlickrAPI(
        api_key=flickr_api_creds["api_key"],
        secret=flickr_api_creds["api_secret"]
    )


def cache_sizes(api, photo_id):
    resp = api.do_flickr_call(
        "flickr.photos.getSizes",
        photo_id=photo_id
    )

    sizes = [
        dict(sz.items())
        for sz in resp.find("sizes").findall("size")
    ]

    out_path = os.path.join(get_flickr_outdir(), "photo_%s.json" % photo_id)

    with open(out_path, "w") as outfile:
        outfile.write(json.dumps(sizes))


def get_flickr_outdir():
    path = os.path.join(ROOT, "src", "_flickr")
    os.makedirs(path, exist_ok=True)
    return path


if __name__ == '__main__':
    files_to_upload = sys.argv[1:]

    if not files_to_upload:
        sys.exit(f"Usage: {__file__} [files]")

    user_id = get_user_id()
    api = get_flickr_api()
    outdir = get_flickr_outdir()

    for filename in files_to_upload:
        print(f"Uploading {filename}...")
        photo_id = upload_photo(api=api, filename=filename)

        print("  Getting sizes...")
        cache_sizes(api=api, photo_id=photo_id)

        print("  Copying asset...")
        copy_dst = os.path.join(get_flickr_outdir(), os.path.basename(filename))
        if not os.path.exists(copy_dst):
            shutil.copyfile(src=filename, dst=copy_dst)
        else:
            assert filecmp.cmp(filename, copy_dst)

        print(f"  {photo_id}")
