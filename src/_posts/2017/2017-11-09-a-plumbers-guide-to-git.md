---
layout: post
date: 2017-11-09 18:18:05 +0000
title: A plumber's guide to Git
summary: How does Git work under the hood? How does it store information, and what's really behind a branch? Notes from a workshop at PyCon UK 2017.
tags: pyconuk slides git
category: "Working with Git"

index:
  best_of: true
---

Git is a very common tool in modern development workflows.
It's incredibly powerful, and I use it all the time --- I can't remember the last time I used a version control tool that *wasn't* Git --- but it's a bit of a black box.
How does it actually work?

For a long time, I've only had a vague understand of the Git's inner workings.
I think it's important to understand my tools, because it makes me more confident and effective, so I wanted to learn how Git works under the hood.
To that end, I gave a workshop [at PyCon UK 2017][pycon] about Git internals.
Writing the workshop forced me to really understand what was going on.

The session wasn't videoed, but I do have my notes and exercises.
There were four sections, each focusing on a different Git concept.
It was a fairly standard format: I did a bit of live demo to show the new ideas, then people would work through the exercises on their own laptop.
I wandered around the room, helping people who were stuck, or answering questions, then we'd come together to discuss the exercise.
Repeat.
On the day, we took about 2 1/2 hours to cover all the material.

If you're trying to follow along at home, the Git book has a great section on [the low-level commands of Git][book].
I made heavy reference to this when I wrote the notes and exercises.

If you're interested, you can download the [notes and exercises][notes].

(There are a few amendments and corrections compared to the workshop, because we discovered several mistakes as we worked through it!)

<!-- summary -->

The workshop is split into four sections:

1.  **The Git object database.**

    Getting started: creating a Git repository, looking inside the `.git` folder, and storing some files in the Git object store.
    The idea is to get you comfortable with how Git saves files `.git/objects`, and notice that Git is only keeping the *contents* of files, not the names.

2.  **Blobs and trees.**

    Once you've noticed that `hash-object` doesn't store the names of files, the next set of exercises focuses on *tree* objects, which can save a directory hierarchy.
    The idea is to get you comfortable with tree objects, which gives us a way to take a complete snapshot of a repository's state.

3.  **Creating commits.**

    Now we have snapshots of a repository, but navigating between them can be tricky.
    So you take the trees, and you create commits from them.
    A commit can have extra context (an author, a date, a commit message), so we know why a snapshot is significant.
    You can also construct a history of commits, so you can see how one commit follows another.

4.  **Refs and branches.**

    Commits give us history and context, but we still have to refer to them with commit hashes.
    In the final section, we look at ways to create named references to commits --- which we usually call *branches*.
    How to create a branch, point a branch at a new commit, and how Git stores branches internally.

At the end of the workshop, you should know enough to reconstruct a basic workflow with `git add`, `commit` and `branch`.
I didn't go into remote refs, but the Git book has information on those topics.

The aim of the workshop isn't necessarily to learn the plumbing commands by heart --- you'd never use them in practice --- but by interacting with Git at a low-level, you can build a better mental model of Git under the hood.

[notes]: /files/git_plumbers_guide.pdf
[pycon]: http://2017.pyconuk.org/sessions/workshops/a-plumber-s-guide-to-git/
[book]: https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain
