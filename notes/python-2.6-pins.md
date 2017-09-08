---
date_added: 8 October 2016
layout: page
minipost: true
slug: notes/python-2.6-pins
title: Pins for Python&nbsp;2.6
---

Although official support for Python&nbsp;2.6 ended [in October&nbsp;2013][pep361], I still have to use it from time-to-time.
Personally, I'd like everywhere to move to 2.7 (or better still, straight to Python&nbsp;3), but that's not always practical.

Lots of third-party packages have been dropping support for 2.6: a move I support, but it can cause problems for left-behind users.
If you use pip to install the latest version of a package, it may break or behave in unexpected ways.
You need to "pin" to an older version &ndash; install that instead of the latest &ndash; but to do so, you need to know which version to pin to.

There are some packages I use on a regular basis.
This page records the version pins I use to get those packages working on Python&nbsp;2.6.
These snippets can be dropped into a `requirements.txt` file or passed to `pip install`.

*   Hypothesis

        hypothesis==2.0.0

*   pylint

        pylint==1.3.1
        astroid==1.2.1

[pep361]: https://www.python.org/dev/peps/pep-0361/