---
layout: page
last_updated: 2018-03-13 08:20:58 GMT
title: A Plumber's Guide to Git
summary: Git is a fundamental part of many modern developer workflows -- but how does it really work under the hood?  In this workshop, we'll learn about the internals of Git.
---

This is the write-up of a workshop I've run several times, first [at PyCon UK][pyconuk], and more recently at [the Cambridge Python User Group][meetup].
I've also run it [at PyCon UK][pyconuk] and in my workplace.

[meetup]: https://www.meetup.com/CamPUG/events/246459416/
[pyconuk]: http://2017.pyconuk.org/sessions/workshops/a-plumber-s-guide-to-git/

Here's the premise:

Git is a key part of many modern development workflows, but its complexity and idiosyncratic user interface means it has a reputation as a magic black box.
How does it actually work?

<figure style="max-width: 331px;">
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

I very much enjoy giving this workshop in person (and I think it works best that way) -- but I can't be everywhere!
For people I can't actually meet, I've written up my notes and exercises, so you can work through it at home.

**If you'd like me to run this workshop at your meetup, conference or workplace, [send me an email](mailto:alex@alexwlchan.net).**

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
It typically takes about two hours.

If you want to follow along, you'll need a computer with Git and a text editor installed.
Everything is done with Git in the command line, not in a GUI.

Part 1 introduces [the Git object store][part 1], and explains how to store individual files in Git.
Part 2 adds [the idea of trees][part 2], which allow us to take the snapshot of an entire repo.
In part 3, we add some context to our snapshots by [creating commits][part 3].
The [final part][part 4] gives human-readable labels to commits.
Finally, there's a short [conclusion][conclusion] that recaps the entire workshop.

[part 1]: /a-plumbers-guide-to-git/1-the-git-object-store/
[part 2]: /a-plumbers-guide-to-git/2-blobs-and-trees/
[part 3]: /a-plumbers-guide-to-git/3-context-from-commits/
[part 4]: /a-plumbers-guide-to-git/4-refs-and-branches/
[conclusion]: /a-plumbers-guide-to-git/conclusion/
