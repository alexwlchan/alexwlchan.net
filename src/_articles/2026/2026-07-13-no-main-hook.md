---
layout: article
date: 2026-07-13 21:44:05 +01:00
title: A Git hook to prevent committing directly to main
summary: I'm not supposed to commit directly to main, but I often forget, so I have the computer remember for me.
topic: Git
---
At work, we use a standard Git workflow: develop on a feature branch, push to GitHub, and open a pull request to `main`.
Once somebody else approves the PR, the changes get merged.

At least once a week, I forget to branch and commit changes directly to my local `main`.

I only realise my mistake when I try to push and GitHub blocks me.
To untangle myself, I have to create a new branch with my current state, push that instead, and then reset my local `main` back to origin so I can pull other people's changes.
This isn't difficult to fix, but it's annoying -- especially when I often forget to clean up my local `main` until the next time I try to pull.

To stop me getting into this state, I've written a Git `pre-commit` hook.
I saved the following shell script in `.git/hooks/pre-commit` and made it executable:

```bash {"names":{"3":"branch"}}
#!/usr/bin/env bash

set -o errexit
set -o nounset

branch="$(git rev-parse --abbrev-ref HEAD)"

if [ "$branch" = "main" ]; then
   echo "You can't commit directly to main"
   exit 1
fi
```

The [`git rev-parse command`][git-rev-parse-abbrev-ref] prints the short name of the current HEAD.
If I'm on a branch, it returns the branch name; if I'm in a detached HEAD state, it returns `HEAD`.

If the hook detects that I'm on `main`, it exits with an error code.
This aborts the commit and prevents it being saved, serving as a friendly reminder to create a feature branch first -- and leaving my local `main` completely clena.

Ideally I'd always remember to branch when I start a new piece of work -- but since I don't, I'm happy to let the computer remember instead.

[git-rev-parse-abbrev-ref]: https://git-scm.com/docs/git-rev-parse#Documentation/git-rev-parse.txt---abbrev-refstrictloose
