---
layout: post
title: Falsehoods programmers believe about Unix time
summary:
tags:
category: Programming and code
---

With apologies to [Patrick McKenzie].

[Danny] was asking us about our favourite facts about [Unix time] in the Wellcome Slack yesterday, and I was reminded of the way that it behaves in some completely counter-intuitive ways.

These three facts all seem eminently sensible and reasonable, right?

1.  Unix time is the number of seconds since 1 January 1970 00:00:00 UTC
2.  If I wait exactly one second, Unix time advances by exactly one second
3.  Unix time can never go backwards

False, false, false.

But it's unsatisfying to say "this is false" without explaining *why*, so I'll explain that below.
If you'd like to think about it first and make your own guess, don't scroll past the picture of the clock!

<figure>
  <img src="/images/2019/L0072180.jpg">
  <figcaption>
    A bracket clock.
    Construction and assembly by John Leroux.
    Credit: <a href="https://wellcomecollection.org/works/t8v9t648">Wellcome Collection</a>.
    Used under <a href="https://creativecommons.org/licenses/by/4.0/">CC&nbsp;BY</a>.
  </figcaption>
</figure>

All three of these falsehoods have the same underlying cause: *[leap seconds]*.
If you're unfamiliar with leap seconds, here's a brief primer:

There are two factors that make up UTC:

*   [International Atomic Time], which is an average of hundreds of atomic clocks spread around the globe.
    We can measure a second from the electromagnetic properties of an atom, and it's the most accurate measurement of time known to science.

*   [Universal Time], which is based on the Earth's rotation about its own axis.
    One complete rotation is one day.

Problem is, these two numbers don't always match.
The Earth's rotation isn't consistent -- it's gradually slowing down, so days in Universal Time are getting longer.
Atomic clocks, on the other hand, are fiendishly accurate, and consistent for millions of years.

When the two times drift apart, a leap second is added or removed to UTC to bring them back together.
Since 1972, [the IERS] \(who manage this stuff) have inserted an extra 27 leap seconds.
The result is a UTC day with 86,401 seconds (one extra), or 86,399 (one missing) -- both of which mess with a fundamental assumption of Unix time.

Unix time assumes that each day is exactly 86,400 seconds long (60&nbsp;&times;&nbsp;60&nbsp;&times;&nbsp;24&nbsp;=&nbsp;86,400), leap seconds be damned.
If there's a leap second in a day, Unix time either repeats or omits a second as appropriate to make them match.
As of 2019, the extra 27 leap seconds are missing.

And so our falsehoods go as follows:

*   Unix time is the number of seconds since 1 January 1970 00:00:00 UTC, *minus leap seconds*.

*   If I wait exactly one second, Unix time advances by exactly one second, *unless a leap second has been removed*.

    So far, there's never been a leap second removed in practice (and the Earth's slowing rotation means it's unlikely), but if it ever happened, it would mean the UTC day is one second shorter.
    The last UTC second (23:59:59) is dropped.

    Each Unix day has the same number of seconds, so when the next day starts, it skips ahead by one.
    The final Unix second of the shorter day never gets allocated to a UTC timestamp.
    Here's what that would look like, in quarter-second increments:

    <img src="/images/2019/unix_time_skips_forwards.png" style="width: 612px;">

    If you start at 23:59:58:00 UTC and wait one second, the Unix time advances by *two* seconds, and the Unix timestamp 101 never gets assigned.

*   Unix time can never go backwards, *unless a leap second has been added*.

    This one has happened in practice -- 27 times at time of writing.
    The UTC day gets an extra second added to the end, 23:59:60.
    Each Unix day has the same number of seconds, so it can't just add an extra second -- instead, it repeats the Unix timestamps for the last second of the day.
    Here's what that would look like, in quarter-second increments:

    <img src="/images/2019/unix_time_goes_backwards.png" style="width: 612px;">

    If you start at 23:59:60.50 and wait half a second, the Unix time goes *back* by half a second, and the Unix timestamp 101 matches two UTC seconds.

And these probably aren't even the only weirdnesses of Unix time -- they're just the ones I half-remembered yesterday, enough to check a few details and write a blog post about.

Time is *straaaaaange*.

[Patrick McKenzie]: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
[Danny]: https://twitter.com/dannybirchall
[Unix time]: https://en.wikipedia.org/wiki/Unix_time
[leap seconds]: https://en.wikipedia.org/wiki/Leap_second
[International Atomic Time]: https://en.wikipedia.org/wiki/International_Atomic_Time
[Universal Time]: https://en.wikipedia.org/wiki/Universal_Time
[the IERS]: https://en.wikipedia.org/wiki/International_Earth_Rotation_and_Reference_Systems_Service
