---
date: 2016-12-01 07:43:00 +0000
layout: post
slug: strings-are-terrible
summary: 'Pop quiz: if I lowercase a string, does it still have the same length as
  the original string?'
tags: unicode, hypothesis, python
title: Another example of why strings are terrible
---

Here's a programming assumption I used to make, that until today I'd never really thought about: *changing the case of a string won't change its length*.

Now, thanks to [Hypothesis](http://hypothesis.works), I know better:

```pycon
>>> x = u'İ'
>>> len(x)
1
>>> len(x.lower())
2
```

I'm not going to pretend I understand enough about Unicode or Python's string handling to say what's going on here.

I discovered this while testing a moderately fiddly normalisation routine &ndash; this routine would normalise the string to lowercase, unexpectedly tripping a check that it was the right length.
If you'd like to see this for yourself, here's a minimal example:

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_changing_case_preserves_length(xs):
    assert len(xs) == len(xs.lower())
```

{% update 2016-12-02 %}
  [David MacIver asked](https://twitter.com/DRMacIver/status/804236463516844037) whether this affects Python 2, 3, or both, which I forgot to mention.
  The behaviour is different: Python 2 lowercases `İ` to an ASCII `i`, whereas Python 3 adds a double dot: `i̇`.

  This means that only Python 3 has the bug where the length changes under case folding (whereas Python 2 commits a different sin of throwing away information).

  Cory Benfield pointed out that the Unicode standard has explicit character mappings that add or remove characters when changing case, and [highlights a nice example](https://twitter.com/Lukasaoz/status/804236722561228801) in the other direction: when you uppercase the German [esszett (ß)](https://en.wikipedia.org/wiki/ß), you replace it with a double-S.

  Finally, Rob Wells wrote a [follow-on post](http://www.robjwells.com/2016/12/language-is-hard-strings-are-great/) that explains this problem in more detail.
  He also points out the potential confusion of `len()`: should it count visible characters, or Unicode code points?
  The Swift String API does a rather good job here: if you haven't used it, check out Apple's [introductory blog post](https://developer.apple.com/swift/blog/?id=30).
{% endupdate %}
