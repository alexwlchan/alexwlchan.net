#!/usr/bin/env bash

set -o errexit
set -o nounset

mkdir -p .cache
docker export alexwlchan/alexwlchan.net > .cache/alexwlchan_build.tar
docker export alexwlchan/specktre > .cache/specktre.tar
