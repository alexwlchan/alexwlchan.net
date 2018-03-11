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

<div class="post__separator" aria-hidden="true">&#9675; &#8592;&#9675; &#8592;&#9675;</div>

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

So now we have an empty repository, and we've had a look inside the `.git` directory -- let's try to store something!

[init]: https://git-scm.com/docs/git-init
[part4]: /plumbers-guide-to-git/4-refs-and-branches/
[hooks]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks

## Storing individual files with "hash-object"

Let's create our first file, then save it to the Git object store:

```console
$ echo "An awesome aardvark admires the Alps" > animals.txt
$ git hash-object -w animals.txt
a37f3f668f09c61b7c12e857328f587c311e5d1d
```

This is our first example of a plumbing command.
The [hash-object command][hashobj] takes a path to a file, reads its contents, and saves the contents of the file to the Git object store.
It's returned a hex string -- the ID of the object it's just created.

If we look in `.git/objects`, we can see something with the same name:

```console
$ find .git/objects -type f
.git/objects/a3/7f3f668f09c61b7c12e857328f587c311e5d1d
```

We've created our first object!

This object is a binary file that holds the text we just saved.
(You'll see the first two characters create a directory.
A typical repo has thousands of objects, so Git breaks up `objects` into subdirectories to avoid any one directory becoming too large.)

The object ID is chosen based on the contents of the object -- specifically, prepend a short header to our file, and take the SHA1 hash.
This is how Git stores all of its objects -- the content of an object determines its ID.
The technical term for this is a *content-addressable filesystem*.

This means that if we try to write the file a second time, because the contents haven't changed, nothing changes:

```console
$ git hash-object -w animals.txt
a37f3f668f09c61b7c12e857328f587c311e5d1d

$ find .git/objects -type f
.git/objects/a3/7f3f668f09c61b7c12e857328f587c311e5d1d
```

We have the same set of objects as before.

[hashobj]: https://git-scm.com/docs/git-hash-object

## Retrieving objects with "cat-file"

So now we've saved an object, we can use a second plumbing command to retrieve it:

```console
$ git cat-file -p a37f3f668f09c61b7c12e857328f587c311e5d1d
An awesome aardvark admires the Alps
```

The [cat-file command][catfile] is used to inspect objects stored in Git.
The "-p" flag means "pretty" -- it pretty-prints the contents of the object.

With this command, we can restore our file even if we delete it -- because the object is kept safe in the `.git` directory:

```console
$ rm animals.txt
$ git cat-file -p a37f3f668f09c61b7c12e857328f587c311e5d1d > animals.txt
$ cat animals.txt
An awesome aardvark admires the Alps
```

[catfile]: https://git-scm.com/docs/git-cat-file

<div class="post__separator" aria-hidden="true">&#9675;&#8594; &#9675;&#8594; &#9675;</div>

## Exercises

These are some exercises to get you used to the idea of storing and retrieving files from the Git object store:

1.  Create a new directory, and initialise Git.
2.  Look inside the `.git` folder.
    Make sure you understand what it contains.
3.  Using a text editor, create a file and write some text.
4.  Use a Git plumbing command to save the contents of your file to the Git object store.
    Check you can see the new object in `.git/objects`.
5.  Use a Git plumbing command to inspect the object in the database.

Repeat steps 3--5 a couple of times.

<ol start="6">
  <li>
    Make an edit to your file, then save the new version to the Git object store.
    What do you see in <code>.git/objects</code>?
    <em>Before you look: what do you expect to see?</em>
  </li>
  <li>
    Delete a file, then recreate it from the Git object store.
  </li>
  <li>
    What if you save two files with the same contents, but different filenames?
    What do you see in <code>.git/objects</code>?
    <em>What do you expect to see?</em>
  </li>
</ol>

<div class="post__separator" aria-hidden="true">&#9675; &#8592;&#9675;&#8594; &#9675;</div>

## Notes

Hopefully now you're comfortable saving individual files.

You might have noticed that Git doesn't store any information about *filenames*.

You can restore an object to a file with a different name to the original:

```console
$ git cat-file -p a37f3f668f09c61b7c12e857328f587c311e5d1d > alliteration.txt
```

When you edit a file, then save the edited file in Git, you get an entirely new object.

```console
$ echo "Big blue basilisks bawl in the basement" > animals.txt

$ git hash-object -w animals.txt
b13311e04762c322493e8562e6ce145a899ce570

$ find .git/objects -type f
.git/objects/a3/7f3f668f09c61b7c12e857328f587c311e5d1d
.git/objects/b1/3311e04762c322493e8562e6ce145a899ce570
```

Whereas if you save two files with the same contents, they both get the same hash:

```console
$ echo "Clueless cuttlefish crowd the curious crab" > c_creatures.txt
$ cp c_creatures.txt sea_creatures.txt

$ git hash-object -w c_creatures.txt
ce289881a996b911f167be82c87cbfa5c6560653

$ git hash-object -w sea_creatures.txt
ce289881a996b911f167be82c87cbfa5c6560653
```

That's because we're only saving the *contents* of a file, and object IDs are determined entirely by their contents.
We haven't saved anything about the filenames or the directory structure of our repository.
For that, we need to learn about *trees*.
Onwards to [part 2][part2]!

[part2]: /plumbers-guide-to-git/2-blobs-and-trees/
