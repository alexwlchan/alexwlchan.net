#!/usr/bin/env bash

set -o errexit
set -o nounset

git ls-tree --name-only HEAD src/_drafts/ | xargs mate
