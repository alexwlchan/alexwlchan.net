---
layout: post
date: 2025-08-03 14:49:06 +00:00
title: Create space-saving clones on macOS with Python
summary: You can shell out to `cp -c` using `subprocess`, or you can make a `clonefile()` syscall using the `ctypes` library.
tags:
  - python
  - macos
---
{% comment %}
  Card image: https://pixabay.com/photos/stormtrooper-star-wars-lego-storm-1343772/
{% endcomment %}

The standard Mac filesystem, <a href="https://en.wikipedia.org/wiki/Apple_File_System"><abbr title="Apple File System">APFS</abbr></a>, has a feature called *space-saving clones*.
This allows you to create multiple copies of a file without using additional disk space -- the filesystem only stores a single copy of the data.

Although cloned files share data, they're independent -- you can edit one copy without affecting the other (unlike [symlinks] or [hard links]).
APFS uses a technique called [copy-on-write] to store the data efficiently on disk -- the cloned files continue to share any pieces they have in common.

Cloning files is both faster and uses less disk space than copying.
If you're working with large files -- like photos, videos, or datasets -- space-saving clones can be a big win.

Several filesystems support cloning, but in this post, I'm focusing on macOS and APFS.

For a recent project, I wanted to clone files using Python.
There's [an open ticket][cpython81338] to support file cloning in the Python standard library.
In Python 3.14, there's [a new `Path.copy()` function][cpython119058] which adds support for cloning on Linux -- but there's nothing yet for macOS.

In this post, I'll show you two ways to clone files in APFS using Python.

[APFS]: https://en.wikipedia.org/wiki/Apple_File_System
[ctypes]: https://docs.python.org/3/library/ctypes.html
[hard links]: https://en.wikipedia.org/wiki/Hard_link
[symlinks]: https://en.wikipedia.org/wiki/Symbolic_link
[cpython81338]: https://github.com/python/cpython/issues/81338
[cpython119058]: https://github.com/python/cpython/pull/119058
[copy-on-write]: https://en.wikipedia.org/wiki/Copy-on-write

{% table_of_contents %}


---


<h2 id="benefits">What are the benefits of cloning?</h2>

There are two main benefits to using clones rather than copies.

<h3 id="benefits-space">Cloning files uses less disk space than copying</h3>

Because the filesystem only has to keep one copy of the data, cloning a file doesn't use more space on disk.
We can see this with an experiment.
Let's start by creating a random file with 1GB of data, and checking our free disk size:

```console
$ dd if=/dev/urandom of=1GB.bin bs=64M count=16
16+0 records in
16+0 records out
1073741824 bytes transferred in 2.113280 secs (508092550 bytes/sec)

$ df -h -I /
Filesystem        Size    Used   Avail Capacity  Mounted on
/dev/disk3s1s1   460Gi    14Gi    43Gi    25%    /
```

My disk currently has 43GB available.

Let's copy the file, and check the free disk space after it's done.
Notice that it decreases to 42GB, because the filesystem is now storing a second copy of this 1GB file:

```console
$ # Copying
$ cp 1GB.bin copy.bin

$ df -h -I /
Filesystem        Size    Used   Avail Capacity  Mounted on
/dev/disk3s1s1   460Gi    14Gi    42Gi    25%    /
```

Now let's clone the file by passing the `-c` flag to `cp`.
Notice that the free disk space stays the same, because the filesystem is just keeping a single copy of the data between the original and the clone:

```console
$ # Cloning
$ cp -c 1GB.bin clone.bin

$ df -h -I /
Filesystem        Size    Used   Avail Capacity  Mounted on
/dev/disk3s1s1   460Gi    14Gi    42Gi    25%    /
```

<h3 id="benefits-speed">Cloning files is faster than copying</h3>

When you clone a file, the filesystem only has to write a small amount of metadata about the new clone.
When you copy a file,it needs to write all the bytes of the entire file.
This means that cloning a file is much faster than copying, which we can see by timing the two approaches:

