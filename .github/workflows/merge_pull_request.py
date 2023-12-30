#!/usr/bin/env python3

import os
import sys

import httpx


if __name__ == '__main__':
    # GITHUB_REF is the tag ref that triggered the workflow run,
    # which for pull requests looks something like 'refs/pull/496/merge'.
    github_ref = os.environ['GITHUB_REF']

    if github_ref.split("/")[1] != "pull":
        sys.exit("GITHUB_REF={github_ref}; is this a pull request?")

    pr_number = github_ref.split("/")[2]
    print(f"Deduced pull request as https://github.com/alexwlchan/alexwlchan.net/pull/{pr_number}")


#
# PULL_NUMBER=$(echo "$GITHUB_REF" | tr '/' ' ' | awk '{print $3}')
# echo
#
# # Get information about the pull request, in particular branch name.
# #
# # See https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
# PR_BRANCH=$(curl \
#     --header "Accept: application/vnd.github.v3+json" \
#     https://api.github.com/repos/alexwlchan/alexwlchan.net/pulls/$PULL_NUMBER |
#   jq -r .head.ref
# )
# echo "This PR is coming from branch '$PR_BRANCH'"
#
# curl \
#   -X PUT \
#   --header "Accept: application/vnd.github.v3+json" \
#   --header "Authorization: token $GITHUB_TOKEN" \
#       "https://api.github.com/repos/alexwlchan/alexwlchan.net/pulls/$PULL_NUMBER/merge"
#
# curl \
#   -X DELETE \
#   --header "Accept: application/vnd.github.v3+json" \
#   --header "Authorization: token $GITHUB_TOKEN" \
#       "https://api.github.com/repos/alexwlchan/alexwlchan.net/git/refs/heads/$PR_BRANCH"
#
