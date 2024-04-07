#!/usr/bin/env python3

import io
import json
import pathlib
import sys

from PIL import Image
from PIL import ImageCms


def get_file_paths_under(root=".", *, suffix=""):
    """
    Generates the absolute paths to every matching file under ``root``.
    """
    root = pathlib.Path(root)

    if root.exists() and not root.is_dir():
        raise ValueError(f"Cannot find files under file: {root!r}")

    if not root.is_dir():
        raise FileNotFoundError(root)

    for dirpath, _, filenames in root.walk():
        for f in filenames:
            if f == ".DS_Store":
                continue

            p = dirpath / f

            if p.is_file() and f.lower().endswith(suffix):
                yield p


def get_profile_description(path):
    im = Image.open(path)
    icc_profile = im.info.get('icc_profile')

    if icc_profile is None:
        return None

    f = io.BytesIO(icc_profile)
    prf = ImageCms.ImageCmsProfile(f)
    return prf.profile.profile_description


if __name__ == '__main__':
    result = {
        str(p): get_profile_description(p)
        for p in get_file_paths_under(sys.argv[1])
    }
    print(json.dumps(result))
