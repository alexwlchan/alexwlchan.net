---
layout: note
date: 2026-07-21 08:49:38 +01:00
title: A single command to test all my changed Go packages
summary: |
  <code>go test $(git ls-files --modified | xargs dirname | uniq | xargs -I '{}' echo "./{}")</code>
topics:
  - Go
  - Software testing
---
I work in a Go monolith with many packages, and my patches often span multiple patches.
Before I push to CI, I like to test all the packages with changed files, but enumerating all those packages by hand is tedious.

I've automated this with a short shell script:

```shell
go test $(git ls-files --modified \
  | xargs dirname \
  | uniq \
  | xargs -I '{}' echo "./{}")
```

Here's how it works:

*   `git ls-files --modified` -- print the path of every file with an unstaged change
*   `xargs dirname` -- print the list of folders/packages
*   `uniq` -- de-duplicate the list
*   `xargs -I '{}' echo "./{}"` -- prepend `./` to each path, so the folder can be passed to `go test`