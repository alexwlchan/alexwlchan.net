#!/usr/bin/env bash

set -o errexit
set -o nounset

if [[ -d _cache ]]
then
  ls _cache
fi

if [[ -f _cache/alexwlchan_build.tar ]]
then
  echo "*** Cached Docker images exist; reloading from cache"
  docker load < _cache/alexwlchan_build.tar
  docker load < _cache/specktre.tar
else
  echo "*** No cache of Docker images; rebuilding from scratch"
fi
