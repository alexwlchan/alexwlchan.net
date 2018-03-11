---
layout: page
last_updated: 2018-03-11 14:27:32 +0000
title: Part 4: Refs and branches
---

introductory waffle

at end of part 3, can construct hisotry in a repo
but passing around commit hashes is unwieldy
let's given them better names!

## Introduction

so far worked exclusively in .git/objects folder
what about .git/refs?

check -- it's empty, just two empty dirs

let's put somthing there

```
$ git update-ref refs/heads/master b440a10affe724badb4cf7cece898738ee2e3c18
$ git rev-parse master
b440a10affe724badb4cf7cece898738ee2e3c18
$ cat .git/refs/heads/master
b440a10affe724badb4cf7cece898738ee2e3c18
```

now we can use "master" as a standin for that commit

```
$ git cat-file -p master
tree 4215a014f4613f4ef4e2d6deb107b330e753aace
parent 418816bdefa8889cf5e02e27b8f37157ff506bd1
author Alex Chan <alex@alexwlchan.net> 1520779952 +0000
committer Alex Chan <alex@alexwlchan.net> 1520779952 +0000

Adding alliteration.txt
```

or git log master?

we've created our first branch!

now create a new commit and second branch:

```
$ git update-index --add crayfish.txt

alexwlchan at Alexs-MacBook-2.local in ~/workshop-repo on git:master
$ git write-tree
446342e3d00c97ee14170502262ac1a5c9a2cb4d

alexwlchan at Alexs-MacBook-2.local in ~/workshop-repo on git:master
$ git ^C

alexwlchan at Alexs-MacBook-2.local in ~/workshop-repo on git:master
$ echo "Add a new file: crayfish.txt" | git commit-tree 446342e3d00c97ee14170502262ac1a5c9a2cb4d -p master
cd29d1987067863c3d7aba10a1ff03c66a6f7310

$ git update-ref refs/heads/dev cd29d1987067863c3d7aba10a1ff03c66a6f7310
```

and we can see list of branches with porcelain command:

```
$ git branch
  dev
* master
```

* == we're on the master branch

```
$ cat .git/HEAD
ref: refs/heads/master
```

can tell git we're on the dev branch instead:

```
$ git symbolic-ref HEAD refs/heads/dev

alexwlchan at Alexs-MacBook-2.local in ~/workshop-repo on git:dev
$ git branch
* dev
  master
```

notice that master still points at old commit:

```
$ git rev-parse master
b440a10affe724badb4cf7cece898738ee2e3c18
```

we have to advance it manually -- this is one of the niceties that commit gives us

```
git update-ref refs/heads/master cd29d1987067863c3d7aba10a1ff03c66a6f7310
```

final set of exercises!

---

## Exercises

1.  Look in your `.git/refs` directory.
    Check it only contains two empty directories.

2.  Take one of the commits you created in part 3, and create a *master* branch.
    Use a porcelain `git log` to look at all the commits on this branch.

3.  Have another look inside the `.git/refs` folder.
    What do you see?

4.  Create some moe commits, and then check that *master* hasn't changed.
    Advance *master* to your latest commit.

5.  Create a second branch *dev*.
    Add some more commits, and advance *dev* to your latest commit.
    Check that *master* hasn't moved.

Repeat this a couple of times, so you get really comfortable creating branches.
Use a `git branch` to check your work.

To finish off, here are a couple of bonus exercises:

6.  If a branch is created by a file in `.git/refs`, can you think how you might delete a branch?
    Try it, and use `git branch` to check you were successful.

7.  There's a second folder in `.git/refs` -- `tags`.
    What if you create a ref that points to someting in that folder?
    Where do those appear?

## Useful commands

Don't peek!
Try the exercises on your own machine, then scroll past the picture of the folders to get the commentary

https://www.pexels.com/photo/brown-tree-and-green-leaf-51329/

---

## Commentary

hopefully you're comfortbale creating branches

this is why people say branches are cheap in git -- just tiny pointers to commits

so branches point to commits
... which point to commits and trees
... which point to trees and blobs
... which point to the contents of a file

<< diagram >>

so now we can reconstruct the state of repo at any point in history, and we have the context to know why those points are significant, and we have human-friendly names for tracking our progress

now you've seen everything that happens in a thpical git workflow:

*   git add -- hash-object, update-index -w
*   git commit = write-tree, git commit-tree, update branch in HEAD
*   git branch

hopefully you have a better understanding of how git works under the hood, and just how much happens in a typical workflow!

if you've found this useful, drop me an email?
feedback always appreciated!
