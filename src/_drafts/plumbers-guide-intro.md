---
layout: page
title: A Plumber's Guide to Git -- Introduction
tags: git
summary: Git is a fundamental part of many modern developer workflows -- but how does it really work under the hood?  In this series, we'll learn about the fundamentals of Git internals.
---

On Tuesday, the third run of my workshop *A Plumber's Guide to Git*, at [the Cambridge Python User Group][meetup].
I've also run it at PyCon UK and in my workplace.
On all three occasions, it's been very popular and I've had good feedback -- and on Tuesday, we actually ran out of space in the room!
So to make it as accessible as possible, I'm going to write it up as a series of blog posts.

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



[meetup]:

<!-- summary -->

The
