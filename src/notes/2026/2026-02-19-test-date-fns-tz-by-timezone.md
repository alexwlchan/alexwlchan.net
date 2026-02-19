---
layout: note
title: Testing date formatting with date-fns-tz and different timezones
summary: Override the `TZ` environment variable in your tests.
date: 2026-02-19 08:47:15 +00:00
topics:
  - JavaScript
  - Datetime shenanigans
---
I was reading some code which formatted dates using the [`format` function][date-fns-tz-format] from the [`date-fns-tz` library][date-fns-tz].
Here's an example:

```javascript {"names":{"1":"format","2":"formatDate","3":"date"}}
import { format } from "date-fns-tz"

/* formatDate returns the given date as a date string, with a 12-hour
 * timestamp and the timezone. Example: Jan 2, 2006 - 10:04 PM GMT. */
export function formatDate(date: Date): string {
  return format(date, "MMM d, y - p z")
}
```

If I tested the code in Chrome by [changing the browser timezone][chrome-browser-tz], I could see it behaving correctly -- the displayed time would change to match my current timezone.

I wanted to write an automated test to check this behaviour.

## Option 1: Pass the timezone to `format()` in `OptionsWithTZ` 

The `format()` function accepts an optional third argument `options: OptionsWithTZ`, which can include a timezone.
If I allowed passing a timezone to `formatDate()`, I could pass it to `format()`.

However, that would mean changing the function.
This code didn't have any existing tests, and I don't like changing code at the same time I add tests -- it's too easy to introduce a change unexpectedly, and codify the wrong behaviour in your new tests.

I prefer to add tests that check the existing behaviour, merge them to main, and only then start changing the implementation.

## Option 2: Mock the `TZ` environment variable

If you don't give `format()` an explicit timezone, it guesses one based on your environment.
In my Node tests, it was enough to mock the value of the `TZ` environment variable with different timezones, and watch the value change.

Here's an example using vitest:

```javascript {"names":{"1":"afterEach","2":"describe","3":"expect","4":"it","5":"vi","6":"formatDate","8":"d","10":"testCases","11":"tz","13":"expected","30":"tz","31":"expected"}}
import { afterEach, describe, expect, it, vi } from "vitest"
import { formatDate } from "./dates"

describe("formatDate", () => {
  const d = new Date("2006-01-02T15:04:05-0700")
   
  const testCases: { tz: string, expected: string | Regexp }[] = [
    { tz: "America/Los_Angeles", expected: /Jan 2, 2006 - 2:04 PM (GMT-8|PST)/ },
    { tz: "Europe/London",       expected: "Jan 2, 2006 - 10:04 PM GMT"        },
    { tz: "Asia/Kolkata",        expected: "Jan 3, 2006 - 3:34 AM GMT+5:30"    },
    { tz: "Pacific/Auckland",    expected: "Jan 3, 2006 - 11:04 AM GMT+13"     },
  ]

  afterEach(() => vi.unstubAllEnvs())

  it.each(testCases)("formats date for $tz as $expected", ({ tz, expected }) => {
    vi.stubEnv("TZ", tz)
    expect(formatDate(d)).toMatch(expected)
  })
})
```

Notes:

*   My example date is the reference time used for [formatting dates in Go][go-reference-date].
*   The way timezones are displayed can vary across platforms, hence the `Regexp`.
    On my Mac, Los Angeles time is `GMT-8`, but in the Linux CI worker, it's `PST`.
*   I wonder if this test will break when the clocks change in one of the locations, but I think it will be fine.
    The UTC offset in those locations on that day isn't going to change.
    I'll update this note if the code breaks.

[chrome-browser-tz]: https://stackoverflow.com/a/60008052
[date-fns-tz]: https://github.com/marnusw/date-fns-tz
[date-fns-tz-format]: https://github.com/marnusw/date-fns-tz?tab=readme-ov-file#format
[go-reference-date]: https://pkg.go.dev/time#pkg-constants
