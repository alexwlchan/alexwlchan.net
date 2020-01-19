---
layout: post
title: A Docker image to run LaTeX
summary:
category: LaTeX
link: https://github.com/alexwlchan/tex-dockerfile
---

These days, I do less and less writing that needs to be printed, but when I do, my tool of choice is still LaTeX.
Because I don't use it very often, my local installation is often out-of-date or broken, and I waste time getting back to a working setup.

A few months back, I wrote a Dockerfile for running LaTeX, and it's worked pretty well.
Every time I start a new document, it builds on the first try.

The Dockerfile installs a minimal version of TeX Live, then has `tlmgr` available (the TeX Live package manager) if I need to install extra packages.
The base image is small, so it builds quickly, and then I extend that image to add new packages.

If you use LaTeX regularly, you probably have an installation you keep up-to-date and working, and this may not be for you.
But if, like me, you're an occasional user, you might want to give this a try.
The code and instructions for using the image are both [on GitHub](https://github.com/alexwlchan/tex-dockerfile).
