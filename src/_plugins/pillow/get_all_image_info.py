#!/usr/bin/env python3
"""
Get the information about every image it can find.
"""

import json
import pathlib

from get_image_info import get_info


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

            if f.endswith((".svg", ".mov")):
                continue

            p = dirpath / f

            if p.is_file() and f.lower().endswith(suffix):
                yield p


if __name__ == "__main__":
    result = {}

    for p in get_file_paths_under("src/_images"):
        result[str(p)] = get_info(p)

    print(json.dumps(result))
