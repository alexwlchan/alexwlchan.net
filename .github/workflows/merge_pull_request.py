#!/usr/bin/env python3

import os
import subprocess
import sys
import time

import httpx


api_client = httpx.Client(
    base_url="https://api.github.com/",
    headers={
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)


def current_merge_commit():
    """
    Return the SHA1 hash of the current Git commit.
    """
    cmd = ["git", "rev-parse", "HEAD"]
    return subprocess.check_output(cmd).decode("utf8").strip()


def other_checks_are_running(branch_name):
    # Now look for other checks running on the same branch.
    #
    # See https://docs.github.com/en/rest/checks/runs?apiVersion=2022-11-28#list-check-runs-for-a-git-reference
    checks_resp = api_client.get(
        f"/repos/alexwlchan/alexwlchan.net/commits/{branch_name}/check-runs"
    )
    checks_resp.raise_for_status()

    other_checks = [
        check_run
        for check_run in checks_resp.json()["check_runs"]
        if check_run["name"] != "Merge pull request"
    ]

    for cr in other_checks:
        if cr["status"] == "completed" and cr["conclusion"] != "success":
            print(f"!!! Check run {cr['name']!r} did not succeed", file=sys.stderr)
            sys.exit(1)

    for cr in other_checks:
        if cr["status"] != "completed":
            print(f"Still waiting for {cr['name']!r}...")
            return True

    return False


if __name__ == "__main__":
    # GITHUB_REF is the tag ref that triggered the workflow run,
    # which for pull requests looks something like 'refs/pull/496/merge'.
    github_ref = os.environ["GITHUB_REF"]

    if github_ref.split("/")[1] != "pull":
        sys.exit("GITHUB_REF={github_ref}; is this a pull request?")

    pr_number = github_ref.split("/")[2]
    print(
        f"Deduced pull request as https://github.com/alexwlchan/alexwlchan.net/pull/{pr_number}"
    )

    # Get information about the pull request, in particular the name
    # of the branch.
    #
    # See https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
    pr_resp = api_client.get(url=f"/repos/alexwlchan/alexwlchan.net/pulls/{pr_number}")
    pr_resp.raise_for_status()

    branch_name = pr_resp.json()["head"]["ref"]
    print(f"This PR is coming from branch {branch_name}")

    # Check if it's a draft PR -- if so, we shouldn't merge it.
    if pr_resp.json()["draft"]:
        print("This is a draft PR, so not merging")
        sys.exit(0)

    # Wait 20 seconds for any other check runs to be triggered, then wait
    # until they've all finished.
    time.sleep(20)

    while other_checks_are_running(branch_name):
        time.sleep(2)

    # Check if the branch has been updated since this build started;
    # if so, the build on the newer commit takes precedent.
    merge_commit_id = pr_resp.json()["merge_commit_sha"]
    print(f"The current merge commit on the branch is {merge_commit_id!r}")

    if merge_commit_id != current_merge_commit():
        print(
            f"The current merge commit in GitHub is {current_merge_commit()}; not the same as this build; aborting"
        )
        sys.exit(0)

    # Now look for other checks and see if they succeeded.
    #
    # See https://docs.github.com/en/rest/checks/runs?apiVersion=2022-11-28#list-check-runs-for-a-git-reference
    checks_resp = api_client.get(
        f"/repos/alexwlchan/alexwlchan.net/commits/{branch_name}/check-runs"
    )
    checks_resp.raise_for_status()

    succeeded_checks = set()

    for check_run in checks_resp.json()["check_runs"]:
        if check_run["name"] == "Merge pull request":
            continue

        if check_run["status"] != "completed":
            print(f"!!! Check run {check_run['name']!r} has not completed", file=sys.stderr)
            sys.exit(1)

        if check_run["conclusion"] != "success":
            print(f"!!! Check run {check_run['name']!r} did not succeed", file=sys.stderr)
            sys.exit(1)

        succeeded_checks.add(check_run["name"])

    if len(succeeded_checks) == 0:
        print("No other check runs triggered, okay to merge")
    else:
        print(f"All other check runs succeeded, okay to merge ({succeeded_checks})")

    api_client.put(
        f"/repos/alexwlchan/alexwlchan.net/pulls/{pr_number}/merge",
    )

    api_client.delete(
        f"/repos/alexwlchan/alexwlchan.net/git/refs/heads/{branch_name}",
    )
