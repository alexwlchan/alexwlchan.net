#!/usr/bin/env python3

import json
import sys

from PIL import Image


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <PATH>")

    im = Image.open(path)

    info = {"path": path, "width": im.width, "height": im.height, "format": im.format}

    print(json.dumps(info))
