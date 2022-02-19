#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o verbose

make deploy-prod

git remote add ssh-origin git@github.com:alexwlchan/alexwlchan.net.git
git push --verbose ssh-origin HEAD:live