---
layout: post
date: 2020-06-06 06:38:11 +0000
title: Finding the months between two dates in Python
category: Python
---

Here's a function extracted from a recent project that I'm likely to reuse elsewhere: finding all the months between two dates in Python.

I often use this when I want to aggregate some time-based data into per-month buckets, to produce a high-level summary.
For example, let's suppose I had a list of how many steps I'd walked each day.
I might combine that data to get the total number of steps walked each month.

The function is a generator.
Here's a quick summary of how it works:

1.  Find the month/year of the start date
2.  Get the 1st of that month -- yield this date to the user (as a lazy generator)
3.  Advance the month by one, wrapping around to the next year as appropriate
4.  Get the 1st of that month -- yield this date
5.  Repeat steps 3 and 4 until the date is after the end date

Once I have these values, typically I'll then pull out the month/year value as numbers, or call `strftime()` to turn it into a pretty string.

If you look, you'll see I'm incrementing the `month`/`year` on the datetime objects by hand.
The Python standard library does have a [datetime.timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta) object for incrementing or decrementing a datetime object, rather than manipulating `month`/`year` directly, but at the month and year level there's a lot of weirdness to deal with.

For example, if you're at March 30th, and you go back by one month – what should you get?
Or if you're at February 29th in a leap year, and you want to go forward by two years – what should the code do?
The correct behaviour is going to depend on our context, so the standard library defers these decisions to us.

If this function sounds useful, you can copy/paste the code below into your project:

```python
import datetime


def months_between(start_date, end_date):
    """
    Given two instances of ``datetime.date``, generate a list of dates on
    the 1st of every month between the two dates (inclusive).

    e.g. "5 Jan 2020" to "17 May 2020" would generate:

        1 Jan 2020, 1 Feb 2020, 1 Mar 2020, 1 Apr 2020, 1 May 2020

    """
    if start_date > end_date:
        raise ValueError(f"Start date {start_date} is not before end date {end_date}")

    year = start_date.year
    month = start_date.month

    while (year, month) <= (end_date.year, end_date.month):
        yield datetime.date(year, month, 1)

        # Move to the next month.  If we're at the end of the year, wrap around
        # to the start of the next.
        #
        # Example: Nov 2017
        #       -> Dec 2017 (month += 1)
        #       -> Jan 2018 (end of year, month = 1, year += 1)
        #
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1


if __name__ == "__main__":
    start_of_2020 = datetime.date(2020, 1, 1)
    today = datetime.date.today()

    for month in months_between(start_of_2020, today):
        print(month.strftime("%B %Y"))
        # January 2020, February 2020, March 2020, …
```
