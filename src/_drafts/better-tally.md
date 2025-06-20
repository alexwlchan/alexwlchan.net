---
layout: post
title: A better shell alias for tallying data
summary: How I count records on the command-line.
tags:
  - shell scripting
---
Eight years ago, I wrote about [`tally`][old_post], a shell alias I use for tallying data on the command line.

I can pipe it some text, and it would print a tally of all the lines:

```console
$ cat colors.txt | tally
   8 yellow
  45 red
  68 green
 100 blue
```

[old_post]: /2016/a-shell-alias-for-tallying/