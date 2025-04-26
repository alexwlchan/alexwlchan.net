---
layout: til
title: When fixing mojibake, use `ftfy.fix_and_explain()` to understand how it's fixing a piece of text
date: 2025-04-26 08:29:22 +0100
tags:
  - python
  - unicode
---
I was writing some code that was pulling in text from a third-party API, and the API was returning [Mojibake] -- text with an obviously mangled encoding.
I wanted to fix the mangled encoding before I showed the text in my app.

I was already aware of Robyn Speer's excellent [python-ftfy library][ftfy], which is able to fix this sort of thing.
(The name "ftfy" literally stands for "fix text for you".)

```pycon
>>> import ftfy
>>> title = "Amadeo LeÃ³n Rochaâ€™s plight"
>>> fixed = ftfy.fix_text(title)
>>> fixed
"Amadeo León Rocha's plight"
```

What I learnt today is that ftfy doesn't just fix text -- it can [*explain the fixes*][explain].
Here's an example:

```pycon
>>> import ftfy
>>> title = "Amadeo LeÃ³n Rochaâ€™s plight"
>>> fixed, explanation = ftfy.fix_and_explain(title)

>>> fixed
"Amadeo León Rocha's plight"

>>> explanation
[('encode', 'sloppy-windows-1252'),
 ('decode', 'utf-8'),
 ('apply', 'uncurl_quotes')]
```

This will be invaluable if I want to report the errors to the upstream data provider -- I can write a more detailed bug report than "text's broken, fix it please".

This also allowed me to understand why my attempts to fix the data weren't working -- there were actually multiple encoding messes in the same data set.
As well as some poorly encoded Windows-1252, I had some poorly encoded Latin-1:

```pycon
>>> title = "Stockholms SpÃ¥rvÃ¤gsmuseum"
>>> fixed, explanation = ftfy.fix_and_explain(title)

>>> fixed
'Stockholms Spårvägsmuseum'

>>> explanation
[('encode', 'latin-1'), ('decode', 'utf-8')]
```

While ftfy is a great tool for experimentation, I don't necessarily want it in my production data pipeline -- it's a bit of a black box.
But now I can use ftfy to work out the issues, then write my own code for applying the fixes, and I'll understand exactly what my code is doing.

[Mojibake]: https://en.wikipedia.org/wiki/Mojibake
[ftfy]: https://pypi.org/project/ftfy/
[explain]: https://ftfy.readthedocs.io/en/latest/explain.html
