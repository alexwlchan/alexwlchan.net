#!/usr/bin/env python3

import os

import os

def get_file_paths_under(root=".", *, suffix=""):
    """Generates the paths to every file under ``root``."""
    if not os.path.isdir(root):
        raise ValueError(f"Cannot find files under non-existent directory: {root!r}")

    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if os.path.isfile(os.path.join(dirpath, f)) and f.lower().endswith(suffix):
                yield os.path.join(dirpath, f)

for path in get_file_paths_under(".", suffix=".avif"):
    os.unlink(path)
