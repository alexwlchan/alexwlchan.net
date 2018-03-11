---
layout: page
last_updated: 2018-03-11 14:27:32 +0000
title: "Part 1: The Git object store"
meta:
  - Part of <a href="/plumbers-guide-to-git/">A Plumber&rsquo;s Guide to Git</a>
---

We'll start by storing the contents of a single file in Git.

Read the theory, make sure you understand the examples, then try the exercises.
At the end of part 1, you should be able to store and retrieve individual files from Git.

<div class="post__separator" aria-hidden="true">&#9675; &#8592; &#9675; &#8592; &#9675;</div>

## Initialising a new Git repo

Let's start by creating a new directory:

```console
$ mkdir plumbing-repo
$ cd plumbing-repo
```

Then we can create a new Git repository with the [git-init command][init]:

```console
$ git init
Initialized empty Git repository in ~/plumbing-repo/.git/
```

This command creates the `.git` directory, which is where Git stores all of its information.
If you delete everything except this directory, you can still rebuild your entire repository -- as we'll see in the rest of the workshop.

The command also creates a few other empty directories for us.
If you've never looked inside the `.git` directory before, let's start now:

```console
$ ls .git
HEAD        description info        refs
config      hooks       objects
```

Here's what we have:

-   The `HEAD` file tells Git which branch we're working on -- we'll skip it for now, and come back to it in [part 4 "refs and branches"][part4].

-   The `config` file contains repo-specific configuration.
    We're not using it in this workshop.

-   The `description` file is only used by the GitWeb program -- it can be ignored.

-   The `hooks` directory is used to store scripts that fire on certain events -- for example, running a linter before you commit.
    We don't cover it in this workshop, but it can be very useful!
    See the [Git docs][hooks] for more information.

-   The `info` directory has a single file, `exclude`, which contains a list of per-repo ignores.
    Like a gitignore file, but it doesn't need to be checked in.
    We won't use it in this workshop.

-   The `objects` directory should be empty (aside from two more empty directories) -- but we're about to see what it holds.

-   The `refs` directory is also empty -- we'll see it again in [part 4][part4].

[init]: https://git-scm.com/docs/git-init
[part4]: /plumbers-guide-to-git/4-refs-and-branches/
[hooks]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks


---
---
---

Let's start by creating a new directory, then initialising a Git repository:

```console
$ mkdir workshop-repo
$ cd workshop-repo
$ git init
Initialized empty Git repository in ~/workshop-repo/.git/
```

The `git init` command creates the `.git` directory, which is where Git stores information.

create a few empty directories for us, just a convenient werapper

If you've never looked inside the `.git` directory, let's do it now:



We have three files (`HEAD`, `config` and `description`) and four directories.

The `HEAD` file tells Git which branch we're working on -- we'll come back to it in [part 4][part4].
what are config, description?
hooks -- useful but not today
info -- link to previous
objects -- look at next (check is empty)
refs -- see part 4

so we know where git will store info
let's try it!

create out first file, and save it

```console
$ echo "An awesome aardvark admires the Alps" > animals.txt
$ git hash-object -w animals.txt
a37f3f668f09c61b7c12e857328f587c311e5d1d
```

this is our first *plumbing* command
hash-object saves an object to the git db
SHA1 hash

if we look in .git/objects, we see it's created:

```console
$ find .git/objects -type f
.git/objects/a3/7f3f668f09c61b7c12e857328f587c311e5d1d
```

look -- it's the hash we just got back!

(two char prefix to avoid too many files in same dir)

this is a binary file that holds the text we just saved

"content-addressable filesystem"
imagine it like a python dictionary
git has chosen the name of that binary file based on the contents of our original text file

if we save the file a second time, because the contents haven't changed, nothing happens:

```console
$ git hash-object -w animals.txt
a37f3f668f09c61b7c12e857328f587c311e5d1d

$ find .git/objects -type f
.git/objects/a3/7f3f668f09c61b7c12e857328f587c311e5d1d
```

we can retrieve it like so:

```
$ git cat-file -p a37f3f668f09c61b7c12e857328f587c311e5d1d
An awesome aardvark admires the Alps
```

and if we delete our file, we can use this to restore it:

```console
$ rm animals.txt
$ git cat-file -p a37f3f668f09c61b7c12e857328f587c311e5d1d > animals.txt
$ cat animals.txt
An awesome aardvark admires the Alps
```



---

## Exercises

1.  Create a new directory, and initialise Git.

2.  Look inside the `.git` folder.
    Make sure you understand what's in there.

3.  Using a text editor, create a file and write some text.

4.  Use a Git plumbing command to save the contents of your file to the Git object store.
    Check you can see the new object in `.git/objects`.

5.  Use a Git plumbing command to inspect the object in the database.

Repeat steps 3--5 a couple of times, so that you're comfortable saving files to the Git object store.

6.  Make an edit to your file, then save the new version to the Git object store.
    What do you see in `.git/objects`?

    *Before you look: what do you expect to see?*

7.  Delete the file, then recreate it from the Git object store.

8.  What if you save two files with the same contents, but different filenames?
    What do you see in `.git/objects`?

    *What do you expect to see?*

## Useful commands

Don't peek!
Try the exercises on your own machine, then scroll past the picture of the folders to get the commentary

https://www.pexels.com/photo/multi-colored-folders-piled-up-159519/

---

## Commentary

hopefully now you're comfortable saving individual files

you might have noticed git doesn't store any info about *filenames*

so if you want to recreate a file, you could get it back under a different name:

```
$ git cat-file -p a37f3f668f09c61b7c12e857328f587c311e5d1d > alliteration.txt
```

If you create two files with the same contents, they get the same hash:

```
$ echo "Big blue basilisks bawl in the basement" > basilisks.txt
$ echo "Big blue basilisks bawl in the basement" > basement.txt
$ git hash-object -w basilisks.txt
b13311e04762c322493e8562e6ce145a899ce570
$ git hash-object -w basement.txt
b13311e04762c322493e8562e6ce145a899ce570
```

so we're not keeping enough information to get filenames, just snapshots of an individual file's contents

for filenames, we need to introduce the concept of *trees*
