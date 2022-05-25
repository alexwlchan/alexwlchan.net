#!/usr/bin/env bash

set -o errexit
set -o nounset

echo "$GITHUB_REPOSITORY"
echo "$GITHUB_EVENT_PATH"
echo "$GITHUB_REF"