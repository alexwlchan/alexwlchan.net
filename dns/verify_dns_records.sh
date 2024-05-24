#!/usr/bin/env bash

set -o errexit
set -o nounset

ROOT=$(git rev-parse --show-toplevel)
DNS="$ROOT/dns"

pushd $(mktemp -d)
    echo "boom!"
popd