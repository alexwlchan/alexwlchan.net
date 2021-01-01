---
layout: post
title: What year it it? (A tale of ISO week dates)
summary: If you use ICU date formatting, make sure you use the right format specifier for year.
tags: datetime-shenanigans
---

<style>
  hr {
    margin-left:  1em;
    margin-right: 1em;
  }
</style>

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

[timezones]: https://www.timeanddate.com/counters/firstnewyear.html



<center class="separator">
  <!-- https://thenounproject.com/search/?q=calendar&i=3669219 -->
  <svg height='40px' width='40px' fill="#f0f0f0" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16.933333 16.933333" version="1.1" x="0px" y="0px">
    <g transform="translate(0,-280.06669)"><path style="color:#f0f0f0;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;font-variant-ligatures:normal;font-variant-position:normal;font-variant-caps:normal;font-variant-numeric:normal;font-variant-alternates:normal;font-feature-settings:normal;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;writing-mode:lr-tb;direction:ltr;text-orientation:mixed;dominant-baseline:auto;baseline-shift:baseline;text-anchor:start;white-space:normal;shape-padding:0;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;vector-effect:none;fill:#f0f0f0;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:3.99999976;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:8;stroke-opacity:1;paint-order:stroke fill markers;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate"
      d="M 15.996094 2 C 12.706681 2 10.001953 4.7106393 10.001953 8 L 10.001953 10
      L 8 10 C 4.7105924 10 2 12.710602 2 16 L 2 56 C 2 59.289398 4.7105924 62 8 62 L 15.996094 62 A 2.0001999 2.0001999 0 1 0 15.996094 58 L 8 58 C 6.8574465 58 6 57.142551 6 56 L 6 16 C 6 14.857449 6.8574465 14 8 14 L 10.001953 14 L 10.001953 16.001953 C 10.001953 19.291352 12.706704 21.996094 15.996094 21.996094 C 19.285484 21.996094 21.998047 19.291352 21.998047 16.001953 L 21.998047 14.001953 L 25.998047 14.001953 L 25.998047 16.001953 C 25.998047 19.291352 28.710609 21.996094 32 21.996094 C 35.28939 21.996094 38.001953 19.291352 38.001953 16.001953 L 38.001953 14.001953 L 42.003906 14.001953 L 42.003906 16.001953 C 42.003906 19.291352 44.706703 21.996094 47.996094 21.996094 C 51.285481 21.996094 53.998047 19.291389 53.998047 16.001953 L 53.998047 14 L 56 14 C 57.142555 14 58 14.857449 58 16 L 58 56 C 58 57.142551 57.142555 58 56 58 L 32 58 A 2.0001999 2.0001999 0 1 0 32 62 L 56 62 C 59.28941 62 62 59.289398 62 56 L 62 16 C 62 12.710602 59.28941 10 56 10 L 53.998047 10 L 53.998047 8 C 53.998047 4.7106393 51.285504 2 47.996094 2 C 44.70668 2 42.003906 4.7106393 42.003906 8 L 42.003906 10.001953 L 38.001953 10.001953 L 38.001953 8 C 38.001953 4.7106393 35.289413 2 32 2 C 28.710587 2 25.998047 4.7106393 25.998047 8 L 25.998047 10.001953 L 21.998047 10.001953 L 21.998047 8 C 21.998047 4.7106393 19.285507 2 15.996094 2 z M 15.996094 6 C 17.13868 6 17.996094 6.8574488 17.996094 8 L 17.996094 16.001953 C 17.996094 17.14458 17.138703 18.003906 15.996094 18.003906 C 14.853484 18.003906 14.003906 17.14458 14.003906 16.001953 L 14.003906 8 C 14.003906 6.8574488 14.853507 6 15.996094 6 z M 32 6 C 33.142586 6 34.001953 6.8574488 34.001953 8 L 34.001953 16.001953 C 34.001953 17.14458 33.142609 18.003906 32 18.003906 C 30.85739 18.003906 30 17.14458 30 16.001953 L 30 8 C 30 6.8574488 30.857413 6 32 6 z M 47.996094 6 C 49.138675 6 49.998047 6.8574488 49.998047 8 L 49.998047 16.001953 C 49.998047 17.14458 49.138698 18.003906 47.996094 18.003906 C 46.853482 18.003906 45.996094 17.14458 45.996094 16.001953 L 45.996094 8 C 45.996094 6.8574488 46.853505 6 47.996094 6 z M 12.003906 25.998047 A 2.000504 2.000504 0 0 0 12.003906 29.998047 L 51.998047 29.998047 A 2.000504 2.000504 0 1 0 51.998047 25.998047 L 12.003906 25.998047 z M 24 34 A 1.9999999 1.9999999 0 0 0 22 36 A 1.9999999 1.9999999 0 0 0 24 38 A 1.9999999 1.9999999 0 0 0 26 36 A 1.9999999 1.9999999 0 0 0 24 34 z M 32 34 A 1.9999999 1.9999999 0 0 0 30 36 A 1.9999999 1.9999999 0 0 0 32 38 A 1.9999999 1.9999999 0 0 0 34 36 A 1.9999999 1.9999999 0 0 0 32 34 z M 40 34 A 1.9999999 1.9999999 0 0 0 38 36 A 1.9999999 1.9999999 0 0 0 40 38 A 1.9999999 1.9999999 0 0 0 42 36
      A 1.9999999 1.9999999 0 0 0 40 34 z M 48 34 A 1.9999999 1.9999999 0 0 0 46 36 A 1.9999999 1.9999999 0 0 0 48 38 A 1.9999999 1.9999999 0 0 0 50 36 A 1.9999999 1.9999999 0 0 0 48 34 z M 16 42 A 1.9999999 1.9999999 0 0 0 14 44 A 1.9999999 1.9999999 0 0 0 16 46 A 1.9999999 1.9999999 0 0 0 18 44 A 1.9999999 1.9999999 0 0 0 16 42 z M 24 42 A 1.9999999 1.9999999 0 0 0 22 44 A 1.9999999 1.9999999 0 0 0 24 46 A 1.9999999 1.9999999 0 0 0 26 44 A 1.9999999 1.9999999 0 0 0 24 42 z M 32 42 A 1.9999999 1.9999999 0 0 0 30 44 A 1.9999999 1.9999999 0 0 0 32 46 A 1.9999999 1.9999999 0 0 0 34 44 A 1.9999999 1.9999999 0 0 0 32 42 z M 40 42 A 1.9999999 1.9999999 0 0 0 38 44 A 1.9999999 1.9999999 0 0 0 40 46 A 1.9999999 1.9999999 0 0 0 42 44 A 1.9999999 1.9999999 0 0 0 40 42 z M 48 42 A 1.9999999 1.9999999 0 0 0 46 44 A 1.9999999 1.9999999 0 0 0 48 46 A 1.9999999 1.9999999 0 0 0 50 44 A 1.9999999 1.9999999 0 0 0 48 42 z M 16 50 A 1.9999999 1.9999999 0 0 0 14 52 A 1.9999999 1.9999999 0 0 0 16 54 A 1.9999999 1.9999999 0 0 0 18 52 A 1.9999999 1.9999999 0 0 0 16 50 z M 24 50 A 1.9999999 1.9999999 0 0 0 22 52 A 1.9999999 1.9999999 0 0 0 24 54 A 1.9999999 1.9999999 0 0 0 26 52 A 1.9999999 1.9999999 0 0 0 24 50 z M 32 50 A 1.9999999 1.9999999 0 0 0 30 52 A 1.9999999 1.9999999 0 0 0 32 54 A 1.9999999 1.9999999 0 0 0 34 52 A 1.9999999 1.9999999 0 0 0 32 50 z M 40 50 A 1.9999999 1.9999999 0 0 0 38 52 A 1.9999999 1.9999999 0 0 0 40 54 A 1.9999999 1.9999999 0 0 0 42 52 A 1.9999999 1.9999999 0 0 0 40 50 z M 24 58 A 1.9999999 1.9999999 0 0 0 22 60 A 1.9999999 1.9999999 0 0 0 24 62 A 1.9999999 1.9999999 0 0 0 26 60 A 1.9999999 1.9999999 0 0 0 24 58 z " transform="matrix(0.26458333,0,0,0.26458333,0,280.06669)">
  </path>
