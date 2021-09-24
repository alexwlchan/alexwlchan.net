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

# Required to create avatar thumbnails in the Twitter gem
apk add imlib2 imlib2-dev libexif-dev

# Required for libsass.  If this is missing, you get the error:
#
#   LoadError: Could not open library
#   '/usr/local/bundle/gems/sassc-2.1.0-x86_64-linux/lib/sassc/libsass.so':
#   Error loading shared library ld-linux-x86-64.so.2: No such file or directory
#   (needed by /usr/local/bundle/gems/sassc-2.1.0-x86_64-linux/lib/sassc/libsass.so)
#
apk add --update gcompat

bundle install

# These packages are only required for installation, not for running Jekyll
apk del --purge g++ make musl-dev ruby-dev
rm -rf /var/cache/apk/*