```console
$ # Copying
$ time cp 1GB.bin copy.bin
Executed in  260.07 millis

$ # Cloning
$ time cp -c 1GB.bin clone.bin
Executed in    6.90 millis
```

This 43× difference is with my Mac's internal SSD.
In my experience, the speed difference is even more pronounced on slower disks, like external hard drives.





<h2 id="howto">How do you clone files on macOS?</h2>

<h3 id="howto-finder">Using the “Duplicate” command in Finder</h3>

If you use the Duplicate command in Finder (File > Duplicate or ⌘D), it clones the file.

<h3 id="howto-command-line">Using <code>cp -c</code> on the command line</h3>

If you use the [`cp` (copy) command][cp] with the `-c` flag, and it's possible to clone the file, you get a clone rather than a copy.
If it's not possible to clone the file -- for example, if you're on a non-APFS volume that doesn't support cloning -- you get a regular copy.

Here's what that looks like:

```console
$ cp -c src.txt dst.txt
```

[cp]: https://alexwlchan.net/man/man1/cp.html

<h3 id="howto-c-function">Using the <code>clonefile()</code> function</h3>

There's a macOS syscall [`clonefile()`][clonefile2] which creates space-saving clones.
It was introduced alongside APFS.

Syscalls are quite low level, and they're how programs are meant to interact with the operating system.
I don't think I've ever made a syscall directly -- I've used wrappers like the Python `os` module, which make syscalls on my behalf, but I've never written my own code to call them.

Here's a rudimentary C program that uses `clonefile()` to clone a file:

{% code lang="c" names="0:main 1:src 2:dst 3:flags" %}
#include <stdio.h>
#include <stdlib.h>
#include <sys/clonefile.h>

int main(void) {
    const char *src = "1GB.bin";
    const char *dst = "clone.bin";

    /* clonefile(2) supports several options related to symlinks and
     * ownership information, but for this example we'll just use
     * the default behaviour */
    const int flags = 0;

    if (clonefile(src, dst, flags) != 0) {
        perror("clonefile failed");
        return EXIT_FAILURE;
    }

    printf("clonefile succeeded: %s ~> %s\n", src, dst);

    return EXIT_SUCCESS;
}
{% endcode %}

You can compile and run this program like so:

```console?prompt=$
$ gcc clone.c

$ ./a.out
clonefile succeeded: 1GB.bin ~> clone.bin

$ ./a.out
clonefile failed: File exists
```

But I don't use C in any of my projects -- can I call this function from Python instead?

[clonefile2]: https://alexwlchan.net/man/man2/clonefile.html





<h2 id="cloning-in-python">How do you clone files with Python?</h2>

<h3 id="python-subprocess">Shelling out to <code>cp -c</code> using <code>subprocess</code></h3>

The easiest way to clone a file in Python is by shelling out to `cp -c` with the [`subprocess` module][subprocess].
Here's a short example:

{% code lang="python" %}
import subprocess

# Adding the `-c` flag means the file is cloned rather than copied,
# if possible.  See the man page for `cp`.
subprocess.check_call(["cp", "-c", "1GB.bin", "clone.bin"])
{% endcode %}

I think this snippet is pretty simple, and a new reader could understand what it's doing.
If they're unfamiliar with file cloning on APFS, they might not immediately understand why this is different from [`shutil.copyfile`][shutil.copyfile], but they could work it out quickly.

This approach gets all the nice behaviour of the `cp` command -- for example, if you try to clone on a volume that doesn't support cloning, it falls back to a regular file copy instead.
There's a bit of overhead from spawning an external process, but the overall impact is negligible (and easily offset by the speed increase of cloning).

The problem with this approach is that error handling gets harder.
The `cp` command fails with exit code 1 for every error, so you need to parse the stderr to distinguish different errors, or implement your own error handling.

