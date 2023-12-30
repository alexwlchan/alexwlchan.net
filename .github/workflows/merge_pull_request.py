#!/usr/bin/env python3

import os
import subprocess
import sys

import httpx


api_client = httpx.Client(
    base_url="https://api.github.com/",
    headers={"Accept": "application/vnd.github.v3+json"}
)


def current_commit():
    """
    Return the SHA1 hash of the current Git commit.
    """
    cmd = ['git', 'rev-parse', 'HEAD']
    return subprocess.check_output(cmd).decode('utf8').strip()


if __name__ == '__main__':
    # GITHUB_REF is the tag ref that triggered the workflow run,
    # which for pull requests looks something like 'refs/pull/496/merge'.
    github_ref = os.environ['GITHUB_REF']

    if github_ref.split("/")[1] != "pull":
        sys.exit("GITHUB_REF={github_ref}; is this a pull request?")

    pr_number = github_ref.split("/")[2]
    print(f"Deduced pull request as https://github.com/alexwlchan/alexwlchan.net/pull/{pr_number}")

    # Get information about the pull request, in particular the name
    # of the branch.
    #
    # See https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
    resp = api_client.get(
        url=f"/repos/alexwlchan/alexwlchan.net/pulls/{pr_number}"
    )
    resp.raise_for_status()

    branch_name = resp.json()['head']['ref']
    print(f'This PR is coming from branch {branch_name}')

    # Check if the branch has been updated since this build started;
    # if so, the build on the newer commit takes precedent.
    commit_id = resp.json()['head']['sha']

    if commit_id != current_commit():
        print('This commit isn’t the same as the current branch; aborting')
        sys.exit(0)

#
# # Get information about the pull request, in particular branch name.
# #
# # See https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
# PR_BRANCH=$(curl \
#     --header "Accept: application/vnd.github.v3+json" \
#      |
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