</g>
</svg>
</center>



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
[strftime]: https://linux.die.net/man/3/strftime
[strptime]: https://linux.die.net/man/3/strptime
[datetime]: https://docs.python.org/3/library/datetime.html



<center class="separator">
  <!-- https://thenounproject.com/search/?q=calendar&i=3669219 -->
  <svg height='40px' width='40px' fill="#f0f0f0" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16.933333 16.933333" version="1.1" x="0px" y="0px">
    <g transform="translate(0,-280.06669)"><path style="color:#f0f0f0;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;font-variant-ligatures:normal;font-variant-position:normal;font-variant-caps:normal;font-variant-numeric:normal;font-variant-alternates:normal;font-feature-settings:normal;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;writing-mode:lr-tb;direction:ltr;text-orientation:mixed;dominant-baseline:auto;baseline-shift:baseline;text-anchor:start;white-space:normal;shape-padding:0;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;vector-effect:none;fill:#f0f0f0;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:3.99999976;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:8;stroke-opacity:1;paint-order:stroke fill markers;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate"
      d="M 15.996094 2 C 12.706681 2 10.001953 4.7106393 10.001953 8 L 10.001953 10
      L 8 10 C 4.7105924 10 2 12.710602 2 16 L 2 56 C 2 59.289398 4.7105924 62 8 62 L 15.996094 62 A 2.0001999 2.0001999 0 1 0 15.996094 58 L 8 58 C 6.8574465 58 6 57.142551 6 56 L 6 16 C 6 14.857449 6.8574465 14 8 14 L 10.001953 14 L 10.001953 16.001953 C 10.001953 19.291352 12.706704 21.996094 15.996094 21.996094 C 19.285484 21.996094 21.998047 19.291352 21.998047 16.001953 L 21.998047 14.001953 L 25.998047 14.001953 L 25.998047 16.001953 C 25.998047 19.291352 28.710609 21.996094 32 21.996094 C 35.28939 21.996094 38.001953 19.291352 38.001953 16.001953 L 38.001953 14.001953 L 42.003906 14.001953 L 42.003906 16.001953 C 42.003906 19.291352 44.706703 21.996094 47.996094 21.996094 C 51.285481 21.996094 53.998047 19.291389 53.998047 16.001953 L 53.998047 14 L 56 14 C 57.142555 14 58 14.857449 58 16 L 58 56 C 58 57.142551 57.142555 58 56 58 L 32 58 A 2.0001999 2.0001999 0 1 0 32 62 L 56 62 C 59.28941 62 62 59.289398 62 56 L 62 16 C 62 12.710602 59.28941 10 56 10 L 53.998047 10 L 53.998047 8 C 53.998047 4.7106393 51.285504 2 47.996094 2 C 44.70668 2 42.003906 4.7106393 42.003906 8 L 42.003906 10.001953 L 38.001953 10.001953 L 38.001953 8 C 38.001953 4.7106393 35.289413 2 32 2 C 28.710587 2 25.998047 4.7106393 25.998047 8 L 25.998047 10.001953 L 21.998047 10.001953 L 21.998047 8 C 21.998047 4.7106393 19.285507 2 15.996094 2 z M 15.996094 6 C 17.13868 6 17.996094 6.8574488 17.996094 8 L 17.996094 16.001953 C 17.996094 17.14458 17.138703 18.003906 15.996094 18.003906 C 14.853484 18.003906 14.003906 17.14458 14.003906 16.001953 L 14.003906 8 C 14.003906 6.8574488 14.853507 6 15.996094 6 z M 32 6 C 33.142586 6 34.001953 6.8574488 34.001953 8 L 34.001953 16.001953 C 34.001953 17.14458 33.142609 18.003906 32 18.003906 C 30.85739 18.003906 30 17.14458 30 16.001953 L 30 8 C 30 6.8574488 30.857413 6 32 6 z M 47.996094 6 C 49.138675 6 49.998047 6.8574488 49.998047 8 L 49.998047 16.001953 C 49.998047 17.14458 49.138698 18.003906 47.996094 18.003906 C 46.853482 18.003906 45.996094 17.14458 45.996094 16.001953 L 45.996094 8 C 45.996094 6.8574488 46.853505 6 47.996094 6 z M 12.003906 25.998047 A 2.000504 2.000504 0 0 0 12.003906 29.998047 L 51.998047 29.998047 A 2.000504 2.000504 0 1 0 51.998047 25.998047 L 12.003906 25.998047 z M 24 34 A 1.9999999 1.9999999 0 0 0 22 36 A 1.9999999 1.9999999 0 0 0 24 38 A 1.9999999 1.9999999 0 0 0 26 36 A 1.9999999 1.9999999 0 0 0 24 34 z M 32 34 A 1.9999999 1.9999999 0 0 0 30 36 A 1.9999999 1.9999999 0 0 0 32 38 A 1.9999999 1.9999999 0 0 0 34 36 A 1.9999999 1.9999999 0 0 0 32 34 z M 40 34 A 1.9999999 1.9999999 0 0 0 38 36 A 1.9999999 1.9999999 0 0 0 40 38 A 1.9999999 1.9999999 0 0 0 42 36
      A 1.9999999 1.9999999 0 0 0 40 34 z M 48 34 A 1.9999999 1.9999999 0 0 0 46 36 A 1.9999999 1.9999999 0 0 0 48 38 A 1.9999999 1.9999999 0 0 0 50 36 A 1.9999999 1.9999999 0 0 0 48 34 z M 16 42 A 1.9999999 1.9999999 0 0 0 14 44 A 1.9999999 1.9999999 0 0 0 16 46 A 1.9999999 1.9999999 0 0 0 18 44 A 1.9999999 1.9999999 0 0 0 16 42 z M 24 42 A 1.9999999 1.9999999 0 0 0 22 44 A 1.9999999 1.9999999 0 0 0 24 46 A 1.9999999 1.9999999 0 0 0 26 44 A 1.9999999 1.9999999 0 0 0 24 42 z M 32 42 A 1.9999999 1.9999999 0 0 0 30 44 A 1.9999999 1.9999999 0 0 0 32 46 A 1.9999999 1.9999999 0 0 0 34 44 A 1.9999999 1.9999999 0 0 0 32 42 z M 40 42 A 1.9999999 1.9999999 0 0 0 38 44 A 1.9999999 1.9999999 0 0 0 40 46 A 1.9999999 1.9999999 0 0 0 42 44 A 1.9999999 1.9999999 0 0 0 40 42 z M 48 42 A 1.9999999 1.9999999 0 0 0 46 44 A 1.9999999 1.9999999 0 0 0 48 46 A 1.9999999 1.9999999 0 0 0 50 44 A 1.9999999 1.9999999 0 0 0 48 42 z M 16 50 A 1.9999999 1.9999999 0 0 0 14 52 A 1.9999999 1.9999999 0 0 0 16 54 A 1.9999999 1.9999999 0 0 0 18 52 A 1.9999999 1.9999999 0 0 0 16 50 z M 24 50 A 1.9999999 1.9999999 0 0 0 22 52 A 1.9999999 1.9999999 0 0 0 24 54 A 1.9999999 1.9999999 0 0 0 26 52 A 1.9999999 1.9999999 0 0 0 24 50 z M 32 50 A 1.9999999 1.9999999 0 0 0 30 52 A 1.9999999 1.9999999 0 0 0 32 54 A 1.9999999 1.9999999 0 0 0 34 52 A 1.9999999 1.9999999 0 0 0 32 50 z M 40 50 A 1.9999999 1.9999999 0 0 0 38 52 A 1.9999999 1.9999999 0 0 0 40 54 A 1.9999999 1.9999999 0 0 0 42 52 A 1.9999999 1.9999999 0 0 0 40 50 z M 24 58 A 1.9999999 1.9999999 0 0 0 22 60 A 1.9999999 1.9999999 0 0 0 24 62 A 1.9999999 1.9999999 0 0 0 26 60 A 1.9999999 1.9999999 0 0 0 24 58 z " transform="matrix(0.26458333,0,0,0.26458333,0,280.06669)">
  </path>
