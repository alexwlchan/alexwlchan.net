---
layout: post
date: 2020-07-13 22:20:06 +0000
title: What does \d match in a regex?
tags: regex
summary: It's more complicated than I thought.
---

[Earlier tonight](https://twitter.com/alexwlchan/status/1282771306824511488), I was playing with Hypothesis's [from_regex strategy](https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.from_regex).
This strategy generates strings that match a given regex, and I thought it might be a good way to debug especially gnarly regexes -- by seeing examples of matching strings, maybe I could understand a complex regex better.

I was trying to find strings that matched the regex `\d+\(\d+\)` (a random example from Google), and it exposed a bug in my understanding.

I know that `\d` matches any digits, and I'd always treated it as synonymous with `[0-9]` -- but it turns out that's not always the case.
**There are all sorts of Unicode characters which are digits and which match `\d`, but which aren't Arabic numerals.**
Here are just a couple:

- ꘠ / [Vai digit zero](https://www.fileformat.info/info/unicode/char/a620/index.htm)
- ೯ / [Kannada digit nine](https://www.fileformat.info/info/unicode/char/0cef/index.htm)
- ᧔ / [New Tai Lue digit four](https://www.fileformat.info/info/unicode/char/19d4/index.htm)
- ᠗ / [Mongolian digit seven](https://www.fileformat.info/info/unicode/char/1817/index.htm)

Different languages handle this differently -- for example, using `\d` in Python 3 will match all these numeric characters that aren't [Arabic numerals](https://en.wikipedia.org/wiki/Arabic_numerals), but in Python 2 it won't.
No doubt it varies among other programming languages as well.

How much this distinction matters depends on your use case, and in most cases I imagine the answer is "very little".
I present it more as an intellectual curiosity than something which needs serious consideration when writing regexes.

This isn't the first time Hypothesis has [exposed one of my faulty assumptions](/2016/12/strings-are-terrible/) -- language is incredibly complicated, and I still have a lot to learn.
