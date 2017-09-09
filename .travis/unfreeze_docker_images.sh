#!/usr/bin/env bash

set -o errexit
set -o nounset

if [[ -f .cache/alexwlchan_build.tar ]]
then
  echo "Cached Docker exist; reloading from cache"
  docker load .cache/alexwlchan_build.tar
  docker load .cache/specktre.tar
fi
