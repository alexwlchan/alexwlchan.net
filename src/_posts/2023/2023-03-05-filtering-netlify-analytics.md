---
layout: post
date: 2023-03-05 12:33:07 +00:00
title: Filtering out bogus requests from Netlify Analytics
summary: Using redirects to filter out bots trying to hack my non-existent PHP installation.
tags:
  - blogging about blogging
  - netlify
colors:
  index_light: "#73714B"
  index_dark:  "#c9ba8d"
card_attribution: https://www.pexels.com/photo/large-elephants-near-lake-86413/, CC0
---

I host this site on Netlify, and I pay for [Netlify Analytics] to monitor its performance.
It's essentially server-side logging with a dashboard on top, and it's more than sufficient for the very limited analytics I want to do here.

One of the dashboard panels is "resources not found", which tells me which URLs are 404'ing on the site.
For example, I changed a bunch of URLs at the end of last year, and I tried to redirect all the old URLs -- this table tells me about anything I missed.

{%
  picture
  filename="netlify-resources-not-found.png"
  width="549"
  alt="A table titled 'Top resources not found' followed by a list of paths and a request count. The resources not found include /index.php/PHP%0ABonusChallengeExploits.php, /images/2022/guest_headers_card.png, /talks/hypothesis-intro/hypothesis-slide029.png and /.well-known/traffic-advice."
  class="screenshot"
%}

Sometimes this table contains useful data -- like the fact that I have two images I didn't redirect, which still get several hundred hits a month (<a href="/images/2022/guest_headers_card.png" data-proofer-ignore>fixed</a>, <a href="/talks/hypothesis-intro/hypothesis-slide029.png" data-proofer-ignore>fixed</a>).
But a lot of the hits are from malicious bots, crawling the web for vulnerable PHP or WordPress installations.
Since I don't run PHP, I'm not worried about them breaking anything; these errors are just noise.

To filter these requests out of the table, I've created a bunch of redirects [in my `_redirects` file][redirects].
I'm matching on a handful of these patterns using wildcards, and sending them all to an HTTP 400 page with an HTTP 400 status code:

```
/wp-*                       /400/ 400

/blog/wp-*                  /400/ 400
/cms/wp-*                   /400/ 400
/site/wp-*                  /400/ 400
/wordpress/wp-*             /400/ 400
/wp/wp-*                    /400/ 400
/wp2/wp-*                   /400/ 400

/index.php*                 /400/ 400
```

(That HTTP 400 error page is also tiny – a mere 23 bytes – to avoid wasting any unnecessary bandwidth on these Internet leeches.)

Because these requests are now getting an HTTP 400 instead of HTTP 404, they stop appearing in the "Top resources not found" table.

Using wildcards keeps this list manageable – with a few lines I can discard the majority of requests, rather than playing a game of whack-a-mole with every PHP URL somebody thinks to try.

It'd be nice if Netlify could do this for me, because this sort of crawling is incredibly common and filtering these requests out would improve this table for a lot of their customers -- but in the meantime, a handful of redirects does the trick.

[Netlify Analytics]: https://docs.netlify.com/monitor-sites/analytics/
[redirects]: https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file
