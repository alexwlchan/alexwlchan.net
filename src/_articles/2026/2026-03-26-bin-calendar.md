---
layout: article
title: Creating a personalised bin calendar
date: 2026-03-26 17:33:58 +00:00
topics:
  - Domestic life
  - Python
---
Every spring, my council publish a new bin collection calendar.
These calendars are typically published as a single PDF to cover the entire region, with the information packed into a compact design.
I imagine this design is for economy of printing -- you can print one calendar in bulk, and post the same thing to everybody.

Here's an example of this sort of compact diagram from [South Cambridge][cam-bins], where breaks the county into four different regions:

<figure>
  {%
    picture
    filename="scambs_bins.png"
    width="750"
    class="screenshot"
  %}
  <figcaption>
    I haven’t lived in South Cambridge for over eight years so this isn’t my calendar, but I don’t want to tell the Internet where I live by linking to a local council.
  </figcaption>
</figure>

For example, if your usual bin day is Thursday, your final collection of the year would be on Monday 22nd December.

This compact representation is a marvel of design, but it's not that useful for me, a person who only lives in a single house.
I only care about bin day on my street, not across the county.

I create a personalised calendar which shows when my bins will be collected, then I print it and stick it on my fridge.
It's a manual process, but a small amount of effort now pays off across the year.


[cam-bins]: https://www.scambs.gov.uk/media/yawnruwn/bin-calendar-autumn-2025-pdf.pdf

---



I start by generating an HTML calendar using Python. There's a built-in module to create calendars, which I customise to an individual ID attributes to each day. Here is a script, which generates a calendar from April 2026 to March 2027:

[[script]]

This gets written to an HTML file, where each month is a table, and each day is an individually identifiable cell:

[[code]]

I have a CSS file that I carry from year to year, which adds a bit of spacing and turns it into a three-up view:

[[css]]

[[screenshot]]
