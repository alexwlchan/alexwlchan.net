---
layout: post
title: Why is os.sep insufficient for path operations?
summary: Digging into a throwaway comment in the Python documentation.
tags: python
---

I was reading [the documentation for Python's os module][docs] recently, and a sentence caught my eye:

<style>
  dl code {
    background: none;
  }
</style>

<blockquote>
  <dl>
    <dt><code>os.<strong>sep</strong></code></dt>
    <dd>
      The character used by the operating system to separate pathname components.
      This is <code>'/'</code> for POSIX and <code>'\\\\'</code> for Windows. Note that knowing this is not sufficient to be able to parse or concatenate pathnames — use <code>os.path.split()</code> and <code>os.path.join()</code> — but it is occasionally useful.
    </dd>
  </dl>
</blockquote>

I was naturally curious: when is `os.sep` not sufficient?

I decided to have a peek at the implementation of `os.path.split()` and `os.path.join()` – how are they more complicated than a simple `str.split()` and `str.join()`?

First, it's worth understanding how `os.path` works.

Because paths behave differently on different platforms, there are multiple modules for manipulating paths in the standard library – `posixpath` for UNIX-style paths, and `ntpath` for Windows-style paths.
Older versions of Python included modules like [`macpath`][macpath] for old MacOS-style paths and `os2emxpath` for OS/2 EMX paths.

When you use `os.path`, it selects the appropriate module for your platform.
Using `os.path` means your code should do the right thing, even if the code is run on a different platform to where you wrote it.
If you do want a specific style of path, you can import the specific module, which is what I'll do in my examples.

I looked at four files to find out what these functions do:

-   [cpython/Lib/ntpath.py](https://github.com/python/cpython/blob/f4c03484da59049eb62a9bf7777b963e2267d187/Lib/ntpath.py#L76-L195)
-   [cpython/Lib/posixpath.py](https://github.com/python/cpython/blob/f4c03484da59049eb62a9bf7777b963e2267d187/Lib/posixpath.py#L67-L109)
-   [cpython/Lib/test/test_ntpath.py](https://github.com/python/cpython/blob/f4c03484da59049eb62a9bf7777b963e2267d187/Lib/test/test_ntpath.py#L121-L210)
-   [cpython/Lib/test/test_posixpath.py](https://github.com/python/cpython/blob/f4c03484da59049eb62a9bf7777b963e2267d187/Lib/test/test_posixpath.py#L49-L74)

Even without reading the code, the length of the functions and their tests give a clue as to how complicated they are.

Here are a few of my favourite examples where paths are trickier than simple strings:

*   The `os.path.split()` function can recognise that multiple path separators are equivalent to a single separator:

    ```pycon
    >>> posixpath.split('/Users/alexwlchan///blog.txt')
    ('/Users/alexwlchan', 'blog.txt')

    >>> ntpath.split('c:\\\\Users\\alexwlchan\\\\\\blog.txt')
    ('c:\\\\Users\\alexwlchan', 'blog.txt')
    ```

*   The `os.path.join()` function only inserts a path separator as needed, and skips it if it already sees one:

    ```pycon
    >>> posixpath.join('/x', 'y', 'z')
    '/x/y/z'

    >>> posixpath.join('/x', 'y/', 'z')
    '/x/y/z'

    >>> ntpath.join('c:\\x', 'y', 'z')
    'c:\\x\\y\\z'

    >>> ntpath.join('c:\\x', 'y\\', 'z')
    'c:\\x\\y\\z'
    ```

*   Both `os.path.split()` and `os.path.join()` can cope with paths on Windows, which can use backslash and forward slash:

    ```pycon
    >>> ntpath.join('/a/b', 'x/y')
    '/a/b\\x/y'

    >>> ntpath.join('/a/b/', 'x/y')
    '/a/b/x/y'

    >>> ntpath.split('/a/b\\x/y')
    ('/a/b\\x', 'y')

    >>> ntpath.split('/a/b/x/y')
    ('/a/b/x', 'y')
    ```

There's also a lot of code for Windows drive letters and [UNC paths][unc], two concepts I'm totally unfamiliar with.

I don't pretend to have a complete understanding of how paths work after this quick skim – but I did enjoy digging into it, and now I feel I have a better understanding of why I shouldn't use `os.sep` to do my own path operations.

[docs]: https://docs.python.org/3/library/os.html#os.sep
[macpath]: https://docs.python.org/release/2.7/library/macpath.html#module-macpath
[unc]: https://en.wikipedia.org/wiki/Path_(computing)#Universal_Naming_Convention
