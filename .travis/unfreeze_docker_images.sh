#!/usr/bin/env bash

set -o errexit
set -o nounset

mkdir -p /home/travis/docker

for tarfile in $(find /home/travis/docker -name '*.tar')
do
  docker load --input "$tarfile"
done
