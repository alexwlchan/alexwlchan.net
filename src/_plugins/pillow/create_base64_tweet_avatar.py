#!/usr/bin/env python3
"""
Get a base64-encoded representation of an image.

This takes two arguments: the path to the image and the target width.
It prints the base64 encoded image data.

This is meant for use with avatars in embedded tweets.
"""

import base64
import io
import sys

from PIL import Image


if __name__ == '__main__':
    path = sys.argv[1]
    width = int(sys.argv[2])

    im = Image.open(path)
    assert im.width == im.height
    resized_im = im.resize((width, width))

    output = io.BytesIO()
    resized_im.save(output, format=im.format)
    data = output.getvalue()
    b64_data = base64.b64encode(data).decode("ascii")

    if im.format == 'PNG':
        print(f"data:image/png;base64,#{b64_data}", end="")
    elif im.format == 'JPEG':
        print(f"data:image/jpeg;base64,#{b64_data}", end="")
    else:
        raise ValueError(f"Unrecognised avatar extension: {path}")
