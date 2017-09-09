#!/usr/bin/env bash

set -o errexit
set -o nounset

if [[ -f .cache/alexwlchan_build.tar ]]
then
  docker load .cache/alexwlchan_build.tar
  docker load .cache/specktre.tar
fi
