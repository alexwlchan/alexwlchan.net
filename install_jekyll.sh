#!/usr/bin/env sh

set -o errexit
set -o nounset

# Some links that were useful in getting 'gem install' to work:
#
#   - https://jekyllrb.com/docs/installation/
#   - https://github.com/ffi/ffi/issues/485
#
apk update
apk add g++ libffi-dev make musl-dev ruby ruby-dev

# Other dependencies for gems
apk add nodejs

# Required for the static file generator
apk add rsync

# Required for the pygments gem.  This has to be Python 2, not Python 3:
# https://github.com/tmm1/pygments.rb/issues/45
apk add py2-pip
pip install pygments

bundle install

apk del --purge g++ make musl-dev ruby-dev
rm -rf /var/cache/apk/*
