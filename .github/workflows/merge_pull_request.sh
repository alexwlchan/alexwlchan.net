#!/usr/bin/env bash

set -o errexit
set -o nounset

# GITHUB_REF is the tag ref that triggered the workflow run,
# which for pull requests looks something like 'refs/pull/496/merge'.
REF_PART=$(echo "$GITHUB_REF" | tr '/' ' ' | awk '{print $2}')

if [[ "$REF_PART" != "pull "]]
then
  echo "GITHUB_REF=$GITHUB_REF; is this a pull request?" >&2
  exit 1
fi

PULL_NUMBER=$(echo "$GITHUB_REF" | tr '/' ' ' | awk '{print $3}')
echo "Deduced pull request as https://github.com/alexwlchan/alexwlchan.net/pull/$PULL_NUMBER"

# Get information about the pull request, in particular branch name.
#
# See https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
curl \
  --header "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/alexwlchan/alexwlchan.net/pulls/$PULL_NUMBER
