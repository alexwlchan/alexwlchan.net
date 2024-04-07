#!/usr/bin/env python3
"""
Create an ico image.

Takes three arguments: a path to a 16×16 PNG, a path to a 32×32 PNG, and
the path where the ICO image should be written.
"""

import os
import sys

from PIL import Image


if __name__ == "__main__":
    _, png16_path, png32_path, ico_path = sys.argv

    im16 = Image.open(png16_path)
    im32 = Image.open(png32_path)

    im16.save(ico_path, append_images=[im32])

    assert os.path.exists(ico_path)