In my project, I wrapped this `cp` call in a function which had some additional checks to spot common types of error, and throw them as more specific exceptions.
Any remaining errors get thrown as a generic `subprocess.CalledProcessError`.
Here's an example:

{% code lang="python" names="3:clonefile 4:src 6:dst" %}
from pathlib import Path
import subprocess


def clonefile(src: Path, dst: Path):
    """Clone a file on macOS by using the `cp` command."""
    # Check a couple of common error cases so we can get nice exceptions,
    # rather than relying on the `subprocess.CalledProcessError` from `cp`.
    if not src.exists():
        raise FileNotFoundError(src)

    if not dst.parent.exists():
        raise FileNotFoundError(dst.parent)

    # Adding the `-c` flag means the file is cloned rather than copied,
    # if possible.  See the man page for `cp`.
    subprocess.check_call(["cp", "-c", str(src), str(dst)])

    assert dst.exists()
{% endcode %}

For me, this code strikes a nice balance between being readable and returning good errors.

[subprocess]: https://docs.python.org/3/library/subprocess.html
[shutil.copyfile]: https://docs.python.org/3/library/shutil.html#shutil.copyfile

<h3 id="python-ctypes">Calling the <code>clonefile()</code> function using <code>ctypes</code></h3>

What if we want detailed error codes, and we don't want the overhead of spawning an external process?
Although I know it's possible to make syscalls from Python using [the `ctypes` library][ctypes], I've never actually done it.
This is my chance to learn!

Following the documentation for `ctypes`, these are the steps:

1.  **Import `ctypes` and [load a dynamic link library][cdll].**
    This is the first thing we need to do -- in this case, we're loading the macOS link library that contains the `clonefile()` function.
    
    {% code lang="python" names="1:libSystem" %}
    import ctypes

    libSystem = ctypes.CDLL("libSystem.B.dylib")
    {% endcode %}

    I worked out that I need to load `libSystem.B.dylib` by looking at other examples of `ctypes` code on GitHub.
    I couldn't find an explanation of it in Apple's documentation.

    I later discovered that I can use [`otool`][otool] to see the shared libraries that a compiled executable is linking to.
    For example, I can see that `cp` is linking to the same `libSystem.B.dylib`:

    ```console
    $ otool -L /bin/cp
    /bin/cp:
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1351.0.0)
    ```

    This `CDLL()` call only works on macOS, which makes sense -- it's loading macOS libraries.
    If I run this code on my Debian web server, I get an error: *OSError: libSystem.B.dylib: cannot open shared object file: No such file or directory*.

2.  **Tell `ctypes` about the function signature.**
    If we look at the [man page for `clonefile()`][clonefile2], we see the signature of the C function:

    {% code lang="c" names="0:clonefile 1:src 2:dst 3:flags" %}
    int clonefile(const char * src, const char * dst, int flags);
    {% endcode %}

    We need to tell `ctypes` to find this function inside `libSystem.B.dylib`, then describe the arguments and return type of the function:

    {% code lang="python" names="0:clonefile" %}
    clonefile = libSystem.clonefile
    clonefile.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    clonefile.restype = ctypes.c_int
    {% endcode %}

    Although `ctypes` can call C functions if you don't describe the signature, it's a good practice and gives you some safety rails.

    For example, now `ctypes` knows that the `clonefile()` function takes three arguments.
    If I try to call the function with one or two arguments, I get a `TypeError`.
    If I didn't specify the signature, I could call it with any number of arguments, but it might behave in weird or unexpected ways.

3.  **Define the inputs for the function.**
    This function needs three arguments.
  
    In the original C function, `src` and `dst` are `char*` -- pointers to a null-terminated string of `char` values.
    In Python, this means the inputs need to be `bytes` values.
    Then `flags` is a regular Python `int`.

    ```python
    # Source and destination files
    src = b"1GB.bin"
    dst = b"clone.bin"

    # clonefile(2) supports several options related to symlinks and
    # ownership information, but for this example we'll just use
    # the default behaviour
    flags = 0
    ```

