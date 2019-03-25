---
layout: post
date: 2018-08-02 07:31:35 +0000
title: Selective sudo on Travis
tags: travis build-systems
summary: I recently learnt how to set up Travis with a mixture of VMs and containers – not just all of one or the other.
category: Build automation and build systems
---

I'm a heavy user of [Travis CI][travis].
If you don't know it, Travis is a service for automatically building and testing your code.
You tell it how to run your tests, and when you commit to GitHub, it runs your tests and tells you the result.
I use Travis to run tests at work, test and release several open source projects I work on, and it even builds this blog!

If you're running builds on Linux, Travis offers [two  build environments][buildenv]:

> **Sudo-enabled**
>
> A sudo enabled, full virtual machine per build, that runs Linux, either Ubuntu Precise 12.04 or Ubuntu Trusty&nbsp;14.04.
>
> **Container-based**
>
> A fast boot time environment in which sudo commands are not available. Running Linux Ubuntu Trusty&nbsp;14.04.

The container-based builds are usually much faster, and I prefer using them when I can.
The main distinction for me is "do I need Docker" -- I use Docker in a lot of my projects, and that's only available in the sudo-enabled builds.

In your Travis build, you can have multiple "jobs" -- processes that run on different build machines.
For example, you might test your Python library with three versions of Python in three separate jobs.

Until recently, I thought sudo-vs-containers was all or nothing.
If any of my jobs needed sudo, I had to add `sudo: required` at the top of my Travis config, and every job would get the slower VMs -- even if they could run in a container instead.

Thanks to Anthony Sottile, I know that's no longer the case!
Anthony opened a [pull request for Hypothesis][pullrequest] adding Python&nbsp;3.7 support to the build, which requires a sudo-enabled Travis build machine.
This is the relevant snippet from the build config:

```yaml
# .travis.yml
sudo: false

jobs:
  include:
    - env: TASK=check-py35
    - env: TASK=check-py36
    - env: TASK=check-py37
      sudo: required
      dist: xenial
```

Adding `sudo: required` to the individual job runs the py37 job in a sudo-enabled environment, but the py35 and py36 jobs still run in containers.

I've changed a number of my builds this way to run more jobs on containers, and it's made a nice improvement in build times.
It also makes it easier to add sudo-based jobs to builds in future, because I don't have to take a penalty for switching the other tasks to VMs.

[travis]: https://travis-ci.org/
[buildenv]: https://docs.travis-ci.com/user/reference/overview/#virtualization-environments
[pullrequest]: https://github.com/HypothesisWorks/hypothesis/pull/1376
