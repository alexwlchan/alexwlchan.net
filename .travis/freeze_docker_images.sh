#!/usr/bin/env bash

set -o errexit
set -o nounset

echo "*** Freezing Docker images"
mkdir -p /home/travis/docker
for img in $(docker images --format "{{.ID}}")
do
  docker save "$img" --output "/home/travis/docker/$img.tar"
done
