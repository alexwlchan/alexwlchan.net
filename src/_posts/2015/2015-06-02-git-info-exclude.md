---
category: Git
date: 2015-06-02 18:09:00 +0000
layout: post
summary: Another way to ignore untracked files in Git.
tags: git
title: 'Useful Git features: a per-clone exclude file (.git/info/exclude)'
---

With Git, you can define a list of rules to tell it which files should never be checked in as part of a commit. These "ignore rules" could include files which auto-generated, compiled from source or temporary &ndash; anything you don't need to keep around.

Until this morning, I only knew about two places where I could store these rules:

1.  **Globally: use `~/.gitignore_global`.**

    The rules in this file apply to every Git repo on your computer. It's useful, but not very interesting &ndash; [mine](/files/gitignore_global.txt) is just a list of file types that I (almost) never want to check in to Git.

    This isn't attached to a particular repo, so I use Dropbox to sync it between my computers.

2.  **Per-repo: use `.gitignore`.**

    The rules in this file can be tailed to fit one repo. You can check in this file alongside your code, so the same rules apply whenever the repo gets checked out.

Those two files cover about 95% of my use cases. But sometimes I write rules that I don't want to be checked in or globally applied: locally-generated files that I'm unlikely to create again.

Doing a bit of Googling, I stumbled upon a solution:

<ol start="3">
<li>
  <p><strong>Per-clone: use <code>.git/info/exclude</code>.</strong></p>

  <p>This file contains a list of ignore rules, but it doesn't get checked in with the repo. It's exactly what I was looking for.</p>
</li>
</ol>

Despite using Git for almost five years, I've never come across this file. It makes sense that it exists &ndash; it fills a natural gap left by the first two files &ndash; but I never knew it was there. It just goes to show: there's always more to learn.