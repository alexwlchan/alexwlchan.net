---
layout: post
title: Creating a GitHub Action to auto-merge pull requests
summary:
tags:
category: Build automation and build systems
---

GitHub Actions is a new service for “workflow automation” – a sort-of scriptable GitHub. When something happens in GitHub (you open an issue, close a pull request, leave a comment, and so on), you can kick off a script to take further action. The scripts run in Docker containers, so there’s a lot of flexibility in what you can do.

If you’ve not looked at Actions yet, the [awesome-actions repo](https://github.com/sdras/awesome-actions) will give you an idea of the sort of things it can do.

I love playing with build systems

% tweet https://twitter.com/alexwlchan/status/1101601909310439429 %

Tweeted in frustration about GA
Got a call with PM + engineer

[https://twitter.com/alexwlchan/status/1101601909310439429](https://twitter.com/alexwlchan/status/1101601909310439429)

dearth of anything about `check_run` API
this post is an example of how I’m using it to auto-merge pro and clean up the branch

## The problem

I have lots of “single-author” repos on GitHub, where I’m the only person who ever writes code.
The source code for this blog is one example; my junk drawer repo is another.

I have CI set up on those repos to run tests and linting (usually with Travis CI or Azure Pipelines).
I open pull requests when I’m making big changes, but I’m not waiting for code review or approval from anybody else.
I’d rather those PRs were automatically merged if/when they pass tests.

Here’s what I want to happen:

* I open a pull request
* A CI service starts running tests, and they pass
* The pull request is merged

This means my code is merged immediately, and I don’t have lingering pull requests I’ve forgotten to merge.

I’ve experimented with a couple of tools for this (most recently [Mergify](https://mergify.io/)), but I wasn’t happy with any of them.
It felt like GitHub Actions would be a better fit, and give me lots of flexibility in the rules.

## Creating a “Hello World” Action

Let’s start by creating a tiny action that just prints “hello world”.
Using the GitHub Actions docs, create three files:





## Setting up a basic action

I started with a basic inline action:

`.github/main.workflow`
	workflow "on pull request pass, merge the branch" {
	  resolves = ["Auto-merge pull requests"]
	  on = "check_run"
	}

	action "Auto-merge pull requests" {
	  uses = "./.github/auto_merge_pull_requests"
	  secrets = ["GITHUB_TOKEN"]
	}

`.github/auto_merge_pull_requests/Dockerfile`
	FROM python:3-alpine
	MAINTAINER Alex Chan <alex@alexwlchan.net>
	LABEL "com.github.actions.name"="Auto-merge pull requests"
	LABEL "com.github.actions.description"="Merge the pull request after the checks pass"
	LABEL "com.github.actions.icon"="activity"
	LABEL "com.github.actions.color"="green"
	RUN	pip3 install requests
	COPY merge_branch.py /merge_branch.py
	ENTRYPOINT ["python3", "/merge_branch.py"]

`.github/automergepullrequests/mergebranch.py
`	#!/usr/bin/env python
	# -*- encoding: utf-8

	if __name__ == '__main__':
	    print("hello world")

this creates a very basic workflow: whenever the `check_run` event fires, it runs the Docker image defined by `Dockerfile`.
this starts a very basic Python script that prints “hello world”

includes python-requests for making HTTP requests, for interactions with GitHub API

I had a lot of difficulty understanding the check_run event, and this is one of the things I discussed with Phiantic.
[https://developer.github.com/v3/activity/events/types/#checkrunevent](https://developer.github.com/v3/activity/events/types/#checkrunevent)

a check run is a traditional CI integration, e.g. Travis or Circle CI
the event fires when a check is scheduled, started or completes

other difficulty is that not all events are check_runs_
old travis integration

## Adding the logic Action?

let’s start adding logic to the main() function

start by loading the event data
this is a JSON file that’s mounted inside the container, which contains all the info that triggered the action:

	    github_event_path = os.environ["GITHUB_EVENT_PATH"]
	    event_data = json.load(open(github_event_path))

we only want to do something if check_run is completed, otherwise we don’t have enough info to determine if ready to merge

	check_run = event_data["check_run"]
	name = check_run["name"]

	    if check_run["status"] != "completed":
	        print(f"*** Check run {name} has not completed, skipping")
	        sys.exit(78)


exit code 78 = neutral, we don’t do anything
see [https://developer.github.com/actions/creating-github-actions/accessing-the-runtime-environment/#exit-codes-and-statuses](https://developer.github.com/actions/creating-github-actions/accessing-the-runtime-environment/#exit-codes-and-statuses)
(illustration grey / green)

now we can look at the conclusion.
anything except a success means we shouldn’t merge this PR — need to wait for further action

	    if conclusion != "success":
	        print(f"*** Check run {name} has not succeeeded, will not merge PR")
	        sys.exit(1)

if we get this far into the script, we know that the check has completed and succeeded, so now we put in conditions for merging the PR
for me, that’s

* not a WIP PR, marked by “[WIP]" in the PR title
* opened by me. I don’t want PRs from random strangers to be merged! (yes, that happened with mergify)

The check_run event includes a bit of data about PR, which I’ll use for logging:

	    assert len(check_run["pull_requests"]) == 1
	    pull_request = check_run["pull_requests"][0]
	    pr_number = pull_request["number"]
	    pr_src = pull_request["head"]["ref"]
	    pr_dst = pull_request["base"]["ref"]

	    print(f"*** Checking pull request #{pr_number}: {pr_src} ~> {pr_dst}")


but to get the detailed info I want,  need to query pull_requests API:

start with HTTP session for GitHub:

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

adds some headers for authoring with the GitHub api, including the token
using hooks, see old post

the `secrets = ["GITHUB_TOKEN"]` line in `main.workflow` exposes a GitHub API token, which we can use to
create session:


	if __name__ == '__main__':
	    github_token = os.environ["GITHUB_TOKEN"]

	    sess = get_session(github_token)

okay, now checks:


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

if the PR isn’t ready to be merged, use another neutral status – not really a success, but a failing build is more severe than it looks
possible extension: call the reviews API to request a review from me if not there, but not needed yet

if ready, then we can merge it!


	    print("*** This PR is ready to be merged.")
	    merge_url = pull_request["url"] + "/merge"
	    sess.put(merge_url)


and then to keep things tidy, I clean up the PR branch when I’m done:


	    print("*** Cleaning up PR branch")
	    pr_ref = pr_data["head"]["ref"]
	    api_base_url = pr_data["base"]["repo"]["url"]
	    ref_url = f"{api_base_url}/git/refs/heads/{pr_ref}"
	    sess.delete(ref_url)


# putting it all together

combined script
I keep it in a separate repo (not with auto-merging), so you can’t malicious modify the workflow rules and get your own code merged
quite neat, saves me a bit of work every time
no support for multiple checks, probably something with chedck_suite_
