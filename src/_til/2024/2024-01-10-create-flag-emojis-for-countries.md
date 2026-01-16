---
layout: til
title: How to create flag emojis for countries in Python
date: 2024-01-10 10:31:11 +00:00
tags:
  - python
  - unicode
---
## Flags for countries with 2-character codes

There's a [pycountry package][pycountry] that provides a Python API for the ISO databases for country information.
You can get the flags from its API, for example:

```pycon
>>> import pycountry
>>> germany = pycountry.countries.get(alpha_2='DE')
>>> germany.flag
'🇩🇪'
```

Alternatively, flag emojis are constructed from a pair of "regional indicator symbol letters", e.g. the Armenian country code is AM, so the flag emoji is 🇦🇲 = 🇦​🇲.
You can then construct your flags like so:

```python
def get_flag_emoji(country_id: str) -> str:
    code_point_start = ord("🇦") - ord("A")
    assert code_point_start == 127397

    code_points = [code_point_start + ord(char) for char in country_id]
    return "".join(chr(cp) for cp in code_points)
```

This is based on JavaScript code [written by Jorik Tangelder][jorik], but adapted for Python and an explanation of the `127397` magic number.

[jorik]: https://dev.to/jorik/country-code-to-flag-emoji-a21
[pycountry]: https://pypi.org/project/pycountry/

## Flags for subdivisions of countries (e.g. Scotland, Wales)

Some countries are subdivisions of other countries, and some of those subdivisions have flags.

pycountry doesn't have flags for subdivisions, e.g.

```pycon
>>> scotland = pycountry.subdivisions.get(code='GB-SCT')
>>> scotland.flag
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/private/var/folders/_c/h0g4c9_n6rg8d2v509hztzdc0000gn/T/tmp.YhlCEzkg/.venv/lib/python3.12/site-packages/pycountry/db.py", line 17, in __getattr__
    raise AttributeError()
AttributeError
```

And these flags aren't constructed from two-character regional codes.
e.g. the Scottish flag combines black flag, five regional indicator symbols, and a closing symbol: 🏴󠁧󠁢󠁳󠁣󠁴󠁿 = 🏴​ 🇬​🇧​🇸​🇨​🇹 ​U+E007F

The best approach I've found is to hard-code exceptions for these where necessary:

```python
def get_flag_emoji(country_id: str) -> str:
    if country_id == "GB-SCT":
        return "🏴󠁧󠁢󠁳󠁣󠁴󠁿"

    if country_id == "GB-WLS":
        return "🏴󠁧󠁢󠁷󠁬󠁳󠁿"

   …
```

Note that [Emojipedia's page about flags][emojipedia] suggests this may be a relatively uncommon case, and just a few edge cases may be enough to handle it:

> Emoji country flags are based on ISO 3166-1: a list of internationally recognized two-letter country codes. As of 2021 England, Scotland and Wales are the only RGI subdivision flags.

[emojipedia]: https://emojipedia.org/flags
