---
layout: note
title: Python f-strings cheat sheet
date: 2026-01-30 07:47:30 +00:00
summary:
  Some Python f-string examples that I find helpful.
breadcrumb: 
  - label: Python
    href: /python/
---
This is a collection of Python f-string (["formatted string"][pydoc-fstring]) examples that I find helpful but don't always remember.

## Numbers

Print a number with commas:

```pycon
>>> f'{123456789:,}'
'123,456,789'
```

Print a number and add spaces to make it a fixed width:

```pycon
>>> f'{123456:9}'
'   123456'
```

Print a fixed-width number with commas:

```pycon
>>> f'{123456:9,}'
'  123,456'
```

[pydoc-fstring]: https://docs.python.org/3/reference/lexical_analysis.html#f-strings