</g>
</svg>
</center>



The Keyboard Maestro docs link to the [ICU date format instructions](https://unicode-org.github.io/icu/userguide/format_parse/datetime/#date-field-symbol-table), and here I discovered my error.
Although uppercase `Y` seems to work, it's actually one of *two* symbols for the year:

<img src="/images/2021/icu_symbols_1x.png" srcset="/images/2021/icu_symbols_1x.png 1x, /images/2021/icu_symbols_2x.png 2x" alt="A table with two rows. The first has symbol 'y' and is the 'year'; the second had symbol 'Y' and is the 'year of “Week of Year”'" style="width: 627px; box-shadow: 0 1px 2px rgba(0,0,0,0.12),0 3px 10px rgba(0,0,0,0.08)">

The first year is the calendar year, and what I thought I was using.

The second, "Week of Year" refers to the [ISO week date](https://en.wikipedia.org/wiki/ISO_week_date), a system that divides the year into numbered weeks.
Each week starts on a Monday and runs for seven days, so a week is always in a single year and has a predictable length.
For certain fiscal processes, those properties are more useful than the variable-length months of the calendar year.

Here's how the ISO weeks look around December 2020:

<figure style="max-width: 500px;">
{% inline_svg "_images/2021/week_numbers.svg" %}
</figure>

Notice that January 1, 2021 is in Week 53 of 2020, so the ISO week-calendar year is still 2020, and will be until next Monday.
This is where my problem lies: **I was using the wrong type of year in my ICU format specifier.**

For almost all the year, the calendar year and the ISO week-calendar year are the same -- it's only in the first few days of the calendar year when they differ.
I can't remember when I wrote this macro, and it's possible it's been broken for multiple years.
The code seemed to be working until today, even if it was by coincidence rather than because it was actually correct.

If this bug was in some sort of business software that was only used on workdays, it could last a very long time without being detected.
The ISO week starts on a Monday, so it's quite possible the first week of the new ISO year would always start before anybody ran the broken code.



<center class="separator">
  <!-- https://thenounproject.com/search/?q=calendar&i=3669219 -->
  <svg height='40px' width='40px' fill="#f0f0f0" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16.933333 16.933333" version="1.1" x="0px" y="0px">
    <g transform="translate(0,-280.06669)"><path style="color:#f0f0f0;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:medium;line-height:normal;font-family:sans-serif;font-variant-ligatures:normal;font-variant-position:normal;font-variant-caps:normal;font-variant-numeric:normal;font-variant-alternates:normal;font-feature-settings:normal;text-indent:0;text-align:start;text-decoration:none;text-decoration-line:none;text-decoration-style:solid;text-decoration-color:#000000;letter-spacing:normal;word-spacing:normal;text-transform:none;writing-mode:lr-tb;direction:ltr;text-orientation:mixed;dominant-baseline:auto;baseline-shift:baseline;text-anchor:start;white-space:normal;shape-padding:0;clip-rule:nonzero;display:inline;overflow:visible;visibility:visible;opacity:1;isolation:auto;mix-blend-mode:normal;color-interpolation:sRGB;color-interpolation-filters:linearRGB;solid-color:#000000;solid-opacity:1;vector-effect:none;fill:#f0f0f0;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:3.99999976;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:8;stroke-opacity:1;paint-order:stroke fill markers;color-rendering:auto;image-rendering:auto;shape-rendering:auto;text-rendering:auto;enable-background:accumulate"
      d="M 15.996094 2 C 12.706681 2 10.001953 4.7106393 10.001953 8 L 10.001953 10
      L 8 10 C 4.7105924 10 2 12.710602 2 16 L 2 56 C 2 59.289398 4.7105924 62 8 62 L 15.996094 62 A 2.0001999 2.0001999 0 1 0 15.996094 58 L 8 58 C 6.8574465 58 6 57.142551 6 56 L 6 16 C 6 14.857449 6.8574465 14 8 14 L 10.001953 14 L 10.001953 16.001953 C 10.001953 19.291352 12.706704 21.996094 15.996094 21.996094 C 19.285484 21.996094 21.998047 19.291352 21.998047 16.001953 L 21.998047 14.001953 L 25.998047 14.001953 L 25.998047 16.001953 C 25.998047 19.291352 28.710609 21.996094 32 21.996094 C 35.28939 21.996094 38.001953 19.291352 38.001953 16.001953 L 38.001953 14.001953 L 42.003906 14.001953 L 42.003906 16.001953 C 42.003906 19.291352 44.706703 21.996094 47.996094 21.996094 C 51.285481 21.996094 53.998047 19.291389 53.998047 16.001953 L 53.998047 14 L 56 14 C 57.142555 14 58 14.857449 58 16 L 58 56 C 58 57.142551 57.142555 58 56 58 L 32 58 A 2.0001999 2.0001999 0 1 0 32 62 L 56 62 C 59.28941 62 62 59.289398 62 56 L 62 16 C 62 12.710602 59.28941 10 56 10 L 53.998047 10 L 53.998047 8 C 53.998047 4.7106393 51.285504 2 47.996094 2 C 44.70668 2 42.003906 4.7106393 42.003906 8 L 42.003906 10.001953 L 38.001953 10.001953 L 38.001953 8 C 38.001953 4.7106393 35.289413 2 32 2 C 28.710587 2 25.998047 4.7106393 25.998047 8 L 25.998047 10.001953 L 21.998047 10.001953 L 21.998047 8 C 21.998047 4.7106393 19.285507 2 15.996094 2 z M 15.996094 6 C 17.13868 6 17.996094 6.8574488 17.996094 8 L 17.996094 16.001953 C 17.996094 17.14458 17.138703 18.003906 15.996094 18.003906 C 14.853484 18.003906 14.003906 17.14458 14.003906 16.001953 L 14.003906 8 C 14.003906 6.8574488 14.853507 6 15.996094 6 z M 32 6 C 33.142586 6 34.001953 6.8574488 34.001953 8 L 34.001953 16.001953 C 34.001953 17.14458 33.142609 18.003906 32 18.003906 C 30.85739 18.003906 30 17.14458 30 16.001953 L 30 8 C 30 6.8574488 30.857413 6 32 6 z M 47.996094 6 C 49.138675 6 49.998047 6.8574488 49.998047 8 L 49.998047 16.001953 C 49.998047 17.14458 49.138698 18.003906 47.996094 18.003906 C 46.853482 18.003906 45.996094 17.14458 45.996094 16.001953 L 45.996094 8 C 45.996094 6.8574488 46.853505 6 47.996094 6 z M 12.003906 25.998047 A 2.000504 2.000504 0 0 0 12.003906 29.998047 L 51.998047 29.998047 A 2.000504 2.000504 0 1 0 51.998047 25.998047 L 12.003906 25.998047 z M 24 34 A 1.9999999 1.9999999 0 0 0 22 36 A 1.9999999 1.9999999 0 0 0 24 38 A 1.9999999 1.9999999 0 0 0 26 36 A 1.9999999 1.9999999 0 0 0 24 34 z M 32 34 A 1.9999999 1.9999999 0 0 0 30 36 A 1.9999999 1.9999999 0 0 0 32 38 A 1.9999999 1.9999999 0 0 0 34 36 A 1.9999999 1.9999999 0 0 0 32 34 z M 40 34 A 1.9999999 1.9999999 0 0 0 38 36 A 1.9999999 1.9999999 0 0 0 40 38 A 1.9999999 1.9999999 0 0 0 42 36
      A 1.9999999 1.9999999 0 0 0 40 34 z M 48 34 A 1.9999999 1.9999999 0 0 0 46 36 A 1.9999999 1.9999999 0 0 0 48 38 A 1.9999999 1.9999999 0 0 0 50 36 A 1.9999999 1.9999999 0 0 0 48 34 z M 16 42 A 1.9999999 1.9999999 0 0 0 14 44 A 1.9999999 1.9999999 0 0 0 16 46 A 1.9999999 1.9999999 0 0 0 18 44 A 1.9999999 1.9999999 0 0 0 16 42 z M 24 42 A 1.9999999 1.9999999 0 0 0 22 44 A 1.9999999 1.9999999 0 0 0 24 46 A 1.9999999 1.9999999 0 0 0 26 44 A 1.9999999 1.9999999 0 0 0 24 42 z M 32 42 A 1.9999999 1.9999999 0 0 0 30 44 A 1.9999999 1.9999999 0 0 0 32 46 A 1.9999999 1.9999999 0 0 0 34 44 A 1.9999999 1.9999999 0 0 0 32 42 z M 40 42 A 1.9999999 1.9999999 0 0 0 38 44 A 1.9999999 1.9999999 0 0 0 40 46 A 1.9999999 1.9999999 0 0 0 42 44 A 1.9999999 1.9999999 0 0 0 40 42 z M 48 42 A 1.9999999 1.9999999 0 0 0 46 44 A 1.9999999 1.9999999 0 0 0 48 46 A 1.9999999 1.9999999 0 0 0 50 44 A 1.9999999 1.9999999 0 0 0 48 42 z M 16 50 A 1.9999999 1.9999999 0 0 0 14 52 A 1.9999999 1.9999999 0 0 0 16 54 A 1.9999999 1.9999999 0 0 0 18 52 A 1.9999999 1.9999999 0 0 0 16 50 z M 24 50 A 1.9999999 1.9999999 0 0 0 22 52 A 1.9999999 1.9999999 0 0 0 24 54 A 1.9999999 1.9999999 0 0 0 26 52 A 1.9999999 1.9999999 0 0 0 24 50 z M 32 50 A 1.9999999 1.9999999 0 0 0 30 52 A 1.9999999 1.9999999 0 0 0 32 54 A 1.9999999 1.9999999 0 0 0 34 52 A 1.9999999 1.9999999 0 0 0 32 50 z M 40 50 A 1.9999999 1.9999999 0 0 0 38 52 A 1.9999999 1.9999999 0 0 0 40 54 A 1.9999999 1.9999999 0 0 0 42 52 A 1.9999999 1.9999999 0 0 0 40 50 z M 24 58 A 1.9999999 1.9999999 0 0 0 22 60 A 1.9999999 1.9999999 0 0 0 24 62 A 1.9999999 1.9999999 0 0 0 26 60 A 1.9999999 1.9999999 0 0 0 24 58 z " transform="matrix(0.26458333,0,0,0.26458333,0,280.06669)">
  </path>
</g>
</svg>
</center>



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
