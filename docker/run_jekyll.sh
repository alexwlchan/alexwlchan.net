#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o verbose

ROOT=$(git rev-parse --show-toplevel)

JEKYLL_VERSION=4.3.1
JEKYLL_COMMAND_DIR="/usr/local/bundle/gems/jekyll-$JEKYLL_VERSION/lib/jekyll/commands"

docker run --tty --rm \
	--volume /var/run/docker.sock:/var/run/docker.sock \
	--volume "$ROOT:$ROOT" \
	--workdir "$ROOT" \
  --publish 5757:5757 \
  "$DOCKER_IMAGE" "$@"
