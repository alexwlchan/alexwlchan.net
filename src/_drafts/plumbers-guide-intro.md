---
layout: post
title: A Plumber's Guide to Git -- Introduction
tags: git
summary: Git is a fundamental part of many modern developer workflows -- but how does it really work under the hood?  In this series, we'll learn about the fundamentals of Git internals.
---

On Tuesday, the third run of my workshop *A Plumber's Guide to Git*, at [the Cambridge Python User Group][meetup].
I've also run it [at PyCon UK][pyconuk] and in my workplace.
On all three occasions, it's been very popular and I've had good feedback -- and on Tuesday, we actually ran out of space in the room!
So to make it as accessible as possible, I'm going to write it up as a series of blog posts.

[meetup]: https://www.meetup.com/CamPUG/events/246459416/
[pyconuk]: http://2017.pyconuk.org/sessions/workshops/a-plumber-s-guide-to-git/

Git is a key part of many modern development workflows, but its complexity and idiosyncratic user interface means it has a reputation as a magic black box.
How does it actually work?

<figure style="max-width: 330px;">
  <img src="/images/2018/xkcd_git.png">
  <figcaption>
    <em>Git</em>, by Randall Munroe.
    <a href="https://xkcd.com/1597/">XKCD #1597</a>.
  </figcaption>
</figure>

The aim of this workshop is to get an understanding of the underlying concepts of Git.

During the workshop, we learn what happens in a typical Git workflow (`add`, `branch`, `commit`, and so on).
Advanced commands like `rebase`, `cherry-pick` or `filter-branch` don't make an appearance -- this is more about the fundamentals.

<!-- summary -->

## What's in the name?

Git divides commands into *porcelain* and *plumbing*.

Porcelain is the ceramic material usually used to make sinks or toilets, while plumbing is the actual pipes carrying the water.
The porcelain fixtures provide a human-friendly interface to the plumbing.

In the same manner, porcelain Git commands are the human-friendly, high-level commands, while the plumbing commands are used to directly manipulate the Git internals.
Most of the time, we work entirely with porcelain commands, but in this workshop we spend a lot of time using plumbing commands, as we peer into the underlying Git machinery.

## How does the workshop work?

The workshop is divided into four sections.

Usually I do a short demo and explain the new ideas, then I give out some exercises and everybody works through them on their own computer.
When they're done, we discuss what we learnt, then move on to the next section.
The whole workshop can be done within two hours.

Here I'll be writing a blog post for each section, and I'll link them here when I'm doine.

I expect to post part 1 soon -- so watch this space!
