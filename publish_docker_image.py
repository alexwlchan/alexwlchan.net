#!/usr/bin/env python
# -*- encoding: utf-8

import os
import subprocess


if __name__ == "__main__":
    image_name = os.environ["DOCKER_IMAGE_NAME"]
    old_version = int(os.environ["DOCKER_IMAGE_VERSION"])
    new_version = image_version + 1

    existing_makefile = open("Makefile").read()

    image_tag = image_name + ":" + str(new_version)
    subprocess.check_call(["docker", "build", "--tag", image_tag, "."])

    subprocess.check_call(["docker", "push", image_tag])

    new_makefile = existing_makefile.replace(
        "DOCKER_IMAGE_VERSION = %d" % old_version,
        "DOCKER_IMAGE_VERSION = %d" % new_version
    )
    open("Makefile", "w").write(new_makefile)
