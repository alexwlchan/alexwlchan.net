#!/usr/bin/env python3
"""
Get the information about an images.

This takes a path to an image, prints the output as JSON.

Example:

    $ python3 convert_image.py cat.jpg
    {"width": 400, "height": 300, "format": "JPEG"}

"""

import json
import os
import sys

from PIL import Image


def get_info(path):
    im = Image.open(path)
    return {
        "width": im.width,
        "height": im.height,
        "format": im.format,
        "mtime": int(os.path.getmtime(path)),
    }


if __name__ == "__main__":
    print(json.dumps(get_info(sys.argv[1])))
