---
layout: til
title: List all Git object IDs and their type
date: 2018-09-17 12:39:00 +00:00
tags:
  - git
---

From Michal Grochmal in the PyCon UK Slack:

```console
$ find .git/objects/ -type f | sed -e s^\.git/objects/^^ -e s^/^^ | sort | while read x; do echo -n "$x "; git cat-file -t $x; done
```

That didn't work for me on macOS, because I have a different version of sed (I think).
This is less pretty but has the same effect.

```console
$ find .git/objects -type f | tr '/' ' ' | awk '{print $3 $4}' | grep -v pack | while read x; do echo -n "$x "; git cat-file -t "$x"; done
```

With either command, output is of the form:

```
12779b2e3b24fded5f817525a416a625e9f1a356 tree
38246dfb9d83a2c7be5ee0dda3a62cb223e9a764 blob
5d7cd731f9beefea46efe0d13fb1ec11bfb09001 blob
95c8c8a03c2c037b5de2a1eb80d55ec8dd80a528 blob
cfaa614fd42ee1408341d3db3a1570713ea3494c blob
de9e0026f9d6c1948096dfefb093aa25a188577d blob
e977704a7442a6e80b3d1119a7fcc44b29e22f06 tree
ef2fc0e9ecc83352a410860f6baf8b33c66f82fb tree
f25c461b1674c1d67146f57f7ac9c3626958ff3e blob
f741f48754937179332d2f1fb6f670065c5f69bd commit
f8292a790c79453822afaa6f8fee4dd4a14c5cd1 tree
ff6e0f7a0e941b152ccb63e656b110f48f65515e commit
```
