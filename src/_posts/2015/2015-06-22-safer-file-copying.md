---
date: 2015-06-22 23:20:00 +0000
layout: post
summary: A Python script for non-destructive file copying/moving.
tags: python
title: Safer file copying in Python
---

Using scripting and the command line can be a two-edged sword. They're very powerful tools, but they make it easy to shoot yourself in the foot. They assume that you know what you're doing, even if it might be dangerous.

An example I often run in to is moving or copying files. If you try to copy over an existing file, these tools will often scribble over the old file without any warning. For example, here's [the description](https://docs.python.org/3.5/library/shutil.html#shutil.copyfile) for `shutil.copyfile`:

> <code>shutil.<strong>copyfile</strong>(<em>src</em>, <em>dst</em>, *, <em>follow_symlinks=True</em>)</code>

> Copy the contents of the file named *src* to a file named *dst* and return *dst*. […] If *dst* already exists, it will be replaced.

The user is responsible for checking that the command won't be destructive, not the utility.

Modern GUIs are a bit friendlier. For example, in the OS X Finder, if you try to copy over an existing file, you get this warning:

> An item named "myfile.txt" already exists in this location. Do you want to replace it with the one you're moving?
>
> Keep Both / Stop / Replace

If you choose "Keep Both", then the Finder leaves the original file intact, and picks a new name for your copy. (In this case, it would use `myfile 2.txt`, `myfile 3.txt`, and so on.) I use this option when I want to be cautious. When I'm working with something precious, like my photo collection, I'd rather create too many copies than risk accidentally deleting something.

I wanted to replicate that functionality in Python, as a drop-in for the `copyfile()` and `move()` methods of the [*shutil* module](https://docs.python.org/3.5/library/shutil.html). I couldn't find existing code to do this, so I wrote my own script instead.

<!-- summary -->

I came up with a few rules for my "safe"[^1] move/copy function:

*   **It should never affect an existing file.** If I try to copy a file to a location, and there's already something there, then the pre-existing file will be untouched.
*   **Exact filenames aren't important.** The Finder will append a number to a filename until it finds one that isn't taken; my function should do broadly the same.
*   **Copying should be idempotent.** If I try to copy the same file lots of times, I shouldn't create more copies.

    This is an enhancement over "Keep Both" in the Finder. If you try to copy the same file repeatedly and use "Keep Both", Finder will create multiple copies. That's not so bad (better too many than too few copies), but it would be nice to avoid that.

I've uploaded my script [as a Gist](https://gist.github.com/alexwlchan/c2adbb8ee782f460e5ec). It provides two functions: `move()` and `copyfile()`, which mimic the shutil equivalents and return the name of the actual destination.

Here's how I import it:

```python
try:
    from safeutil import move, copyfile
except ImportError:
    from shutil import move, copyfile
```

so if I try to run a script that imports this module on a system where it isn't installed, things will still continue to work (albeit a little less safe).

I asked for advice on an early version on [the Code Review Stack Exchange](http://codereview.stackexchange.com/q/89985/36525). My thanks to 200_success and Günther Noack for their useful feedback.

I've been using these functions in a number of different places. I'll try to write up a few of them in the coming weeks.


[^1]: I use the word "safe" because this function is totally non-destructive. It's also partially inspired by Donald Knuth, who coined the term ["literate programming"](http://www.literateprogramming.com/knuthweb.pdf) to make people feel bad about writing non-literate, or "illiterate" programs. Likewise, why would I want to use an "unsafe" function when I have a safe alternative?
