---
date: 2016-10-01 21:23:00 +0000
layout: post
tags: shell-scripting
title: A shell alias for tallying data
theme:
  minipost: true
---

Here's a tiny shell alias that I find useful when going through data on the command line.

Suppose I have a big collection of data, and I'd like to know which items occur most frequently: I want to build a [tally](https://en.wikipedia.org/wiki/Tally_marks).
I have this shell alias defined that lets me build such a tally:

```bash
alias tally='sort | uniq -c | sort'
```

Here's an example of the sort of output returned by piping to `tally`, a nice tabular format:

```console
$ cat colors.txt | tally
   8 yellow
  45 red
  68 green
 100 blue
```

(Note: on some Linuxes, `sort` uses alphabetical sorting, so you'll want to replace the second `sort` with `sort -h` to get a tally that sorts numerically.)

If you want to get the most common items from a tally, that's just another pipe: send the output from `tally` to `tail -n 5`, replacing 5 with the number of most common items you'd like to see.

Another example: let's see the five most common HTTP status codes in my Apache log.
I read the entire log, use `awk` to extract the status code, and then pass the output to `tally`:

```console
$ cat access.log | awk '{print $9}' | tally | tail -n5
  15804 302
  31955 204
  39115 301
  88825 404
 952709 200
```

This is one of the simplest aliases in my shell config, but I still like having it around.
Anything that saves me a bit of typing and thinking is usually worthwhile.