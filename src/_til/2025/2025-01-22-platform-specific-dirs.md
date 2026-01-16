---
layout: til
title: How to find platform-specific directories
date: 2025-01-22 10:37:05 +00:00
summary: |
  Two Python libraries for this task are appdirs and platformdirs, which tell you the location of the platform-specific cache directory and other similar directories.
tags:
  - python
---
I was writing a Python library that might need to cache some results.
On macOS, that sort of app or library-specific cache should be written to `~/Library/Caches`, but that path will be different on other operating systems.
I had a vague memory of a library that can knows what path to use on different platforms, and I wanted to write down what it was.

## appdirs

[appdirs](https://github.com/ActiveState/appdirs) is the library I was remembering.
It tells you the directory where you should store data, config, caches and logs.

Here's an example on my Mac:

```pycon
>>> from appdirs import *
>>> user_cache_dir(appname="My Great App", appauthor="Alex Chan")
'/Users/alexwlchan/Library/Caches/My Great App'
```

And the same code on my Debian web server:

```pycon
>>> from appdirs import *
>>> user_cache_dir(appname="My Great App", appauthor="Alex Chan")
'/home/alexwlchan/.cache/My Great App'
```

Neat!

It distinguishes between the "user" and the "site" directories -- where the latter seems to mean "all uses of the system".
In macOS terms, it's the difference between `~/Library` and `/Library`.

Although the project is "officially deprecated", it still seems to work -- and it's delivered as a single file, which means you could copy it into your project without using pip.

## platformdirs

[platformdirs](https://github.com/tox-dev/platformdirs) is the successor to appdirs.
It's actively maintained, and knows about a wider number of directories -- for example, a user's desktop and downloads folder.

Here's an example on my Mac:

```pycon
>>> from platformdirs import *
>>> user_downloads_dir()
'/Users/alexwlchan/Downloads'
```

And my Debian web server:

```pycon
>>> from platformdirs import *
>>> user_downloads_dir()
'/home/alexwlchan/Downloads'
```

It also has all the functions provided by appdirs.

## Which to choose?

I didn't implement the caching feature today, so I didn't end up choosing a library.

I find it slightly annoying that both libraries return `str`, because I'm trying to move all of my code [to use `pathlib.Path`][pathlib].
I could obviously wrap the results, but I'd rather the library did it for me.

I like the simplicity of appdirs, because I don't think I need all of the directories offered by platformdirs -- but that's the only one that's actively maintained.

If I need this sort of functionality in the future, I might look at both of these libraries, then replicate the small amount I need in a file in my project -- and convert it to `pathlib.Path` while I'm there.
I could bring in one function rather than an entire library.
(And understanding this code would allow me to port it to other languages if necessary.)

[pathlib]: https://treyhunner.com/2018/12/why-you-should-be-using-pathlib/
