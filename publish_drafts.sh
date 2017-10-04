#!/usr/bin/env sh
# This script copies any items in the _drafts folder into _posts, add
# the date to the filename and front matter, then commit the changes and
# push to GitHub.  It runs as a preprocessor step before builds on master.

set -o errexit
set -o nounset
