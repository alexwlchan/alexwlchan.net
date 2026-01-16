---
layout: til
title: Why does Hypothesis try the same example three times before failing?
date: 2016-12-01 21:50:00 +00:00
tags:
  - python
  - python:hypothesis
---

From the #hypothesis IRC channel:

*   Once to find the failure
*   Once to check the failure isn’t flakey
*   Once to create a failure which is spotted by the test runner
