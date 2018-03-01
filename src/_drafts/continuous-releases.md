---
layout: post
link: https://hypothesis.works/articles/continuous-releases/
title: The Hypothesis continuous release process
tags: hypothesis software-development
---

About a year ago, David built a powerful continuous release system for the hypothesis-python repo.
If you push to master with a release note, our CI bumps the version, updates the changelog, tags a new version on GitHub and uploads a new release to PyPI.
With no manual intervention.

This sort of change permanently ruins you.
I'm now so used to continuous deployment, I get annoyed when I work on projects that don't have it (and have thus copied it to several other repos).

If you're interested, I wrote about the process on the Hypothesis blog -- how it works, why we do it, and why we find it so useful.
