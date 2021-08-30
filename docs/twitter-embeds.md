For embedded tweets, rather than using Twitter's embed function (which comes with all sorts of JavaScript and tracking and slowness), I render tweets as static HTML.
This is an idea I originally got [from Dr. Drang][drangtweet].

To embed a tweet in a post, I use the following tag:

```plain
{% tweet https://twitter.com/iamkimiam/status/848188958567800832 %}
```

When the site is built, I have [a personal plugin](src/_plugins/twitter.rb) that:

*   Polls the Twitter API
*   Caches the complete API response and a copy of the author's avatar
*   Uses the cached API response and a template to render an HTML snippet

Polling the Twitter API requires a set of API tokens, but I check in the cached responses (see `_tweets`).
This means that I can fetch the tweet data on a local machine, but when I push to CI, it doesn't need my credentials to render the tweet.

Because I render the tweets at compile time, I can change the appearance of old tweets by updating the template, without having to edit old posts.
That's part of why I keep the entire API response – in case I later need data I'd thrown away the first time.

[drangtweet]: http://www.leancrew.com/all-this/2012/07/good-embedded-tweets/
