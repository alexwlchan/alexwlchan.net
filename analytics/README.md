# analytics

This directory contains the script for parsing analytics information from my nginx logs.

All my pages embed a small analytics script.
If the user has JavaScript enabled and Do Not Track is false, that script calls a tracking pixel, including the page's referrer, title and URL in the query parameters.
This shows up as a series of requests for `a.gif` in my nginx logs.

When I want to get an analytics report, I SSH on to my server, and I run the command:

```console
$ make analytics-report
```

This reads logs from the nginx container that runs the site, parses out interesting stats, and prints a report to stdout.
This includes:

*   A list of the most popular pages and the site
*   How many visits, and how many unique IPs I had
*   A list of common referrers
*   Any 404 or server errors
