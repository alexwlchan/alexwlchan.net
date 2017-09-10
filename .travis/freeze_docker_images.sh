#!/usr/bin/env bash

set -o errexit
set -o nounset

echo "*** Freezing Docker images"
mkdir -p /home/travis/docker
for img in $(docker images --format "{{.Repository}}:{{.Tag}}" --filter "dangling=false")
do
  outfile="${img/\//_}.tar"
  outfile="${outfile/:/--}"
  echo "$outfile"
  docker save "$img" --output "/home/travis/docker/$outfile"
done
