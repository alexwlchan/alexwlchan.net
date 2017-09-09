#!/usr/bin/env bash

set -o errexit
set -o nounset

mkdir -p _cache
docker save alexwlchan/alexwlchan.net --output _cache/alexwlchan_build.tar
docker save alexwlchan/specktre --output _cache/specktre.tar
