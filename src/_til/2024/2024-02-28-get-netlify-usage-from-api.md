---
layout: til
date: 2024-02-28 10:15:24 +0000
title: Get my Netlify bandwidth usage from the API
tags:
  - netlify
---
I wanted to add a little graph showing my Netlify usage to my analytics dashboard.
You can see this in the Netlify dashboard, but I log in to that rarely so it's not helpful:

<img src="/images/2024/netlify-usage.png" style="width: 204px;" class="screenshot" alt="A screenshot from the Netlify dashboard showing I've used 25GB of 100GB in the current period.">

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
