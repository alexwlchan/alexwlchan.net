#!/usr/bin/env bash
# This script will upload the contents of the local _site folder
# to my web server.
#
# Any arguments passed to this script will be passed to the underlying
# rsync command.

set -o errexit
set -o nounset

LINODE_IP=$(tailscale ip --4 linode-vps)

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
  "alexwlchan@$LINODE_IP:repos/alexwlchan.net/_site/" \
  "$@"
