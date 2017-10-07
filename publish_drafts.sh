#!/usr/bin/env sh
# This script copies any items in the _drafts folder into _posts, add
# the date to the filename and front matter, then commit the changes and
# push to GitHub.  It runs as a preprocessor step before builds on master.

set -o errexit
set -o nounset

ROOT=$(git rev-parse --show-toplevel)
SRC=$ROOT/src

if [[ ! -d $SRC/_drafts ]]
then
  echo "*** _drafts directory does not exist, so not publishing any drafts"
  exit 0
fi

for f in $SRC/_drafts/*.md
do
  new_f="$(dirname $f)/$(date +"%Y-%m-%d-")$(basename $f)"
  mv "$f" "$new_f"

  jekyll publish "$new_f"

  git rm "$f"
  mv $ROOT/_posts/$(basename "$new_f") $ROOT/_posts/$(date +"%Y")/$(basename "$new_f")
  git add $ROOT/_posts/$(date +"%Y")/$(basename "$new_f")

  git commit -m "[auto] Publish draft $(basename $f)"
done
