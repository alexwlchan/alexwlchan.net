---
category: Working with macOS
date: 2019-03-11 20:31:17 +0000
layout: post
tags: os-x shell-scripting
title: Finding the latest screenshot in macOS Mojave
---

One of the things that changed in macOS Mojave was the format of screenshot filenames.
On older versions of macOS, the filename would be something like:

```
Screen Shot 2016-10-10 at 18.34.18.png
```

On Mojave, the first two words got collapsed into one:

```
Screenshot 2019-03-08 at 18.38.41.png
```

I have a handful of scripts for doing something with screenshots -- and in particular, a shortcut that grabs the newest screenshot.
When I started updating to Mojave, I had to update the shell snippet that powers that shortcut.
Because I couldn't update to Mojave on every machine immediately, it had to work with both naming schemes.

This is what I've been using for the last few months (bound to `last_screenshot` in my shell config):

```shell
find ~/Desktop -name 'Screen Shot*' -print0 -o -name 'Screenshot*' -print0
  | xargs -0 stat -f '%m %N'
  | sort --numeric-sort --reverse
  | head -1
  | cut -f "2-" -d " "
```

Let's break it down:

*   The `find` command looks for files in ~/Desktop (where my screenshots get saved) that match the filename `Screen Shot*` or `Screenshot*`.

    It prints the name of every matching file, separated by the [null character][null] (as set by the `-print0` flag).
    Because most shell languages don't have a proper list type, just strings, the null character is a way to shoehorn a list into a string.
    It's less likely to appear in one of your list elements than, say, a newline or a space.

*   `xargs -0` unpacks the null character-separated string, and passes each filename to the `stat` command.
    This prints information about the file: `%m` is the last modified time, and `%N` is the filename.

    You get a list a bit like this:

    ```
    1551602947 /Users/alexwlchan/Desktop/Screenshot 2019-03-03 at 08.49.01.png
    1552070046 /Users/alexwlchan/Desktop/Screenshot 2019-03-08 at 18.34.00.png
    1552260786 /Users/alexwlchan/Desktop/Screenshot 2019-03-10 at 23.33.01.png
    1552070259 /Users/alexwlchan/Desktop/Screenshot 2019-03-08 at 18.37.33.png
    1552070326 /Users/alexwlchan/Desktop/Screenshot 2019-03-08 at 18.38.41.png
    1552070066 /Users/alexwlchan/Desktop/Screenshot 2019-03-08 at 18.34.19.png
    ```

*   That entire string in turn gets passed to `sort`, which treats the strings as numeric (so `3` sorts below `10`, for example), then reverses the order.
    This puts the biggest number -- the newest file modification date -- at the top.

*   The sorted list is passed to `head`, which extracts the top line (the newest file).

*   Finally, `cut` separates the string on spaces (`-d " "`), then prints the second element and everything after it -- throwing away the timestamp, and leaving the filename.

It's certainly possible to do this with a higher-level language like Python or Ruby, but I like the elegance of chaining together tiny utilities like this.
For non-critical code, I enjoy the brevity.

[null]: https://en.wikipedia.org/wiki/Null_character