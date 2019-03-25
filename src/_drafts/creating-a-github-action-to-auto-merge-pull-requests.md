---
layout: post
title: Creating a GitHub Action to auto-merge pull requests
summary:
tags:
category: Build automation and build systems
---

[GitHub Actions][actions] is a new service for “workflow automation” – a sort-of scriptable GitHub. When something happens in GitHub (you open an issue, close a pull request, leave a comment, and so on), you can kick off a script to take further action. The scripts run in Docker containers inside GitHub's infrastructure, so there’s a lot of flexibility in what you can do.

If you’ve not looked at Actions yet, the [awesome-actions repo](https://github.com/sdras/awesome-actions) can give you an idea of the sort of things it can do.

I love playing with build systems, so I wanted to try it out -- but I had a lot of problems getting started.
At the start of March, I tweeted in frustration:

{% tweet https://twitter.com/alexwlchan/status/1101601909310439429 %}

A few days later, I got a DM from [Angie Rivera][angie], the Product Manager for GitHub Actions.
We arranged a three-way call with [Phani Rajuyn][phani], one of GitHub's software engineers, and together we spent an hour talking about Actions.
I was able to show them the rough edges I'd been hitting, and they were able to fill in the gaps in my understanding.

After our call, I got an Action working, and I've had it running successfully for the last couple of weeks.

In this post, I'll explain how I wrote an Action to auto-merge my pull requests.
When a pull request passes tests, GitHub Actions automatically merges the PR and then deletes the branch:

{%
  image
  :filename => "github_actions_merge.png",
  :alt => "A screenshot of the GitHub pull request UI, showing the github-actions bot merging and deleting a branch.",
  :style => "width: 700px;"
%}

If you just want the code, [skip to the end](#putting-it-all-together) or check out [the GitHub repo][repo].

[actions]: https://github.com/features/actions
[angie]: https://twitter.com/AngieRvra
[phani]: https://twitter.com/PhaniRajuyn
[repo]: https://github.com/alexwlchan/auto_merge_my_pull_requests



## The problem

I have lots of “single-author” repos on GitHub, where I’m the only person who ever writes code.
The source code [for this blog][alexwlchan.net] is one example; my [junk drawer repo][junkdrawer] is another.

I have CI set up on some of those repos to run tests and linting (usually with Travis CI or Azure Pipelines).
I open pull requests when I’m making big changes, so I get the benefit of the tests -- but I’m not waiting for code review or approval from anybody else.
What used to happen is that I'd go back later and merge those PRs manually -- but I'd rather they were automatically merged if/when they pass tests.

Here’s what I want to happen:

* I open a pull request
* A CI service starts running tests, and they pass
* The pull request is merged and the branch deleted

This means my code is merged immediately, and I don’t have lingering pull requests I’ve forgotten to merge.

I’ve experimented with a couple of tools for this (most recently [Mergify](https://mergify.io/)), but I wasn’t happy with any of them.
It felt like GitHub Actions could be a good fit, and give me lots of flexibility in deciding whether a particular pull request should be merged.

[alexwlchan.net]: https://github.com/alexwlchan/alexwlchan.net
[junkdrawer]: https://github.com/alexwlchan/junkdrawer



## Creating a “Hello World” Action

Let’s start by creating a tiny action that just prints “hello world”.
Working from the example in the [GitHub Actions docs][getting_started], create three files:

```hcl
# .github/main.workflow
workflow "on pull request pass, merge the branch" {
  resolves = ["Auto-merge pull requests"]
  on       = "check_run"
}

action "Auto-merge pull requests" {
  uses = "./auto_merge_pull_requests"
}
```

```dockerfile
# auto_merge_pull_requests/Dockerfile
FROM python:3-alpine

MAINTAINER Alex Chan <alex@alexwlchan.net>

LABEL "com.github.actions.name"="Auto-merge pull requests"
LABEL "com.github.actions.description"="Merge the pull request after the checks pass"
LABEL "com.github.actions.icon"="activity"
LABEL "com.github.actions.color"="green"

COPY merge_pr.py /
ENTRYPOINT ["python3", "/merge_pr.py"]
```

```python
# auto_merge_pull_requests/merge_pr.py
#!/usr/bin/env python
# -*- encoding: utf-8

if __name__ == "__main__":
    print("Hello world!")
```

The Dockerfile and Python script define a fairly standard Docker image, which prints `"Hello world!"` when you run it.
This is where we'll be adding the interesting logic.
I'm using Python instead of a shell script because I find it easier to write safe, complex programs in Python than in shell.

Then the `main.workflow` file defines the following series of steps:

*   When the `check_run` event fires, run the `Auto-merge pull requests` action
*   When the action runs, build and run the Docker image defined in `./auto_merge_pull_requests`
*   When the Docker image runs, print `"Hello world!"`

I had a lot of difficulty understanding how the `check_run` event works, and Phani and I spent a lot of time discussing it on our call.

A *check run* is a third-party CI integration, like Travis or Circle CI.
A [*check run event*][cr_event] is fired whenever the state of a check changes.
That includes:

*   When the check is *scheduled* (GitHub tells Travis "please run these tests")
*   When a check *starts* (Travis tells GitHub "I have started running these tests")
*   When a check *completes* (Travis tells GitHub "These tests are finished, here is the result")

That last event is what's interesting to me -- if the tests completed and they've passed, I want to take further action.

What confused me is that not all CI integrations use the Checks API -- in particular, a lot of my Travis setups were using a legacy integration that doesn't involve checks.
Travis [started using the Checks API][travis_checks] nine months ago, but I missed the memo, and hadn't migrated my repos.
Until I moved to the Checks integration, it looked as if GitHub was just ignoring my builds.

[getting_started]: https://developer.github.com/actions/creating-github-actions/creating-a-new-action/
[cr_event]: https://developer.github.com/v3/activity/events/types/#checkrunevent
[travis_checks]: https://developer.github.com/v3/activity/events/types/#checkrunevent

## Adding the logic

We start by loading the event data.
When GitHub Actions runs a container, it includes a JSON file with data from the event that triggered it.
It passes the path to this file as the `GITHUB_EVENT_PATH` environment variable.
So let's open and load that file:

```python
import json
import os


if __name__ == "__main__":
    event_path = os.environ["GITHUB_EVENT_PATH"]
    event_data = json.load(open(event_path))
```

We only want to do something if the check run is completed, otherwise we don't have enough information to determine if we're ready to merge.
The GitHub developer docs explain what [the fields on a check_run event look like][event], and the "status" field tells us the current state of the check:

```python
import sys


if __name__ == "__main__":
    ...
    check_run = event_data["check_run"]
    name = check_run["name"]

    if check_run["status"] != "completed":
        print(f"*** Check run {name} has not completed")
        sys.exit(78)
```

Calling `sys.exit` means we bail out of the script, and don't do anything else.
In a GitHub Action, exit code 78 is a [*neutral* status][exit_code].
It's a way to say "we didn't do any work".
This is what it looks like in the UI, compared to a successful run:

{%
  image
  :filename => "github_actions_neutral.png",
  :alt => "Two rows of text, both saying “on pull request pass, merge the branch”, one with a grey square, one with a green tick.",
  :style => "width: 411px;"
%}

[event]: https://developer.github.com/v3/activity/events/types/#checkrunevent
[exit_code]: https://developer.github.com/actions/creating-github-actions/accessing-the-runtime-environment/#exit-codes-and-statuses

If we know the check has completed, we can look at how it completed.
Anything except a success means something has gone wrong, and we shouldn't merge the PR -- it needs manual inspection.

```python
    if check_run["conclusion"] != "success":
        print(f"*** Check run {name} has not succeeded")
        sys.exit(1)
```

Here I'm dropping an explicit failure.
The difference between a failure and a neutral status is that a failure blocks any further steps in the workflow, whereas a neutral result lets them carry on.
Here, something has definitely gone wrong -- the tests haven't passed -- so we shouldn't continue to subsequent steps.

If the script is still running, then we know the tests have passed, so let's put in the conditions for merging the pull request.
For me, that means:

*   It's not a work-in-progress, marked by "[WIP]" in the title
*   It was opened by me.
    I don't want to automatically merge pull requests from random strangers.
    (This happened once with Mergify!
    My rule said "merge anything that passes tests", somebody opened a typo fix, it passed tests… and got merged while I was asleep.)

The check_run event includes a bit of data about the pull request, including the PR number and the branches.
I use this for a bit of logging:

```python
    assert len(check_run["pull_requests"]) == 1
    pull_request = check_run["pull_requests"][0]
    pr_number = pull_request["number"]
    pr_src = pull_request["head"]["ref"]
    pr_dst = pull_request["base"]["ref"]

    print(f"*** Checking pull request #{pr_number}: {pr_src} ~> {pr_dst}")
```

But for the detailed information like title and pull request author, I need to query the [pull requests API][pr_api].
Let's start by creating an HTTP session for working with the GitHub API:

```python
import requests


def create_session(github_token):
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
```

This helper method creates an HTTP session that, on every request:

*   Adds the Accept headers that the GitHub API wants (these seem to change frequently, so may not match the current docs)
*   Adds an authorization header with my API token
*   Adds a User-Agent string
*   Checks if the API returned a 200 OK response, and throws an exception if not.
    This uses a requests hook, which I've written about [in a previous post][hooks].

[pr_api]: https://developer.github.com/v3/pulls/
[hooks]: /2017/10/requests-hooks/

I have to add `pip3 install requests` to the `Dockerfile` so I can use the requests library.

Then I modify the action in my `main.workflow` to expose an API token to my running code:

```hcl
action "Auto-merge pull requests" {
  uses    = "./auto_merge_pull_requests"
  secrets = ["GITHUB_TOKEN"]
}
```

This is one of the convenient parts of GitHub Actions -- it creates this API token for us at runtime, and passes it into the container.
We don't need to much around creating and rotating API tokens by hand.

We can read this environment variable to create a session:

```python
    github_token = os.environ["GITHUB_TOKEN"]

    sess = create_session(github_token)
```

Now let's read some data from the pull requests API, and run the checks:

```python
    pr_data = sess.get(pull_request["url"]).json()

    pr_title = pr_data["title"]
    print(f"*** Title of PR is {pr_title!r}")
    if pr_title.startswith("[WIP] "):
        print("*** This is a WIP pull request, will not merge")
        sys.exit(78)

    pr_user = pr_data["user"]["login"]
    print(f"*** This PR was opened by {pr_user}")
    if pr_user != "alexwlchan":
        print("*** This pull request was opened by somebody who isn't me")
        sys.exit(78)
```

If the PR isn't ready to be merged, I use another neutral status -- a failing build and a red X would look more severe than it really is.

If it's ready and we haven't bailed out yet, we can merge the pull request!

```python
    print("*** This pull request is ready to be merged.")
    merge_url = pull_request["url"] + "/merge"
    sess.put(merge_url)
```

Then to keep things tidy, I delete the PR branch when I’m done:

```python
    print("*** Cleaning up pull request branch")
    pr_ref = pr_data["head"]["ref"]
    api_base_url = pr_data["base"]["repo"]["url"]
    ref_url = f"{api_base_url}/git/refs/heads/{pr_ref}"
    sess.delete(ref_url)
```

This last step partially inspired by Jessie Frazelle's [branch cleanup action][cleanup], which is one of the first actions I used, and was a useful example when writing this code.

[cleanup]: https://github.com/jessfraz/branch-cleanup-action

## Putting it all together

Here's the final version of the code:

```hcl
# .github/main.workflow
workflow "on pull request pass, merge the branch" {
  resolves = ["Auto-merge pull requests"]
  on       = "check_run"
}

action "Auto-merge pull requests" {
  uses    = "./auto_merge_pull_requests"
  secrets = ["GITHUB_TOKEN"]
}
```

```dockerfile
# auto_merge_pull_requests/Dockerfile
FROM python:3-alpine

MAINTAINER Alex Chan <alex@alexwlchan.net>

LABEL "com.github.actions.name"="Auto-merge pull requests"
LABEL "com.github.actions.description"="Merge the pull request after the checks pass"
LABEL "com.github.actions.icon"="activity"
LABEL "com.github.actions.color"="green"

RUN pip3 install requests

COPY merge_pr.py /
ENTRYPOINT ["python3", "/merge_pr.py"]
```

```python
# auto_merge_pull_requests/merge_pr.py
#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os

import requests


def create_session(github_token):
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


if __name__ == "__main__":
    event_path = os.environ["GITHUB_EVENT_PATH"]
    event_data = json.load(open(event_path))

    check_run = event_data["check_run"]
    name = check_run["name"]

    if check_run["status"] != "completed":
        print(f"*** Check run {name} has not completed")
        sys.exit(78)

    if check_run["conclusion"] != "success":
        print(f"*** Check run {name} has not succeeded")
        sys.exit(1)

    assert len(check_run["pull_requests"]) == 1
    pull_request = check_run["pull_requests"][0]
    pr_number = pull_request["number"]
    pr_src = pull_request["head"]["ref"]
    pr_dst = pull_request["base"]["ref"]

    print(f"*** Checking pull request #{pr_number}: {pr_src} ~> {pr_dst}")

    github_token = os.environ["GITHUB_TOKEN"]

    sess = create_session(github_token)

    pr_data = sess.get(pull_request["url"]).json()

    pr_title = pr_data["title"]
    print(f"*** Title of PR is {pr_title!r}")
    if pr_title.startswith("[WIP] "):
        print("*** This is a WIP PR, will not merge")
        sys.exit(78)

    pr_user = pr_data["user"]["login"]
    print(f"*** This pull request was opened by {pr_user}")
    if pr_user != "alexwlchan":
        print("*** This pull request was opened by somebody who isn't me")
        sys.exit(78)

    print("*** This pull request is ready to be merged.")
    merge_url = pull_request["url"] + "/merge"
    sess.put(merge_url)

    print("*** Cleaning up pull request branch")
    pr_ref = pr_data["head"]["ref"]
    api_base_url = pr_data["base"]["repo"]["url"]
    ref_url = f"{api_base_url}/git/refs/heads/{pr_ref}"
    sess.delete(ref_url)
```

I keep this in [a separate repo][auto_merge] (which doesn't have auto-merging enabled), so nobody can maliciously modify the workflow rules and get their own code merged.
I'm not entirely sure what safety checks are in place to prevent workflows modifying themselves, and having an extra layer of separation makes me feel more comfortable.

[auto_merge]: https://github.com/alexwlchan/auto_merge_my_pull_requests

## Putting it to use

If you want to use this code, you'll need to modify the code for your own rules.
Please don't give me magic merge rights to your GitHub repos!

With this basic skeleton, there are lots of ways you could extend it.
You could post comments on failing pull requests explaining how to diagnose a failure.
You could request reviews if you get a pull request from an external contributor, and post a comment thanking them for their work.
You could measure how long it took to run the check, to see if it's slowed down your build times.
And so on.

GitHub Actions feels like it could be really flexible and powerful, and I'm glad to have created something useful with it.
I've had this code running in the repo for this blog for nearly a month, and it's working fine -- saving me a bit of work every time.
It'll even merge the pull request where I've written this blog post.
