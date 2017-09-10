---
layout: post
title:  "Identifying lost Git commits"
date:   2017-09-10 16:16:01 +0000
tags: git
theme:
  minipost: true
---

Here's a bit of Git arcana that came up in Slack this evening.

When you delete a branch in Git, the commits on that branch aren't immediately deleted -- there just isn't a branch that points to them.
(These are called *dangling commits*.)
They only get deleted when the garbage collector runs, and deletes commits that aren't reference from anywhere.

Suppose you've inadvertently lost a commit this way.
How do you get it back?

If you know the commit hash, you can run `git cherry-pick <HASH>` to bring it into your current branch -- but that's a big "if".
Maybe you know the commit is lost, but nothing else.

You can see a list of unreferenced objects with `git fsck`, which is used for deep plumbing of the Git database:

```console
$ git fsck --unreachable --no-reflogs
Checking object directories: 100% (256/256), done.
Checking objects: 100% (30181/30181), done.
unreachable commit 2c0098d6091306e5c5c3414e7d25293386a0f822
unreachable commit 2f00b82cd1468bac0a9734e133276f81c380740c
unreachable blob 76005cc4fb3b8261390de46ca5fb59d4bd334d87
unreachable commit b2003852ee8a741b15f2f7cc5afd3e1341e4eb1f
unreachable blob d8003e04da5f2fc7d6bfc227dd8bd165025ac880
...
```

(Here *blobs* are changes which were staged with `git add`, but never formally baked into a commit.)

So we have commit hashes -- but which is the one we want?
We could inspect commits manually with `git show <HASH>`, but that's slow and impractical -- in one of my repos, I have over 3000 dangling objects.
Far more than I could reasonably inspect by hand.

This led to the question in Slack: could we get a list of lost commits, and their commit messages?
Then it would be easy to find the hash for the commit we want.
Unix pipes to the rescue!

First we need to throw away the "Checking object" lines at the top -- that's just noise.
Those two lines are sent to stderr, so filter that to `/dev/null`.
Then we can use `grep` to get just the commits, and `awk` to isolate the commit hash within each line:

```console
$ git fsck --unreachable --no-reflogs 2>/dev/null | grep 'commit' | awk '{print $3}'
2c0098d6091306e5c5c3414e7d25293386a0f822
2f00b82cd1468bac0a9734e133276f81c380740c
b2003852ee8a741b15f2f7cc5afd3e1341e4eb1f
...
```

Now we have a list of hashes, how do we see their commit messages?
The `git show` command allows you to inspect the contents of an individual commit -- including author, date, complete diff -- and we can use it again here.
It includes some useful flags for choosing exactly what to display.
In our case, we want the short hash, the first line of the commit message, and nothing else.
For example:

```console
$ git show --oneline --no-patch 2c0098d6091306e5c5c3414e7d25293386a0f822
2c0098d Add an explicit test for ?includes=items
```

We can add this to our pipeline above (using `xargs`, because we want to call `git show` for every individual hash):

```console
$ git fsck --unreachable --no-reflogs 2>/dev/null | grep 'commit' | awk '{print $3}' | xargs git show --oneline --no-patch
2c0098d Add an explicit test for ?includes=items
2f00b82 The Miro adapter has never lived in SBT
b200385 It's nice if the code compiles
...
```

This won't always save you -- eventually lost commits are garbage collected, and gone forever -- but if a commit is stored locally, and just inaccessible, this is a useful one-liner for finding it quickly.
