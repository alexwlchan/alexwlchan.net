#!/usr/bin/env bash

set -o errexit
set -o nounset

ls .cache

if [[ -f .cache/alexwlchan_build.tar ]]
then
  echo "Cached Docker images exist; reloading from cache"
  docker load < .cache/alexwlchan_build.tar
  docker load < .cache/specktre.tar
else
  echo "No cache of Docker images; rebuilding from scratch"
fi
