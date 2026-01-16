---
layout: post
date: 2021-01-01 11:11:48 +00:00
title: What year is it? (A tale of ISO week dates)
summary: If you use ICU date formatting, make sure you use the right format specifier for year.
tags:
  - datetime shenanigans
colors:
  index_light: "#b17474"
  index_dark:  "#c28786"
---

Happy (Gregorian) new year!

As I type, it's 9am UTC, and 2021 has arrived in most of the world.
Timezones mean the new year doesn't arrive all at once: it starts in small Pacific islands like Samoa and Kiritimati, [works its way from east to west][timezones], and eventually finishes back in the Pacific, on Baker Island.
For about 24 hours, *"what year is it?"* depends on where you are.

This year, my computer decided to join in the fun.
I have a text expansion macro that prints the current date, and when I ran it shortly after midnight, this was the output:

```
2020-01-01
```

Uh oh.
Computer bug, or a terrifying 2020-esque Groundhog Day?

[timezones]: https://www.timeanddate.com/counters/firstnewyear.html



---



I run the macro with Keyboard Maestro, which types the following snippet:

```
%ICUDateTime%Y-MM-dd%
```

Some of you can already see the issue, but it was a mystery to me -- if you're still puzzled, keep reading.
Those `%` symbols mean this is a Keyboard Maestro *token*: rather than typing the literal text, it [types the date in the ICU format `Y-MM-dd`][kmaestro].

I tried updating to the latest version of Keyboard Maestro, and the output was the same.
Unsurprising, but good to check.

I almost never work with ICU date formatting; I'm more used to the format used by [strftime(3)][strftime] and [strptime(3)][strptime] (which are in turn used by the Python [datetime library][datetime]).
The format specifier looked correct to me, but clearly something was wrong.

[kmaestro]: https://wiki.keyboardmaestro.com/token/ICUDateTime
[strftime]: https://alexwlchan.net/man/man3/strftime.html
[strptime]: https://alexwlchan.net/man/man3/strptime.html
[datetime]: https://docs.python.org/3/library/datetime.html



---



The Keyboard Maestro docs link to the [ICU date format instructions](https://unicode-org.github.io/icu/userguide/format_parse/datetime/#date-field-symbol-table), and here I discovered my error.
Although uppercase `Y` seems to work, it's actually one of *two* symbols for the year:

{%
  picture
  filename="icu_symbols.png"
  alt="A table with two rows. The first has symbol 'y' and is the 'year'; the second had symbol 'Y' and is the 'year of “Week of Year”'"
  class="screenshot"
  width="627"
%}

The first year is the calendar year, and what I thought I was using.

The second, "Week of Year" refers to the [ISO week date](https://en.wikipedia.org/wiki/ISO_week_date), a system that divides the year into numbered weeks.
Each week starts on a Monday and runs for seven days, so a week is always in a single year and has a predictable length.
For certain fiscal processes, those properties are more useful than the variable-length months of the calendar year.

Here's how the ISO weeks look around December 2020:

<figure style="max-width: 500px;">
{%
  inline_svg
  filename="week_numbers.svg"
  alt="A table showing a small December calendar and the week numbers down the left."
%}
</figure>

Notice that January 1, 2021 is in Week 53 of 2020, so the ISO week-calendar year is still 2020, and will be until next Monday.
This is where my problem lies: **I was using the wrong type of year in my ICU format specifier.**

For almost all the year, the calendar year and the ISO week-calendar year are the same -- it's only in the first few days of the calendar year when they differ.
I can't remember when I wrote this macro, and it's possible it's been broken for multiple years.
The code seemed to be working until today, even if it was by coincidence rather than because it was actually correct.

If this bug was in some sort of business software that was only used on workdays, it could last a very long time without being detected.
The ISO week starts on a Monday, so it's quite possible the first week of the new ISO year would always start before anybody ran the broken code.



---



This is the ICU format specifier for the calendar date:

```
yyyy-MM-dd => "2021-01-01"
```

This is the ICU format specifier for the ISO week-calendar date:

```
Y-w-e => "2020-53-5"
```

Both are valid and useful formats, but mixing the two year types is a mistake waiting to happen.

A datetime bug seems like some sort of omen for 2021.
I hope it's an auspicious one, and I hope this new year finds you all well and safe.

*This post started as a [thread on Twitter](https://twitter.com/alexwlchan/status/1344809737322377221).*
