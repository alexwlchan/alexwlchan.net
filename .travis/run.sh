#!/usr/bin/env bash

set -o errexit
set -o nounset

make build

if [[ "$TRAVIS_EVENT_TYPE" == "pull_request" ]]
then
  echo "*** Pull request, skipping deploy to prod"
  exit 0
fi

.travis/deploy.sh
