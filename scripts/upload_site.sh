#!/usr/bin/env bash
# This script will upload the contents of the local _site folder
# to my web server.
#
# Any arguments passed to this script will be passed to the underlying
# rsync command.

set -o errexit
set -o nounset
set -o xtrace

rsync \
  --compress \
  --archive \
  --recursive \
  --delete \
  --verbose \
  --exclude="my-tools/add-cover-to-ao3-epubs/index.html" \
  --exclude="my-tools/list-youtube-likes/" \
  --exclude="my-tools/library-lookup/" \
  --exclude="ideas-for-inclusive-events/" \
  --include="" \
  --filter="" \
  "_site/" \
  "alexwlchan@alexwlchan.net:repos/alexwlchan.net/_site/" \
  "$@"
