---
layout: post
title: The rough edges of filecmp
summary: The filecmp module has a confusing API, and it just caught me out.
category: Programming and code
---

I've been cleaning up some old files recently, and as part of that I'm using the [filecmp module](https://docs.python.org/3/library/filecmp.html) to clean up duplicates.
It exposes one function I'm interested in: `filecmp.cmp(f1, f2)`, which tells you if `f1` and `f2` are the same.
It's a really simple API, and I've been using it this way for years.

As I was running my scripts, I happened to spot something that looked weird.
The module was telling me two files were the same, even though they contained different data:

```python
>>> path1 = "Semaphore_Golf.svg"
>>> path2 = "Semaphore_Lima.svg"

>>> filecmp.cmp(path1, path2)
True

>>> open(path1, "rb").read() == open(path2, "rb").read()
False
```

I went to re-read the docs, and it turns out I'd forgotten a detail -- by default, it only compares the os.stat() signature of the two files.
If that matches, it tells you the files are the same, regardless of the contents.
If you want an actual byte-for-byte comparison, pass `shallow=True`:

```python
>>> filecmp.cmp(path1, path2, shallow=False)
False
```

I've been making this mistake for years, because the API is so simple I never really needed to check the docs.
Nobody's ever spotted it in a code review, and I've seen it in plenty of other code without an explicit `shallow` flag.

Initially this struck me as a dangerous default -- if you use filecmp without paying close attention, you might not realise it's not doing a byte-for-byte comparison.
If you get a positive result and delete the second file as a duplicate, you've just lost data.
Oops.

But the more I read about it, the more I think it's a bad API design.
I went to look in the Python bug tracker, and I found multiple bugs from people complaining that the behaviour of the module was confusing or misleading.
The problem is that "the same file" could mean at least three different things:

*   *Do the files have the same os.stat() signature?*

    In filecmp, it's comparing the size, modified time, and [the mode](https://docs.python.org/3/library/stat.html#stat.S_IFMT)

*   *Do the files have the same byte-for-byte contents?*

    This is what you get by passing shallow=True.

*   *Are the files the same underlying file on disk, modulo hard links?*
    (h/t [@kapellosaur](https://twitter.com/kapellosaur))

    Apparently this is handled by the [os.path.samefile](https://docs.python.org/3/library/os.path.html#os.path.samefile) function, although I've never used it myself.

You want different notions of "same" in different contexts, and having a binary flag to choose the behaviour is pretty unclear.
Even if you do pass an explicit `shallow` flag, it's not so clear which version you're using.

A clearer API would be something like:

```python
def cmp_contents(f1, f2):
    """
    Returns True if f1 and f2 contain the same bytes, False if not.
    """


def cmp_stat(f1, f2):
    """
    Returns True if f1 and f2 have the same os.stat() signature, False if not.
    """


def cmp_same_file(f1, f2):
    """
    Returns True if f1 and f2 point to the same file on disk, False if not.
    """
```

The names make it clearer which version of sameness you're using, and because they each return a boolean, you can combine conditions with logical operators.
