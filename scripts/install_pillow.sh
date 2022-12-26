#!/usr/bin/env sh

set -o errexit
set -o nounset
set -o verbose

apk update
apk add g++ libavif-dev python3 python3-dev py3-pip py3-pillow
pip3 install pillow-avif-plugin==1.3.1 tqdm==4.64.1

# # These packages are only required for installation, not for running Pillow
apk del py3-pip
rm -rf /var/cache/apk/*