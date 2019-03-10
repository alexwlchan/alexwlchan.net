#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import sys

import requests


def get_session(github_token):
    sess = requests.Session()
    sess.headers = {
        "Accept": "; ".join([
            "application/vnd.github.v3+json",
            "application/vnd.github.antiope-preview+json",
        ]),
        "Authorization": f"token {github_token}",
        "User-Agent": f"GitHub Actions script in {__file__}"
    }

    def raise_for_status(resp, *args, **kwargs):
        try:
            resp.raise_for_status()
        except Exception:
            print(resp.text)
            sys.exit("Error: Invalid repo, token or network issue!")

    sess.hooks["response"].append(raise_for_status)
    return sess


if __name__ == '__main__':
    github_token = os.environ["GITHUB_TOKEN"]
    github_repository = os.environ["GITHUB_REPOSITORY"]

    github_event_path = os.environ["GITHUB_EVENT_PATH"]
    event_data = json.load(open(github_event_path))

    check_run = event_data["check_run"]
    name = check_run["name"]

    sess = get_session(github_token)

    # We should only merge pull requests that have the conclusion "succeeded".
    #
    # We get a check_run event in GitHub Actions when the underlying run is
    # scheduled and completed -- if it doesn't have a conclusion, this field is
    # set to "null".  In that case, we give up -- we'll get a second event when
    # the run completes.
    #
    # See https://developer.github.com/v3/activity/events/types/#CheckRunEvent
    #
    conclusion = check_run["conclusion"]
    print(f"*** Conclusion of {name} is {conclusion}")

    if conclusion is None:
        print(f"*** Check run {name} has not completed, skipping")
        sys.exit(78)

    if conclusion != "success":
        print(f"*** Check run {name} has failed, will not merge PR")
        sys.exit(1)

    # If the check_run has completed, we want to check the pull request data
    # before we declare this PR safe to merge.
    assert len(check_run["pull_requests"]) == 1
    pull_request = check_run["pull_requests"][0]
    pr_number = pull_request["number"]
    pr_src = pull_request["head"]["ref"]
    pr_dst = pull_request["base"]["ref"]

    print(f"*** Checking pull request #{pr_number}: {pr_src} ~> {pr_dst}")
    pr_data = sess.get(pull_request["url"]).json()

    pr_title = pr_data["title"]
    print(f"*** Title of PR is {pr_title!r}")
    if pr_title.startswith("[WIP] "):
        print("*** This is a WIP PR, will not merge")
        sys.exit(78)

    pr_user = pr_data["user"]["login"]
    print(f"*** This PR was opened by {pr_user}")
    if pr_user != "alexwlchan":
        print("*** This PR was opened by somebody who isn't me; requires manual merge")
        sys.exit(78)

    print("*** This PR is ready to be merged.")
    merge_url = pull_request["url"] + "/merge"
    sess.put(merge_url)

    print("*** Cleaning up PR branch")
    pr_ref = pr_data["head"]["ref"]
    api_base_url = pr_data["base"]["repo"]["url"]
    ref_url = f"{api_base_url}/git/refs/heads/{pr_ref}"
    sess.delete(ref_url)
