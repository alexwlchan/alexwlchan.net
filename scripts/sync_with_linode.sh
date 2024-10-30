#!/usr/bin/env bash
# This script can be used to synchronise my local build with the
# _site folder on GitHub.
#
# There are two options:
#
#     $ sync_with_linode.sh pull
#         This pulls the latest code from Linode to the local _site folder.
#
#     $ sync_with_linode.sh push
#         This replaces the site on the Linode with my local _site folder.
#         This will only push production builds of the site.
#

set -o errexit
set -o nounset

if (( $# != 1 ))
then
  echo "Usage: $0 push|pull" >&2
  exit 1
fi

case $1 in
  "pull")
    SOURCE="alexwlchan@harmonia.linode:repos/alexwlchan.net/_site/"
    TARGET="_site"
    ;;

  "push")
    if ! grep -q '<meta name="jekyll-environment" content="production" >' _site/index.html
    then
      echo "Will not push development build of site!" >&2
      exit 1
    fi
    
    SOURCE="_site"
    TARGET="alexwlchan@harmonia.linode:repos/alexwlchan.net/_site/"
    ;;

  *)
    echo "Usage: $0 push|pull" >&2
    exit 1
    ;;
esac

rsync \
  --archive \
  --compress \
  --verbose \
  --recursive \
  --progress \
  --delete \
  "$SOURCE" "$TARGET"
