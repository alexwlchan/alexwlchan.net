---
layout: page
last_updated: 2018-03-09 16:56:37 +0000
title: A Plumber's Guide to Git
summary: Git is a fundamental part of many modern developer workflows -- but how does it really work under the hood?  In this series, we'll learn about the fundamentals of Git internals.
---

This is the write-up of a workshop I've run several times, first [at PyCon UK][pyconuk], and more recently at [the Cambridge Python User Group][meetup].
I've also run it [at PyCon UK][pyconuk] and in my workplace.

[meetup]: https://www.meetup.com/CamPUG/events/246459416/
[pyconuk]: http://2017.pyconuk.org/sessions/workshops/a-plumber-s-guide-to-git/

Here's the premise:

Git is a key part of many modern development workflows, but its complexity and idiosyncratic user interface means it has a reputation as a magic black box.
How does it actually work?

<figure style="max-width: 330px;">
  <img src="/images/2018/xkcd_git.png">
  <figcaption>
    <em>Git</em>, by Randall Munroe.
    <a href="https://xkcd.com/1597/">XKCD #1597</a>.
    The phrase &ldquo;graph theory tree model&rdquo; doesn&rsquo;t mean much to most people!
  </figcaption>
</figure>

The aim of this workshop is to get an understanding of the underlying concepts of Git.

During the workshop, we learn exactly what happens in a typical Git workflow (`add`, `branch`, `commit`, and so on).
We look inside the `.git` directory, and by the end of the workshop you should be able to describe the internal workings of Git.

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

If you want to follow along, you'll need a computer with Git and a text editor installed.
Everything is done with Git in the command line, not in a GUI.
