#!/usr/bin/env python3

import os
import json

from PIL import Image
import pillow_avif


if __name__ == "__main__":
    for line in open(".missing_images.json"):
        resize_request = json.loads(line)

        im = Image.open(resize_request["source_path"])

        width = min([im.width, resize_request["width"]])
        height = int(im.height * width / im.width)

        im = im.resize((width, height))

        os.makedirs(os.path.dirname(resize_request["out_path"]), exist_ok=True)

        im.save(resize_request["out_path"])

        print(resize_request)
