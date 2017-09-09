#!/usr/bin/env bash

set -o errexit
set -o nounset

pip3 install -r _tests/requirements.txt

.travis/unfreeze_docker_images.sh
