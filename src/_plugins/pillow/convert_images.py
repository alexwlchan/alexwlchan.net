#!/usr/bin/env python3
"""
Convert images to new image at a given size.

This takes a single argument, which is the path to a file.  Each line of
that file must be a JSON-formatted object with three keys:
``in_path``, ``out_path`` and ``width``.

Example:

    $ cat requests.json
    {"in_path": "cat.jpg", "out_path": "cat_500w.webp", "width": 500}

    $ python3 convert_images.py requests.json

"""

import concurrent.futures
import io
import json
import os
import sys

from PIL import Image
from PIL import ImageCms
import pillow_avif
import tqdm


def get_profile_description(im):
    icc_profile = im.info.get("icc_profile")

    if icc_profile is None:
        return None

    f = io.BytesIO(icc_profile)
    prf = ImageCms.ImageCmsProfile(f)
    return prf.profile.profile_description


def process_request(request):
    im = Image.open(request["in_path"])

    profile_name = get_profile_description(im)
    if profile_name is not None and profile_name not in {
        "sRGB",
        "sRGB built-in",
        "sRGB IEC61966-2.1",
        "Generic Gray Gamma 2.2 Profile",
    }:
        raise ValueError(
            f"Got image with non-sRGB profile: {request['in_path']} ({profile_name})"
        )

    # This is to work around a bug in the AVIF plugin, where opacity is
    # lost when converting a P mode image.
    # See https://github.com/bigcat88/pillow_heif/issues/235
    if (
        im.mode == "P"
        and im.info.get("transparency")
        and request["out_path"].endswith(".avif")
    ):
        im = im.convert("RGBA")

    im = im.resize(
        (
            request["target_width"],
            int(im.height * request["target_width"] / im.width),
        )
    )

    os.makedirs(os.path.dirname(request["out_path"]), exist_ok=True)

    with open(request["out_path"], "xb") as fp:
        im.save(fp)

    print(request["out_path"])


if __name__ == "__main__":
    with open(sys.argv[1]) as in_file:
        requests = [json.loads(line) for line in in_file if line.strip()]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_request, req) for req in requests}

        iterator = concurrent.futures.as_completed(futures)

        if len(futures) > 20:
            iterator = tqdm.tqdm(iterator, total=len(futures))

        for _ in iterator:
            pass
