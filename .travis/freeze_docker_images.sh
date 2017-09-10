#!/usr/bin/env bash

set -o errexit
set -o nounset

echo "*** Freezing Docker images"
mkdir -p /home/travis/docker
for img in $(docker images --format "{{.Repository}} {{.Tag}}" --filter "dangling=false")
do
  repository=$(echo "$img" | awk '{print $1}')
  tag=$(echo "$img" | awk '{print $2}')
  docker save "$repository:$tag" --output /home/travis/docker/${repository/\//_/}--${tag}.tar
done
