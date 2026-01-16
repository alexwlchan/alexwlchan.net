---
layout: til
title: Create a directory before you `cp` or `mv` a file to it
date: 2024-01-07 20:23:36 +00:00
tags:
  - shell scripting
---
Not an exciting snippet, but one I should remember – the bash builtins really aren't too bad for creating a directory before it exists when you `mv`/`cp`:

```bash
mkdir -p "$(dirname "$dst")"
cp "$src" "$dst"
```

I actually don't know if I've done this before (vs just copying the directory name into `mkdir -p`), but this is a bit more DRY.
I spotted it when working in a script that already makes extensive use of `basename` and `dirname`.
