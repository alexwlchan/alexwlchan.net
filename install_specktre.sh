#!/usr/bin/env sh

set -o errexit
set -o nounset

apk update
apk add build-base jpeg-dev optipng python python-dev py2-pip zlib-dev

pip install Pillow
pip install specktre==0.2.0

# These dependencies are only required to install Pillow, not to actually
# run it.
apk del --purge build-base python-dev
rm -rf /var/cache/apk/*
