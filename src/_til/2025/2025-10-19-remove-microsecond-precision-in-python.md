---
layout: til
title: Remove the microsecond precision from a `datetime` in Python
summary: |
  Call `datetime.replace(microsecond=0)`.
date: 2025-10-19 10:16:27 +01:00
tags:
  - python
  - datetime shenanigans
---
If you print the current date as an ISO timestamp in Python, by default it includes microsecond precision (in this case, `.499258`):

{% code lang="pycon" names="0:d" %}
>>> d = datetime.now()
>>> d.isoformat()
'2025-10-19T09:23:04.384593'
{% endcode %}

I wanted to print some timestamps which are just HH:MM:SS, without the microseconds.

I could define a custom printer, or Python will also do what I want if I set the microseconds to zero:

{% code lang="pycon" %}
>>> d.replace(microsecond=0).isoformat()
'2025-10-19T09:23:04'
{% endcode %}

I don't love the decision to say "don't print the microseconds if it's zero", because there is a difference between "microseconds is unknown" and "microseconds is known to be zero" -- but in practice, that's a subtle distinction, and anybody who really cares in that level of detail is probably using `strftime()` to more precisely control their output.
