---
layout: post
title: Showing human-friendly dates in JavaScript
summary: What's a nicer way to show a date than an ISO 8601 timestamp?
category: Programming and code
---

At work, we have an API for tracking the state of ingests in [our digital archive].
An ingest is a request to store new files in the archive.
An ingest includes timestamps to record when it started, when it was being processed, and when it was successfully stored.

When you get an ingest from the API, the response includes the timestamps as [ISO 8601 strings].
For example:

```
2020-05-24T11:17:00Z
```

The suffix "Z" tells us this is a [UTC date string][UTC].
You should always store datetimes as UTC -- handling local timezones on servers is a world of pain -- but you don't always need to expose that in the presentation layer.
UTC, ISO-compliant timestamps are great for computers, but they're not so easy for humans to read.

We have a small dashboard for people to view the state of ingests, and I wanted to replace these timestamps with ones that are a bit more human-friendly.
That means things like:

*   **Localising to the user's timezone**.
    Don't force the user to remember whether to add or subtract an hour.

*   **Including a hint if it's a recent timestamp.**
    A complete timestamp is helpful if you have a clock, but "just now" or "5 minutes ago" is often easier to read and conveys enough info.

*   **Including hints for the date.**
    Most ingests are processed within a working day, and "today" or "yesterday" is easier to understand than remembering the exact date.
    I'm also including the day of the week, so it's easier to correlate with other events.
    For example, you might remember "that's the ingest I sent on Tuesday" before the numeric date.

*   **Reducing the granularity of timestamps on older ingests.**
    Second- or minute-level granularity is useful for an ingest I’ve just started, but less useful for an ingest that completed six months ago.
    (I haven't implemented this yet, but I'm considering it.)

I'm sure there are JavaScript libraries that can do this, but in the dashboard I'm just using vanilla JS, so I wrote my own function.
It's short, it does the job, and it's already reduced confusion between UTC and BST.

If you want to use it yourself, you can [download the file](/files/2020/human_friendly_dates.js), or read my code below:

{% inline_code javascript _files/2020/human_friendly_dates.js %}

[our digital archive]: https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e
[UTC]: https://en.wikipedia.org/wiki/Coordinated_Universal_Time
[ISO 8601 strings]: https://en.wikipedia.org/wiki/ISO_8601


