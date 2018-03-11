---
layout: page
last_updated: 2018-03-11 14:27:32 +0000
title: Part 3: Context from commits
---

introductory waffle

in part 2, we saw how to take snapshots of a repo with trees
but how do we know why snapshots are signifcant?
we need context
we need commits!

## Introduction

let's take a tree, and attach some context

```
$ echo "My first commit" | git commit-tree c249dcb600ddbd958736177ba784798a6143a01e
418816bdefa8889cf5e02e27b8f37157ff506bd1
```

another plumbing command!
this takes a tree, creates a commit object
returns a hash

we can see it in .git/objects:

```
$ find .git/objects -type f
.git/objects/05/443337f802bfec039ec4121570d6c24ccb9eab
.git/objects/41/8816bdefa8889cf5e02e27b8f37157ff506bd1
.git/objects/a3/7f3f668f09c61b7c12e857328f587c311e5d1d
.git/objects/b1/3311e04762c322493e8562e6ce145a899ce570
.git/objects/c2/49dcb600ddbd958736177ba784798a6143a01e
.git/objects/cf/401e115bf7a440ef02216953803271580848dd
```

we can inspect its type:

```
$ git cat-file -t 418816bdefa8889cf5e02e27b8f37157ff506bd1
commit
```

and contents:

```
$ git cat-file -p 418816bdefa8889cf5e02e27b8f37157ff506bd1
tree c249dcb600ddbd958736177ba784798a6143a01e
author Alex Chan <alex@alexwlchan.net> 1520779732 +0000
committer Alex Chan <alex@alexwlchan.net> 1520779732 +0000

My first commit
```

what do we have here?

pointer to tree I used -- snapshot of files and contents

author name/email (from my global gitconfig),
a timestamp -- epoch time
then commit message
difference between author/committer?

so we have standaloen snapshots with context, and even better -- we can combine snapshots into a linear history
add -p flag to supply "parent" commit

```
$ git update-index --add alliteration.txt
$ git write-tree
4215a014f4613f4ef4e2d6deb107b330e753aace
$ echo "Adding alliteration.txt" | git commit-tree 4215a014f4613f4ef4e2d6deb107b330e753aace -p 418816bdefa8889cf5e02e27b8f37157ff506bd1
b440a10affe724badb4cf7cece898738ee2e3c18
```

inspect:

```
$ git cat-file -p b440a10affe724badb4cf7cece898738ee2e3c18
tree 4215a014f4613f4ef4e2d6deb107b330e753aace
parent 418816bdefa8889cf5e02e27b8f37157ff506bd1
author Alex Chan <alex@alexwlchan.net> 1520779952 +0000
committer Alex Chan <alex@alexwlchan.net> 1520779952 +0000

Adding alliteration.txt
```

and now we have a parent!

can use porcelain `git log` to see my history:

```
$ git log b440a10affe724badb4cf7cece898738ee2e3c18
commit b440a10affe724badb4cf7cece898738ee2e3c18
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 14:52:32 2018 +0000

    Adding alliteration.txt

commit 418816bdefa8889cf5e02e27b8f37157ff506bd1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 14:48:52 2018 +0000

    My first commit

```

---

## Exercises

1.  Take one of the trees you created in part 2, and create a commit object.

2.  List all the files in `.git/objects`, and check you can see your new commit.
    Inspect the object you've just created.

3.  Make an edit to one of your files, create a new tree, then create another commit from that tree, using the original commit as its parent.

Repeat step 3 a couple of itmes.
Create several commits that form a linear history -- each has the previous commit as its parent.

4.  Use a porcelain `git log` to see the history you've just created.

5.  you can create a commit with more than one parent, by supplying the `-p` flag more than once
    try creating a few commits like this
    this is a *merge commit*

## Useful commands

Don't peek!
Try the exercises on your own machine, then scroll past the picture of the folders to get the commentary

https://www.pexels.com/photo/depth-of-field-photography-of-brown-tree-logs-923167/

---

## Commentary

hopefully you're comfortbale creating commits

commits are also recursive, ish
point to trees and other commits
trees point to ohter ocmmits

<< diagram >>

merge commits give us non-linear history -- so we can consturct history in any order
always refer backwards

so now we can reconstruct the state of repo at any point in history, and we have the context to know why those points are significant

but we need to pass around SHA1 hashes, ick
for a more human-friendly interface, we'll need to look at creating *references*
