#!/usr/bin/env sh

set -o errexit
set -o nounset
set -o verbose

# Some links that were useful in getting 'gem install' to work:
#
#   - https://jekyllrb.com/docs/installation/
#   - https://github.com/ffi/ffi/issues/485
#
apk update
apk add g++ libffi-dev make musl-dev ruby ruby-dev

# Required for the static file generator
apk add rsync

# Required for the publish-drafts gem
apk add git

bundle install

# These packages are only required for installation, not for running Jekyll
apk del --purge g++ make musl-dev ruby-dev
rm -rf /var/cache/apk/*
