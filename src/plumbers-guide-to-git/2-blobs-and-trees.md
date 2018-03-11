---
layout: page
last_updated: 2018-03-11 14:27:32 +0000
title: Part 2: Blobs and trees
---

introductory waffle

in part 1, we saw how to store the contents of a single file -- but we don't know anything about filenames
in part 2, we'll see how to store filenames + directory layout

## Introduction

if you've used git before, know about "index" or "staging area"
temporary storage, place to put files we're working on

??? this needs a better explanation

save a file to the index:

```console
$ git update-index --add animals.txt
```

we can see a new index file in the .git directory:

```
$ ls .git
HEAD        description index       objects
config      hooks       info        refs
```

we can check it's in the index with a plumbing command:

```
$ git ls-files
animals.txt
```

or a porcelain `git status` works as well:

```console
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

	      new file:   animals.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	      alliteration.txt
	      basement.txt
	      basilisks.txt

```

index tracks contents + filenames
we can snapshot it as a *tree*

```console
$ git write-tree
05443337f802bfec039ec4121570d6c24ccb9eab
```

get back a hash -- this is another git object!

```console
$ find .git/objects -type f
.git/objects/05/443337f802bfec039ec4121570d6c24ccb9eab
.git/objects/a3/7f3f668f09c61b7c12e857328f587c311e5d1d
.git/objects/b1/3311e04762c322493e8562e6ce145a899ce570
```

and a different type of git object!

```
$ git cat-file -t a37f3f668f09c61b7c12e857328f587c311e5d1d
blob

alexwlchan at Alexs-MacBook-2.local in ~/workshop-repo
$ git cat-file -t 05443337f802bfec039ec4121570d6c24ccb9eab
tree
```

let's inspect it

```
$ git cat-file -p 05443337f802bfec039ec4121570d6c24ccb9eab
100644 blob a37f3f668f09c61b7c12e857328f587c311e5d1d	animals.txt
```

what's here?

100644 = file permissions
blob = type of object
a37f3f6 = hash of blob it refers to, the file we saved in previous part
animals.txt = name of file

let's create a more complex structure

```
$ mkdir b-words
$ mv basilisks.txt b-words/
$ mv basement.txt b-words/
```

then add those to the index:

```
$ git update-index --add b-words/basilisks.txt
$ git update-index --add b-words/basement.txt
```

write a tree:

```
$ git write-tree
c249dcb600ddbd958736177ba784798a6143a01e
```

and inspect it:

```
$ git cat-file -p c249dcb600ddbd958736177ba784798a6143a01e
100644 blob a37f3f668f09c61b7c12e857328f587c311e5d1d	animals.txt
040000 tree cf401e115bf7a440ef02216953803271580848dd	b-words
```

ooh, now we have two lines!
one is the blob we'd already saved
second is another tree object
let's look at that:

```
$ git cat-file -p cf401e115bf7a440ef02216953803271580848dd
100644 blob b13311e04762c322493e8562e6ce145a899ce570	basement.txt
100644 blob b13311e04762c322493e8562e6ce145a899ce570	basilisks.txt
```

so a tree can refer to blobs or to trees

let's put these new concepts into practice!

---

## Exercises

1.  Take a file you created in part 1, and add it to the index.

2.  Check that you can see an `index` file in your `.git` directory.

3.  Use a plumbing command to check that you've added it to the index.
    Then use a porcelain `git status` to double-check the result.

4.  Create a tree from the current index.

5.  Look in `.git/objects`.
    Can you see the tree you just created?

6.  Use a Git plumbing command to inspect the tree.
    Make sure you understand what it means.

Create some new files, and add them to your tree as well, repeating steps 1--6.
Make sure you're comfortable creating trees.

7.  Now make an edit to an existing file, and add the new version of that file to a tree.
    Use a plumbing command to inspect the tree.

    *What do you expect to see?*

8.  Create a subdirectory of your main directory, and create some files inside that folder.
    Add those files to a tree, and inspect the contents of that tree as well.

## Useful commands

Don't peek!
Try the exercises on your own machine, then scroll past the picture of the folders to get the comment

https://www.pexels.com/photo/nature-red-forest-leaves-33109/

---

## Commentary

will notice update-index creates object for you
don't need to use hash-object -w

trees are recursive -- tree in b-words folder doesn't know anything about fiels above it
recursive diagram -- trees point to blobs or other trees, and so on down

a tree has enough info to completely reconstruct state of repo
we know filenames, and pointer to blob tells us what the contents of that file should be

<< diagram >>

by creating trees, we can take snapshots of a repo
but we have no context.
why is a partiuclar tree special?

to gove them context, we need to work with *commits*