4.  **Call the function.**
    Now we have the function available in Python, and the inputs in C-compatible types, we can call the function:
    
    {% code lang="python" names="5:errno" %}
    import os
    
    if clonefile(src, dst, flags) != 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    
    print(f"clonefile succeeded: {src} ~> {dst}")
    {% endcode %}
    
    If the clone succeeds, this program runs successfully.
    But if the clone fails, we get an unhelpful error: *OSError: [Errno 0] Undefined error: 0*.
    
    The point of calling the C function is to get useful error codes, but we need to opt-in to receiving them.
    In particular, we need to add the `use_errno` parameter to our `CDLL` call:
    
    {% code lang="python" names="0:libSystem" %}
    libSystem = ctypes.CDLL("libSystem.B.dylib", use_errno=True)
    {% endcode %}
    
    Now, when the clone fails, we get different errors depending on the type of failure.
    The exception includes the numeric error code, and Python will throw named subclasses of `OSError` like `FileNotFoundError`, `FileExistsError`, or `PermissionError`.
    This makes it easier to write `try … except` blocks for specific failures.

Here's the complete script, which clones a single file:

{% code lang="python" names="2:libSystem 6:clonefile 21:src 22:dst 23:flags 28:errno" %}
import ctypes
import os

# Load the libSystem library
libSystem = ctypes.CDLL("libSystem.B.dylib", use_errno=True)

# Tell ctypes about the function signature
# int clonefile(const char * src, const char * dst, int flags);
clonefile = libSystem.clonefile
clonefile.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
clonefile.restype = ctypes.c_int

# Source and destination files
src = b"1GB.bin"
dst = b"clone.bin"

# clonefile(2) supports several options related to symlinks and
# ownership information, but for this example we'll just use
# the default behaviour
flags = 0

# Actually call the clonefile() function
if clonefile(src, dst, flags) != 0:
    errno = ctypes.get_errno()
    raise OSError(errno, os.strerror(errno))
    
print(f"clonefile succeeded: {src} ~> {dst}")
{% endcode %}

I wrote this code for my own learning, and it's definitely not production-ready.
It works in the happy case and helped me understand `ctypes`, but if you actually wanted to use this, you'd want proper error handling and testing.

In particular, there are cases where you'd want to fall back to [`shutil.copyfile`][shutil.copyfile] or similar if the clone fails -- say if you're on an older version of macOS, or you're copying files on a volume which doesn't support cloning.
Both those cases are handled by `cp -c`, but not the `clonefile()` syscall.

[ctypes]: https://docs.python.org/3/library/ctypes.html
[cdll]: https://docs.python.org/3/library/ctypes.html#loading-dynamic-link-libraries
[otool]: https://alexwlchan.net/man/man1/otool.html
[c_char_p]: https://docs.python.org/3/library/ctypes.html#ctypes.c_char_p

<h2 id="in-practice">In practice, how am I cloning files in Python?</h2>

In my project, I used `cp -c` with a wrapper like the one described above.
It's a short amount of code, pretty readable, and returns useful errors for common cases.

Calling `clonefile()` directly with `ctypes` might be slightly faster than shelling out to `cp -c`, but the difference is probably negligible.
The downside is that it's more fragile and harder for other people to understand -- it would have been the only part of the codebase that was using `ctypes`.

File cloning made a noticeable difference.
The project involving copying lots of files on an external USB hard drive, and cloning instead of copying full files made it much faster.
Tasks that used to take over an hour were now completing in less than a minute.
(The files were copied between folders on the same drive -- cloned files have to be on the same APFS volume.)

I'm excited to see how file cloning works on Linux in Python 3.14 [with `Path.copy()`][cpython119058], and I hope macOS support isn't far behind.
