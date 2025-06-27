---
layout: til
title: Comparing two files in a bash script
date: 2025-06-27 14:00:21 +0100
summary: Inspect the exit value of `cmp --silent`.
tags:
  - shell scripting
---
I wanted to write a bash script that compares the contents of two files, and takes an action if the two files are different.
I also wanted this script to be compatible with my usual bash flags -- I run usually write scripts with `errexit` and `nounset`.

I discovered I can use the `cmp` command.
Here's a simple example:

```bash
#!/usr/bin/env bash

set -o errexit
set -o nounset

if cmp --silent "1.txt" "2.txt"
then
    echo "the files are the same!"
else
    echo "the files are different!"
fi
```

Note that if one or both of the files don't exist, then `cmp` returns a non-zero exit code.
In my use case, that was fine, but in other cases you might want to distinguish between "the files are different" and "the files don't exist".

You can invert this if you only want to do something when the files are different:

```bash
#!/usr/bin/env bash

set -o errexit
set -o nounset

if ! cmp --silent "1.txt" "2.txt"
then
    echo "the files are different!"
fi
```