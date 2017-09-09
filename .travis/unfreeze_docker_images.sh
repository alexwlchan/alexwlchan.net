#!/usr/bin/env bash

set -o errexit
set -o nounset

if [[ -f .cache/alexwlchan_build.tar ]]
then
  cat .cache/alexwlchan_build.tar | docker import - alexwlchan/alexwlchan.net
  cat .cache/specktre.tar | docker import - alexwlchan/specktre
fi
