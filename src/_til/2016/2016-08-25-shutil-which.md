---
layout: til
title: You can use `shutil.which` to check if an executable is in your PATH
summary: This is useful for checking if something's installed.
date: 2016-08-25 05:49:52 +0000
tags:
  - python
---
[`shutil.which()`](https://docs.python.org/3/library/shutil.html#shutil.which) returns the path to the executable, or `None` if you don't have it installed:

```pycon
>>> import shutil
>>> shutil.which('python3')
'/opt/homebrew/bin/python3'
>>> shutil.which('python2.7')
>>> shutil.which('python2.7') is None
True
```

I used to accomplish something similar with `subprocess`, but this is a bit simpler and clearer.
