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

    # We should only merge pull requests that have the conclusion "succeeded".
    #
    # We get a check_run event in GitHub Actions when the underlying run is
    # scheduled and completed -- if it doesn't have a conclusion, this field is
    # set to "null".  In that case, we give up -- we'll get a second event when
    # the run completes.
    #
    # See https://developer.github.com/v3/activity/events/types/#CheckRunEvent
    #
    if check_run["conclusion"] is None:
        print(f"*** Check run {name} has not completed, skipping")
        sys.exit(0)

    sess = get_session(github_token)

    # Validate the GitHub token
    sess.get(f"https://api.github.com/repos/{github_repository}")

    from pprint import pprint
    pprint(event_data)
