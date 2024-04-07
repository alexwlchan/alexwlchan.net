#!/usr/bin/env python3
"""
Convert an image to a new image at a given size.

This takes one or more arguments, each of which must be a JSON-formatted
object with three keys: ``in_path``, ``out_path`` and ``width``.

Example:

    $ python3 convert_image.py '{"in_path": "cat.jpg", "out_path": "cat_500w.webp", "width": 500}'

"""

import io
import json
import sys

from PIL import Image
from PIL import ImageCms
import pillow_avif


def get_profile_description(im):
    icc_profile = im.info.get("icc_profile")

    if icc_profile is None:
        return None

    f = io.BytesIO(icc_profile)
    prf = ImageCms.ImageCmsProfile(f)
    return prf.profile.profile_description


if __name__ == "__main__":
    for argv in sys.argv[1:]:
        request = json.loads(argv)

        im = Image.open(request["in_path"])

        profile_name = get_profile_description(im)
        if profile_name is not None and profile_name not in {
            "sRGB",
            "sRGB built-in",
            "sRGB IEC61966-2.1",
            "Generic Gray Gamma 2.2 Profile",
        }:
            raise ValueError("Got image with non-sRGB profile: {request['in_path']}")

        im = im.resize(
            (
                request["target_width"],
                int(im.height * request["target_width"] / im.width),
            )
        )

        with open(request["out_path"], "xb") as fp:
            im.save(fp)

        print(request["out_path"])
