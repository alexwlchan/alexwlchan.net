---
layout: til
date: 2024-02-28 10:15:24 +00:00
date_updated: 2024-06-12 10:58:07 +01:00
title: Get my Netlify bandwidth usage from the API
tags:
  - netlify
---
I wanted to add a little graph showing my Netlify usage to my analytics dashboard.
You can see this in the Netlify dashboard, but I log in to that rarely so it's not helpful:

{%
  picture
  filename="netlify-usage.png"
  width="204"
  class="screenshot"
  alt="A screenshot from the Netlify dashboard showing I've used 25GB of 100GB in the current period."
%}

I used the Netlify API to get the data and show it in another dashboard.

1.  I created a personal access token [in my user settings](https://app.netlify.com/user/applications/personal).

2.  I got my Netlify team identifier from the URL of my settings page (`https://app.netlify.com/teams/<team_id>/settings/general`).

3.  I called the Netlify API to get the data:

    ```console
    $ curl -H 'Authorization: Bearer <TOKEN>' 'https://api.netlify.com/api/v1/accounts/<team_slug>/bandwidth' | jq .
    {
      "used": 27167800363,
      "included": 107374182400,
      "additional": 0,
      "last_updated_at": "2024-03-10T15:15:03.237+00:00",
      "period_start_date": "2024-02-17T00:00:00.000-08:00",
      "period_end_date": "2024-03-17T00:00:00.000-07:00"
    }
    ```

A couple of observations on the data you get back:

*   The `included`/`used` values are measured in gibibytes, not gigabytes.
    107374182400 is 100 GiB, but 107.4 GB.

*   This value gets cached for a while -- in the example above, I called the API at 15:22 but the `last_updated_at` value is 15:03.
    I'm not sure how often the value is updated.

## Being a responsible user of the API

*   The API returns a `Retry-After` value, which is a minute after your request.
    This is a clue about how often the value gets updated -- it's definitely not second-level granularity.

    ```console
    $ curl -v -H 'Authorization: Bearer <TOKEN>' 'https://api.netlify.com/api/v1/accounts/<team_slug>/bandwidth'
    …
    < HTTP/2 200
    < date: Wed, 12 Jun 2024 09:52:37 GMT
    …
    < retry-after: 2024-06-12 09:53:37 UTC
    …
    ```

*   The responses include an `ETag` header, which you can use to check if the value has changed since the last request:

    ```console
    $ curl -v -H 'Authorization: Bearer <TOKEN>'  'https://api.netlify.com/api/v1/accounts/<TEAM_SLUG>/bandwidth'
    …
    < HTTP/2 200
    < etag: W/"190b2e3e6d8c239bd546819b0f0b1eb9"
    …

    $ curl -v  -H 'If-None-Match: W/"190b2e3e6d8c239bd546819b0f0b1eb9"' -H 'Authorization: Bearer <TOKEN>' 'https://api.netlify.com/api/v1/accounts/<TEAM_SLUG>/bandwidth'
    < HTTP/2 304
    …
    ```
    
    Annoyingly, this doesn't make the API any faster -- responses still take about half a second, even if nothing has changed.
