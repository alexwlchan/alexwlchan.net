#!/usr/bin/env python
# -*- encoding: utf-8

import datetime as dt
import itertools
import os
import subprocess
import sys

from PIL import Image


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=SCRIPT_DIR).strip().decode("utf8")


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit("Usage: %s <PATH>" % __file__)

    im = Image.open(path)

    for i in itertools.count(start=1):
        if im.width < i * 950:
            break

        width = i * 950
        height = int(float(width) / im.width * im.height)

        im2 = im.resize((width, height))
        image_dir = os.path.join(
            SCRIPT_DIR, "src", "_images", dt.datetime.now().strftime("%Y")
        )
        os.makedirs(image_dir, exist_ok=True)
        out_path = os.path.join(
            image_dir, os.path.basename(os.path.splitext(path)[0]) + "_%dx.jpg" % i
        )
        im2.save(out_path)
        subprocess.check_call(["git", "add", out_path], cwd=ROOT)

    print(os.path.basename(os.path.splitext(path)[0]))
    print("Up to %dx" % (i - 1))
