#!/usr/bin/env python
# -*- encoding: utf-8

import os
import subprocess

for root, _, filenames in os.walk("src"):
    for f in sorted(filenames):
        if not f.endswith(("_3x.jpg", "_4x.jpg")):
            continue

        if f.endswith("_3x.jpg") and os.path.exists(os.path.join(root, f.replace("_3x", "_4x"))):
            continue

        if f.endswith("_4x.jpg"):
            subprocess.check_call([
                "convert",
                "-resize", "%dx" % (950 * 3),
                f, f.replace("_4x", "_3x")
            ], cwd=root)
            subprocess.check_call([
                "convert",
                "-resize", "%dx" % (950 * 2),
                f, f.replace("_4x", "_2x")
            ], cwd=root)
            subprocess.check_call([
                "convert",
                "-resize", "%dx" % 950,
                f, f.replace("_4x", "_1x")
            ], cwd=root)
        else:
            subprocess.check_call([
                "convert",
                "-resize", "%dx" % (950 * 2),
                f, f.replace("_3x", "_2x")
            ], cwd=root)
            subprocess.check_call([
                "convert",
                "-resize", "%dx" % 950,
                f, f.replace("_3x", "_1x")
            ], cwd=root)

        print(f)
