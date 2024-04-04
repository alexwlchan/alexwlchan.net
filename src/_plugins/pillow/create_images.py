#!/usr/bin/env python3

import json

from PIL import Image


if __name__ == "__main__":
    for line in open('.missing_images.json'):
        resize_request = json.loads(line)

        im = Image.open(resize_request['source_path'])
        im = im.resize((resize_request['width'], resize_request['height']))
        im.save(resize_request['out_path'])

        print(resize_request)
