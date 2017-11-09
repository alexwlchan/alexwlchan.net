#!/usr/bin/env sh

set -o errexit
set -o nounset

# Any specktre assets are compiled locally and checked in before they're
# sent to CI, so CI never needs to install these pieces.
if [[ "${CI:-false}" == "true" ]]
then
    echo "*** Running in CI, so skipping installing specktre"
    exit 0
fi

apk update
apk add python py2-pillow py2-pip

pip install Pillow==4.1.0 specktre==0.2.0

# pip is only required to install specktre, not to run it
apk del --purge py2-pip
rm -rf /var/cache/apk/*
