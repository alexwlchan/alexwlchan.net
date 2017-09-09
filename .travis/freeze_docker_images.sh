#!/usr/bin/env bash

set -o errexit
set -o nounset

mkdir -p .cache
docker save alexwlchan/alexwlchan.net > .cache/alexwlchan_build.tar
docker save alexwlchan/specktre > .cache/specktre.tar
