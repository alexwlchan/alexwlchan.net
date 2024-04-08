---
layout: til
date: 2024-03-16 08:39:19 +0000
title: How much will Mastodon instances try to re-send messages?
tags:
  - mastodon
---
Simon Willison had some DNS issues which meant his personal Mastodon instance (which is similar to my Masto.host setup) was knocked offline for a day or so.
He was [wondering whether](https://fedi.simonwillison.net/@simon/112100279854237102) this would cause a flood of traffic when it came back online:

> I wonder how much of an impact this had on the invisible Mastodon infrastructure...
>
> Every time someone I follow posted in the past 24 hours their instance would have tried and failed to deliver to my instance - how hard do these things get retried?
>
> Am I about to see a massive flood of incoming deliveries that finally work?

And there were a couple of replies to his post, explaining what would happen, including a link to the relevant part of the Mastodon codebase -- if a job fails, it gets retried with an exponential delay.

[clifff](https://shakedown.social/@clifff/112100294144816566) (15 March 2024):

> @simon by default, sidekiq jobs that throw an error will be retried 25 times over the course of 20 days <https://github.com/sidekiq/sidekiq/wiki/Error-Handling#automatic-job-retry>
>
> it's possible mastodon has customized this but I haven't specifically looked. would expect you'll get more traffic than usual but shouldn't be all at once

[Jason Culverhouse](https://flipboard.social/@JsonCulverhouse/112101163947801880) (15 March 2024):

> @cliff @simon
>
> Here is the retry algorithm, if you were down a day.  They will trickle in vs a massive flood
>
> ```ruby
> (0..16).each do |count|
>   delay = (count**4) + 15
>   jitter = rand(0.5 * (count**4))
>   total_delay = delay + jitter
>   puts "Retry #{count}: #{total_delay} seconds"
> end
> ```
>
> Retry 0: 15.713002155688077 seconds<br>Retry 1: 16.48915648567112 seconds<br>Retry 2: 31 seconds<br>Retry 3: 124 seconds<br>Retry 4: 382 seconds<br>Retry 5: 938 seconds<br>Retry 6: 1319 seconds<br>Retry 7: 2617 seconds<br>Retry 8: 6006 seconds<br>Retry 9: 9468 seconds<br>Retry 10: 12612 seconds<br>Retry 11: 19804 seconds<br>Retry 12: 26167 seconds<br>Retry 13: 31795 seconds<br>Retry 14: 55286 seconds<br>Retry 15: 67782 seconds<br>Retry 16: 89823 seconds
>
> <https://github.com/mastodon/mastodon/blob/71e5f0f48c3bc95a894fa3ad2c5a34f05c584482/app/workers/activitypub/delivery_worker.rb/#L13-L21>
