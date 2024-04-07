#!/usr/bin/env python3
"""
Get the information about one or more images.

This takes one argument, which is a JSON-formatted list of image paths.
It prints a JSON object whose keys are paths and values are image info.

Example:

    $ python3 convert_image.py '["cat.jpg", "dog.png"]'
    {
        "cat.jpg": {"width": 400, "height": 300, "format": "JPEG"},
        "dog.png": {"width": 1600, "height": 900, "format": "PNG"}
    }

"""

import json
import sys

from PIL import Image


def get_info(path):
    im = Image.open(path)
    return {"width": im.width, "height": im.height, "format": im.format}


if __name__ == "__main__":
    result = {path: get_info(path) for path in json.loads(sys.argv[1])}

    print(json.dumps(result))
