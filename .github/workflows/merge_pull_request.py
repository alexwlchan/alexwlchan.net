#!/usr/bin/env python3

import os
import subprocess
import sys

import httpx


api_client = httpx.Client(
    base_url="https://api.github.com/",
    headers={"Accept": "application/vnd.github.v3+json", "X-GitHub-Api-Version": "2022-11-28"}
)


def current_commit():
    """
    Return the SHA1 hash of the current Git commit.
    """
    cmd = ['git', 'rev-parse', 'HEAD^1']
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
    pr_resp = api_client.get(
        url=f"/repos/alexwlchan/alexwlchan.net/pulls/{pr_number}"
    )
    pr_resp.raise_for_status()

    branch_name = pr_resp.json()['head']['ref']
    print(f'This PR is coming from branch {branch_name}')

    # Check if it's a draft PR -- if so, we shouldn't merge it.
    if pr_resp.json()['draft']:
        print(f'This is a draft PR, so not merging')
        sys.exit(0)

    from pprint import pprint; pprint(pr_resp.json())
    print(current_commit())

    # Check if the branch has been updated since this build started;
    # if so, the build on the newer commit takes precedent.
    commit_id = pr_resp.json()['head']['sha']
    print(f'The current commit on the branch is {commit_id!r}')

    if commit_id != current_commit():
        print(f'The current commit on the branch is {current_commit()}; not the same as this build; aborting')
        sys.exit(0)

    # Now look for other checks running on the same branch.
    #
    # See https://docs.github.com/en/rest/checks/runs?apiVersion=2022-11-28#list-check-runs-for-a-git-reference
    checks_resp = api_client.get(
        f"/repos/alexwlchan/alexwlchan.net/commits/{branch_name}/check-runs"
    )
    checks_resp.raise_for_status()

    for check_run in checks_resp.json()['check_run']:
        if check_run['name'] == 'Build the website':
            continue

        if check_run['status'] != 'completed':
            sys.exit(f"Check run {check_run['name']!r} has not completed")

        if check_run['conclusion'] != 'success':
            sys.exit(f"Check run {check_run['name']!r} did not succeed")

    if len(checks_resp.json()['check_run']) == 1:
        print(f'No other check runs triggered, okay to merge')
    else:
        print(f'All other check runs succeeded, okay to merge')
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
