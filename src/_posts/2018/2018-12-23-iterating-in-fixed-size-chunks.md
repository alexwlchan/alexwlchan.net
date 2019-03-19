---
layout: post
date: 2018-12-23 22:39:38 +0000
title: Iterating in fixed-size chunks in Python
summary: A snippet for iterating over an arbitrary iterable in chunks, and returning a smaller chunk if the boundaries don't line up.
tags: python
category: Programming and code
theme:
  minipost: true
---

Here's a fairly common problem I have: I have an iterable, and I want to go through it in "chunks".
Rather than looking at every item of the sequence one-by-one, I want to process multiple elements at once.

For example, when I'm using the [bulk APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html) in Elasticsearch, I can index many document with a single API call, which is more efficient than making a new API call for every document.

Here's the sort of output I want:

```python
for c in chunked_iterable(range(14), size=4):
    print(c)

# (0, 1, 2, 3)
# (4, 5, 6, 7)
# (8, 9, 10, 11)
# (12, 13)
```

I have two requirements which are often missed in Stack Overflow answers or other snippets I've found:

*   It has to work with generators, where you don't know the length upfront, and you can't slice to a particular point in the generator.
    e.g. iterating over files in a directory

*   I don't want "filler" values at the end -- if it doesn't line up neatly on a boundary, I'd rather have a truncated chunk than extra values.

So to save me having to find it again, this is what I usually use:

```python
import itertools


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk
```

Most of the heavy lifting is done by [itertools.islice()](https://docs.python.org/3/library/itertools.html#itertools.islice); I call that repeatedly until it returns an empty sequence.
The itertools module has lots of useful functions for this sort of thing.

The `it = iter(iterable)` line may be non-obvious -- this ensures that the value `it` is using the same iterator throughout.
If you pass certain fixed iterables to islice(), it creates a new iterator each time -- and then you only ever get the first handful of elements.

For example, trying to call `chunked_iterable([1, 2, 3, 4, 5], size=2)` without this line would emit `[1, 2]` forever.

I think it's the difference between a *container* (for which `iter(…)` returns a new object each time) and an *iterator* (for which `iter(…)` returns itself).
I forget the exact details, but I remember first reading about this in Brett Slatkin's book [*Effective Python*](https://effectivepython.com).
