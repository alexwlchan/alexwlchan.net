#!/usr/bin/env python3
"""
Convert an image to a new image at a given size.

This takes one or more arguments, each of which must be a JSON-formatted
object with three keys: ``in_path``, ``out_path`` and ``width``.

Example:

    $ python3 convert_image.py '{"in_path": "cat.jpg", "out_path": "cat_500w.webp", "width": 500}'

"""

import json
import sys

from PIL import Image


if __name__ == "__main__":
    try:
        resize_request = json.loads(sys.argv[1])
    except IndexError:
        sys.exit(f"Usage: {__file__} <RESIZE_REQUEST>")

    for argv in sys.argv[1:]:
        request = json.loads(argv)

        im = Image.open(request["in_path"])
        im = im.resize(
            (
                request["target_width"],
                im.height * request["target_width"] / im.width,
            )
        )

        with open(request["out_path"], "x") as fp:
            im.save(fp)

        print(request["out_path"])
