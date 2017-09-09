#!/usr/bin/env bash

set -o errexit
set -o nounset

pip install -r _tests/requirements.txt

pushd /tmp
  wget https://github.com/rubys/feedvalidator/archive/master.zip
  unzip master.zip
  pip install -e feedvalidator-master/src
popd

.travis/unfreeze_docker_images.sh
