#!/usr/bin/env sh

set -o errexit
set -o nounset

apk update
apk add python py2-pillow py2-pip

pip install Pillow==4.1.0 specktre==0.2.0

# pip is only required to install specktre, not to run it
apk del --purge py2-pip
rm -rf /var/cache/apk/*
