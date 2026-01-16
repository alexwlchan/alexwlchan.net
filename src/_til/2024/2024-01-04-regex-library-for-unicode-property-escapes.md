---
layout: til
title: Use the regex library to get Unicode property escapes in Python
date: 2024-01-04 23:47:49 +00:00
tags:
  - python
  - unicode
---
I was writing some code to detect and replace emoji.

Maybe you can do this using the builtin `re` module by defining character classes (*"all Unicode characters in range X–Y"*) but that looks tedious and fiddly.
I had a vague memory of "named Unicode groups" – what I was thinking of were Unicode property escapes (which I've previously used [in JavaScript](/til/2023/use-unicode-property-escapes-to-find-emoji/)).

You can use those with the [`regex` library][regex], which is a dropin replacement for the standard library `re` module.

Here's the set of examples from JavaScript: note the difference between `Emoji` and `Extended_Pictographic`.

```pycon
>>> import regex

>>> regex.search(r'\p{Emoji}', 'flowers')
>>> regex.search(r'\p{Emoji}', 'flowers 🌼🌺🌸')
<regex.Match object; span=(8, 9), match='🌼'>
>>> regex.search(r'\p{Emoji}', 'flowers 123')
<regex.Match object; span=(8, 9), match='1'>

>>> regex.search(r'\p{Extended_Pictographic}', 'flowers')
>>> regex.search(r'\p{Extended_Pictographic}', 'flowers 🌼🌺🌸')
<regex.Match object; span=(8, 9), match='🌼'>
>>> regex.search(r'\p{Extended_Pictographic}', 'flowers 123')
```

[regex]: https://pypi.org/project/regex/
