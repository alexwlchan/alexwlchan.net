#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o verbose

echo "*** Freezing Docker images"
mkdir -p _cache
docker save alexwlchan/alexwlchan.net --output _cache/alexwlchan_build.tar
docker save alexwlchan/specktre --output _cache/specktre.tar

ls _cache
set +o verbose
