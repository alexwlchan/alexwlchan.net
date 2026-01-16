---
layout: til
title: Pushing with `--force-with-lease` is safer than with `--force`
summary: |
  It checks the remote state of the origin hasn't changed since you last fetched, so you don't risk overwriting anybody else's commits.
date: 2018-10-24 09:20:00 +00:00
tags:
  - git
---

When doing a `git push`, if there are different commits in the remote, your push is rejected.
This often happens if I've rebased against master.

You can get round this by running `git push --force`, but what if your rebase wasn't the only change?
What if somebody else pushed commits while you weren't looking?
This can be dangerous!

Using `git push --force-with-lease` is safer, because it checks the branch hasn't moved in the meantime.
Quoting [`--force` considered harmful; understanding git's `--force-with-lease`](https://developer.atlassian.com/blog/2015/04/force-with-lease/):

> What `--force-with-lease` does is refuse to update a branch unless it is the state that we expect; i.e. nobody has updated the branch upstream.
