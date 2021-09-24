#!/usr/bin/env sh

set -o errexit
set -o nounset
set -o verbose

apk update
apk add py2-pillow py2-pip py-setuptools

pip install specktre==0.2.0

# pip is only required to install specktre, not to run it
apk del --purge py2-pip
rm -rf /var/cache/apk/*
