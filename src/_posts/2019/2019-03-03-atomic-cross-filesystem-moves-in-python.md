---
layout: post
date: 2019-03-03 23:48:31 +0000
title: Atomic, cross-filesystem moves in Python
summary: Explaining some code for moving files around in a way that's atomic and works across filesystem boundaries.
category: "Programming walkthroughs"
tags:
- python
---

If you want to move a file around in Python, the standard library gives you at least two options: [os.rename()](https://docs.python.org/3/library/os.html#os.rename) or [shutil.move()](https://docs.python.org/3/library/shutil.html#shutil.move).
Both of them work in certain circumstances, but they make different tradeoffs:

*   With os.rename(), you get [atomicity](https://en.wikipedia.org/wiki/Atomicity_(database_systems)) but you can't copy across filesystems.

    On some Unix systems, you get an error if you try to move a file to a different filesystem than the original -- for example, if you're moving a file from an external disk to your local drive.

*   With shutil.move(), you can copy across file systems, but there's no guarantee of atomicity.

    If the operation is interrupted halfway through, you could end up with a half-written file at the destination.

Sometimes you want both of those properties: you want to move across a filesystem boundary *and* have an atomic move.

For example: [Loris](https://github.com/loris-imageserver/loris), an image server.
When a user requests an image, we start by downloading it from the source to a temporary folder.
If the download succeeds, we move the saved image into another cache, and that known-good cache is used to serve the image to the user.
We want that move to be atomic -- so we won't serve a partial image from the cache -- and in some setups, the temporary download folder and the image cache are on different filesystems.
We need a move function that can be both atomic and work across filesystems.

I've had to write code for this a couple of times now, so I'm writing it up here both as a reminder to myself, and an instruction for other people in case it's useful.

## Writing the code

If we're copying within the same filesystem, os.rename() gives us everything we need.
Let's try that first, and only do something different if we get an error:

```python
import os


def safe_move(src, dst):
    try:
        os.rename(src, dst)
    except OSError:
        # do something else...
```

This except clause is quite broad -- it catches and retries *any* error thrown by os.rename().
There are lots of errors that have nothing to do with a cross-filesystem move -- for example, if the source file just doesn't exist!
We should only catch and retry the specific error that comes from copying across a filesystem boundary.

If you try it, this is the error you get:

```pycon
>>> import os
>>> os.rename("/mnt/semele/hello.txt", "/mnt/dionysus/hello.txt")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: [Errno 18] Cross-device link: '/mnt/semele/hello.txt' -> '/mnt/dionysus/hello.txt'
```

Error code 18 is what we want to retry -- this is a standard Linux error number meaning "invalid cross-device link".
We can use the [errno library](https://docs.python.org/3/library/errno.html) to get 18 as a named variable that's a little less of a magic number, like so:

```python
import errno


def safe_move(src, dst):
    try:
        os.rename(src, dst)
    except OSError as err:
        if err.errno == errno.EXDEV:
            # do something else...
        else:
            raise
```

So now we need to decide what "something else" looks like.

To get the file onto the same filesystem, we can use shutil.move() to put it in the same directory as the intended destination, but with a different filename.
As a first pass, we might try something like:

```python
import shutil


def safe_move(src, dst):
    ...
    # do something else
    tmp_dst = dst + ".tmp"
    shutil.copyfile(src, tmp_dst)
    os.rename(tmp_dst, dst)
    os.unlink(tmp_dst)
```

This could be okay in certain circumstances, but if you have multiple worker processes you could end up with a corrupted destination.
If you're running multiple processes, and they both try to copy to the temporary destination, you could get garbage data in that file.
One process might think it's completed the copy, then rename the file as the other process is still writing to it.

To avoid processes treading on each other's toes, add a unique ID to each copy -- that way they can't overlap.
Closer to:

```python
import uuid


def safe_move(src, dst):
    ...
    # do something else
    copy_id = uuid.uuid4()
    tmp_dst = "%s.%s.tmp" % (dst, copy_id)
    shutil.copyfile(src, tmp_dst)
    os.rename(tmp_dst, dst)
    os.unlink(tmp_dst)
```

This is an idea I originally got from a [Stack Overflow answer](https://stackoverflow.com/a/28090883/1558022) about lock-free copy algorithms.
This isn't quite the same problem as that question -- in particular, I don't care if the file already exists -- but the answer and the linked paper make interesting reading.

## Putting it all together

If you just want the code, here's the final version (with comments):

```python
import errno
import os
import shutil


def safe_move(src, dst):
    """Rename a file from ``src`` to ``dst``.

    *   Moves must be atomic.  ``shutil.move()`` is not atomic.
        Note that multiple threads may try to write to the cache at once,
        so atomicity is required to ensure the serving on one thread doesn't
        pick up a partially saved image from another thread.

    *   Moves must work across filesystems.  Often temp directories and the
        cache directories live on different filesystems.  ``os.rename()`` can
        throw errors if run across filesystems.

    So we try ``os.rename()``, but if we detect a cross-filesystem copy, we
    switch to ``shutil.move()`` with some wrappers to make it atomic.
    """
    try:
        os.rename(src, dst)
    except OSError as err:

        if err.errno == errno.EXDEV:
            # Generate a unique ID, and copy `<src>` to the target directory
            # with a temporary name `<dst>.<ID>.tmp`.  Because we're copying
            # across a filesystem boundary, this initial copy may not be
            # atomic.  We intersperse a random UUID so if different processes
            # are copying into `<dst>`, they don't overlap in their tmp copies.
            copy_id = uuid.uuid4()
            tmp_dst = "%s.%s.tmp" % (dst, copy_id)
            shutil.copyfile(src, tmp_dst)

            # Then do an atomic rename onto the new name, and clean up the
            # source image.
            os.rename(tmp_dst, dst)
            os.unlink(src)
        else:
            raise
```

I've been running code like this in production for over a year (as part of our Loris installation at Wellcome), and used it in a few other places with no issues.
