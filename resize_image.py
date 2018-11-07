#!/usr/bin/env python
# -*- encoding: utf-8

import itertools
import os
import sys

from PIL import Image


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
        print((width, height))

        im2 = im.resize((width, height))
        im2.save(
            os.path.splitext(path)[0] + "_%dx.jpg" % i
        )
