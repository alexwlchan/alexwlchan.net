---
layout: post
date: 2020-08-18 15:19:20 +0000
title: S3 keys are not file paths
summary: Although an S3 key looks a lot like a file path, they aren't always the same, and the distinction can trip you up.
tags: amazon-s3 aws
---

If you look at an S3 bucket, you could be forgiven for thinking it behaves like a hierarchical filesystem, with everything organised as files and folders.
Indeed, the S3 console even has a button labelled "Create folder":

<img src="/images/2020/s3_faux_directories.png" alt="Screenshot of the S3 console, including a 'Create folder' button in blue">

But S3 isn't a filesystem; it's an *object store*.
Each object is associated with a *key*, and although keys often happen to look a bit like filesystem paths, they're not the same.
If you treat them as interchangeable, you may be in for a nasty surprise -- as I recently discovered.



## The problem

Most filesystems have special path entries that mean "the current directory" and "the parent directory" -- on Unix-like systems, those are `.` and `..`, respectively.
That means that if you treat the following strings as paths, all four of them point to the same file:

```
pictures/cat.jpg
pictures//cat.jpg
pictures/./cat.jpg
pictures/pets/../cat.jpg
```

But in S3, object keys are just an unstructured identifier -- characters like `/` and `.` don't have any special meaning.
The console will uses slashes to create faux-directories to make it easier to navigate, but there's no special treatment for a faux-directory called `.` or `..`.

You could use the four strings above as keys for four different S3 objects.
That's completely legal, but it's liable to confuse any code that thinks of the world as a filesystem -- or any code that manipulates S3 keys as if they were file paths.

This includes the AWS CLI -- if you use it to download the contents of a bucket, those four objects will be collapsed into a single file:

```
$ aws s3 sync s3://bukkit bukkit
download: s3://bukkit/pictures/./cat.jpg       to bukkit/pictures/cat.jpg
download: s3://bukkit/pictures//cat.jpg        to bukkit/pictures/cat.jpg
download: s3://bukkit/pictures/pets/../cat.jpg to bukkit/pictures/cat.jpg
download: s3://bukkit/pictures/cat.jpg         to bukkit/pictures/cat.jpg
```

Which object you get will vary from sync to sync.
If you were using this, say, to back up the contents of an S3 bucket, you'd be missing data in your backup.
Eek!



## The solution

Most languages include a function to *normalise* a path -- to remove redundant path entries and collapse parent directories.
For example, in Python, we can use [Path.resolve](https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve):

```pycon
>>> def normalise(p):
...     return str(pathlib.PosixPath(p).resolve(strict=False)).encode().decode()
...
>>> normalise('pictures/cat.jpg')
'pictures/cat.jpg'
>>> normalise('pictures//cat.jpg')
'pictures/cat.jpg'
>>> normalise('pictures/./cat.jpg')
'pictures/cat.jpg'
>>> normalise('pictures/pets/../cat.jpg')
'pictures/cat.jpg'
```

You can in turn create a function that tells you whether a path is normalised:

```python
def is_normalised(path):
    return path == normalise(path)
```

(Note that normalisation rules can vary by platform -- for example, POSIX and Windows have different rules.
If you're running on a consistent platform, you're probably okay.)

As far as I know, normalised paths are distinct and unambigous.
If two normalised paths are different, then they refer to different files in a filesystem.
Thus: **if you only ever use normalised paths for S3 keys, you can treat S3 keys and file paths as interchangeable.**

We recently introduced a rule at work that blocks creating S3 objects whose keys aren't normalised paths.
I thought we were already doing this; enforcing it in the Scala type system immediately exposed several places where we weren't handling it correctly.

S3 still isn't a filesystem -- for example, I can put an arbitrary number of objects under a single prefix, whereas most filesystems balk at more than a few thousand files in a single directory -- but if you only use normalised paths for keys, there's no risk of data loss from having multiple keys that normalise to the same path.



## The special cases

S3 has some internal logic to prevent the most destructive mistakes.
In particular, although it allows using `/../` anywhere inside a key, it prevents you from creating a path that would normalise to a location outside the root of the bucket.
If you try to create an object with such a key, you get an HTTP 400 error.

Here are a few examples:

<style>
  table { margin-left: auto; margin-right: auto; }
  .tick { text-align: center; color: #11b01c; }
  .cross { text-align: center; color: #d01c11; }
</style>

<table>
  <tr><td class="tick">✔</td><td><code>x/../x</code></td></tr>
  <tr><td class="cross">✘</td><td><code>x/../../x</code></td></tr>
  <tr><td class="tick">✔</td><td><code>x/y/../../x</code></td></tr>
  <tr><td class="cross">✘</td><td><code>x/y/../../../x</code></td></tr>
  <tr><td class="cross">✘</td><td><code>x/y/../../../x/y</code></td></tr>
  <tr><td class="tick">✔</td><td><code>x/y/../../x/../x/y</code></td></tr>
</table>

Imagine if S3 *did* allow you to create these forbidden keys.
If you were to sync such a key to your local filesystem, it would write that file somewhere outside your current directory – which could have all sorts of unexpected consequences!

I shudder to think about the edge cases this code has to handle.



## The summary

Imagine two distinct sequences of bytes.
If treated as object keys, they refer to different objects in S3.
If treated as file paths, they could refer to the same file on a filesystem.
If you treat S3 keys and file paths as interchangeable, there's a risk of confusion or data loss.

If you only use normalised paths as S3 keys, it's less risky to treat the two interchangeably.

This post is more of a "don't make the same mistake as me" than a "this is definitely right".
I think using normalised paths for keys is safe, but I might be wrong.
Think I've missed something?
Drop me [a tweet](https://twitter.com/alexwlchan) or [an email](mailto:alex@alexwlchan.net).




{% update 2020-08-18 %}
  [Thomas Grainger](https://twitter.com/graingert/) pointed out a few issues:

  *   Path normalisation is platform-dependent -- if you use `os.path.normpath()` on Windows, it converts slashes to backslashes.
      I'm normally interacting with S3 from macOS or Linux so it's not an issue for me.
      I've updated the example to use POSIX paths consistently.

  *   S3 keys are case-sensitive; some filesystems aren't.
      If you have keys `CAT.jpg` and `cat.jpg`, they might become the same file when you download them.

  *   Not all S3 keys are valid filesystem paths -- some filenames are restricted, like COM or NUL on Windows.
      (Which I knew, having read [How I broke Rust's package manager for all Windows users](http://sasheldon.com/blog/2017/05/07/how-i-broke-cargo-for-windows/) a few years ago.)

      Not all filenames are valid S3 keys.
      A key can be at most 1024 bytes of UTF-8 encoded text, but some filesystems allow alternative encodings or longer filenames.

  Based on their comments, I went looking, and found [myths programmers believe about file paths](https://yakking.branchable.com/posts/falsehoods-programmers-believe-about-file-paths/).
  I still think normalising the path is adequate for my use case, but depending on your platform and how you're using S3, you want to be super careful using an S3 key as a filename, or vice versa.

  Paths are complicated, huh?
{% endupdate %}
