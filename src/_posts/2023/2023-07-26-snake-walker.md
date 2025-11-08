---
layout: post
date: 2023-07-26 16:07:14 +0000
title: My Python snippet for walking a file tree
summary: A function to find all the files in a directory is one of my most-used snippets.
tags:
  - python
colors:
  index_dark:  "#7e9327"
  index_light: "#4f5f10"
---

{% comment %}
Cover image from https://www.pexels.com/photo/photo-of-pathway-surrounded-by-fir-trees-1578750/
{% endcomment %}

I write a lot of one-use Python scripts for quick analysis or cleaning something up on my disk, and they often involve iterating over a folder full of files.
The key function for doing this is [`os.walk`][os.walk] in the standard library, but it's not quite what I want, so I have a wrapper function I use instead:

{% code lang="python" names="0:os 1:get_file_paths_under 2:root 3:suffix 10:dirpath 12:filenames 16:f 18:p" %}
import os


def get_file_paths_under(root=".", *, suffix=""):
    """
    Generates the absolute paths to every matching file under ``root``.
    """
    if not os.path.isdir(root):
        raise ValueError(f"Cannot find files under non-existent directory: {root!r}")

    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            p = os.path.join(dirpath, f)

            if os.path.isfile(p) and f.lower().endswith(suffix):
                yield p


for path in get_file_paths_under():
    ...
{% endcode %}

This function gives me a couple of things over just using `os.walk`: it gives me a single iterator I can loop over, and it constructs the absolute path for me.
The ability to filter by suffix is useful too; it gives me a quick way to filter my search.
I use this when I'm working in a folder tree with lots of different file types.

{% code lang="python" names="0:path 2:txt_path" %}
for path in get_file_paths_under("notes"):
    ...

for txt_path in get_file_paths_under("notes", suffix=".txt"):
    ...
{% endcode %}

The body of the function isn't especially complicated; the only vaguely interesting bit is the `ValueError`.
it's to help catch silly mistakes when I accidentally pass the name of a file as the input -- if you try to `os.walk` over a file, you get an empty list of results, which can be a bit confusing.
(I'm sure there's a good reason, even if I don't know what it is.)

An experienced Python programmer could probably write this from scratch in a few minutes, but I use it so often that I like to have it saved.
TextExpander inserts this snippet whenever I type `py!pth`, including both the function and the `for` loop.
I save a few minutes, and I get a version of the function that I know doesn't have any weird edge cases or silly mistakes.

[os.walk]: https://docs.python.org/3/library/os.html#os.walk
