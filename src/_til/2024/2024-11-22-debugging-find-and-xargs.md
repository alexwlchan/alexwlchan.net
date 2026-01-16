---
layout: til
title: Debugging some confusing behaviour with `find` and `xargs`
date: 2024-11-22 16:35:11 +00:00
tags:
  - shell scripting
summary:
  Use the `--verbose` flag to see what `xargs` is doing; don't rely on `find` to return files in a consistent order.
---
I was trying to write a GitHub Actions workflow to format my Caddyfiles.
I'd written a command to find all the Caddyfiles in my repo, and pass them to `caddy fmt`:

```
find . -name Caddyfile | xargs caddy fmt --overwrite
```

Thsi command seemed to work when I ran it locally on my Mac, but it didn't do what I expected when it ran on Ubuntu in GitHub Actions.
It took me a while to work out what was going on!

I learnt two useful debugging techniques along the way:

1.  **Use the `--verbose` flag to see what `xargs` is doing.**
    This will print the exact command which is run by `xargs`.

    ```console
    $ ls *.jpg | xargs echo
    26704189108_9e71d865d8_b.jpg 51119071159_905212c30f_b.jpg 8076936667_c5605863a9_o.jpg

    $ ls *.jpg | xargs --verbose echo
    echo 26704189108_9e71d865d8_b.jpg 51119071159_905212c30f_b.jpg 8076936667_c5605863a9_o.jpg
    26704189108_9e71d865d8_b.jpg 51119071159_905212c30f_b.jpg 8076936667_c5605863a9_o.jpg

    $ ls *.jpg | xargs --verbose -I '{}' echo '{}'
    echo 26704189108_9e71d865d8_b.jpg
    26704189108_9e71d865d8_b.jpg
    echo 51119071159_905212c30f_b.jpg
    51119071159_905212c30f_b.jpg
    echo 8076936667_c5605863a9_o.jpg
    8076936667_c5605863a9_o.jpg
    ```

    In particular, I could see whether the command I was running with `xargs` was being called with all the arguments at once, or passed them individually.

2.  **Files discovered by `find` may be in a different order on different OSes.**

    This was the heart of my issue -- I was passing all my filenames in one big list, and `caddy fmt` will [only format the first path it gets](https://github.com/caddyserver/caddy/issues/6702).
    Because the order of files is different on different OSes, I was getting different behaviour.

    Compare:

    ```console
    $ # macOS
    $ find . -name Caddyfile -o -name '*.Caddyfile'
    ./Caddyfile
    ./caddy/gone.Caddyfile
    ./caddy/redirects.Caddyfile

    $ # Ubuntu
    $ find . -name Caddyfile -o -name '*.Caddyfile'
    ./caddy/gone.Caddyfile
    ./caddy/redirects.Caddyfile
    ./Caddyfile
    ```

    In hindsight, this makes sense -- there are multiple ways you might search a directory tree, and one isn't necessarily better than the other.

    Don't rely on the order to be consistent!

    I've had a brief glance at the man page, and `find` does have some options for controlling the ordering -- for example, you can use `-d`/`--depth` to do a depth-first search (process each directory's contents before the directory itself).

    This reminds me of when I discovered `WalkDir::contents_first()` and `os.walk(topdown: bool)` while [writing `emptydir`](/2024/emptydir/#how-does-it-work).
