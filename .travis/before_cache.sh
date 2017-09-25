#!/usr/bin/env bash

set -o errexit
set -o nounset

sudo service docker stop
sudo chown -R travis ~/docker
