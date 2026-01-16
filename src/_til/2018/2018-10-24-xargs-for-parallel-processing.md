---
layout: til
title: How to use xargs for parallel processing
date: 2018-10-24 08:55:00 +00:00
tags:
  - shell scripting
---
If you have a file full of arguments (`inputs.txt`), and a script that takes a single ID as an argument (`process_single_id.py`), you can run the script in parallel with `xargs`:

```shell
$ xargs -P 84 -I '{}' python process_single_id.py '{}' < inputs.txt
```

Customise the number of parallel processes with the `-P` flag.

You'll want to experiment with the number of processes you run.

(I discovered this while migrating images between two image management systems.
Although my laptop's CPU could handle up to 84 parallel processes, that caused more errors in the APIs of the image management systems, so the overall throughput was actually less.)
