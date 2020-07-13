---
layout: post
date: 2020-07-13 22:20:06 +0000
title: What does \d match in a regex?
tags: regex
summary: It's more complicated than I thought.
---

[Earlier tonight](https://twitter.com/alexwlchan/status/1282771306824511488), I was playing with Hypothesis's [from_regex strategy](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.from_regex).
This strategy generates strings that match a given regex, and I thought it might be a good way to debug especially gnarly regexes -- by seeing examples of matching strings, maybe I could understand a complex regex better.

Here's what I got working:

```python
import re
from hypothesis.strategies import from_regex

gnarly_regex = r"\d+\(\d+\)"

regex_strategy = from_regex(gnarly_regex, fullmatch=True)

for _ in range(20):
    print(regex_strategy.example())
```

The regex is just a random example from Google, and nothing special -- but it exposed a bug in my understanding.

I know that `\d` matches any digits, and I'd always treated it as synonymous with `[0-9]` -- but it turns out that's not the case.
**If you run this code, you find all sorts of examples of Unicode characters which are digits and which match `\d`, but which aren't Arabic numerals.**
Here are just a couple:

- ꘠ / [Vai digit zero](https://www.fileformat.info/info/unicode/char/a620/index.htm)
- ೯ / [Kannada digit nine](https://www.fileformat.info/info/unicode/char/0cef/index.htm)
- ᧔ / [New Tai Lue digit four](https://www.fileformat.info/info/unicode/char/19d4/index.htm)
- ᠗ / [Mongolian digit seven](https://www.fileformat.info/info/unicode/char/1817/index.htm)

(Depending on your browser, those characters may or may not display correctly.)

Whoever implemented Unicode support in Python gave this more thought than me, because Python correctly treats all these characters as proper numbers.
We can verify this by writing two more tests using Hypothesis:

```python
from hypothesis import given
from hypothesis.strategies import from_regex

@given(from_regex(r"\d+", fullmatch=True))
def test_can_be_cast_to_int(s):
    int(s)

@given(from_regex(r"\d+", fullmatch=True))
def test_is_numeric(s):
    assert s.isnumeric()
```

Running that repeatedly doesn't find any counterexamples.

This isn't the first time Hypothesis has [exposed one of my faulty assumptions](/2016/12/strings-are-terrible/) -- language is incredibly complicated, and I still have a lot to learn.
