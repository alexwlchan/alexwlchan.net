#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o xtrace

docker run --volume /var/run/docker.sock:/var/run/docker.sock --volume $(pwd):/analytics analytics ruby runner.rb
