#!/usr/bin/env python3

import base64
import io
import sys

from PIL import Image


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <PATH>")

    im = Image.open(path)
    resized_im = im.resize((108, 108))  # 108 = 36 * 3

    output = io.BytesIO()
    resized_im.save(output, format=im.format)

    thumbnail_data = base64.b64encode(output.getvalue()).decode("ascii")

    if im.format == "JPEG":
        print(f"data:image/jpeg;base64,{thumbnail_data}")
    elif im.format == "PNG":
        print(f"data:image/png;base64,{thumbnail_data}")
    else:
        raise ValueError(f"Unrecognised image format: {im.format}")
