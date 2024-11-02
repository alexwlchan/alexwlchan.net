---
layout: post
title: Moving my website from Netlify to Caddy
summary: |
  To avoid getting stung by Netlify's bandwidth charges, I moved this site to a Linux server running Caddy as my web server.
tags:
  - blogging about blogging
  - caddy
  - netlify
---
I had a long train journey on Tuesday, and I spent part of it moving this website from Netlify to a Linux server running [Caddy].
(Yes, the Wi-Fi on European trains is reliable enough to make that possible, even pleasant.)

Hopefully nobody noticed!
When I flipped the DNS records to point at the new server, there was only about a minute of downtime, and everything should be working as before.

I wanted to write a few notes on the experience.

[Caddy]: https://caddyserver.com/



## Why did I want to move away from Netlify?

I'm feeling the squeeze of Netlify's bandwidth pricing.

I was on their [Starter plan], so I got 100GB of bandwidth per month, for free.
If I exceeded that, I'd have to pay $55 for an extra 100GB of bandwidth.
That was fine for several years because I was well under the limit, but my usage has been creeping up and I've been stung by a couple of overage charges.
Maybe I've got more readers; maybe the site is getting crawled by AI bots.

I've tried to make this site as lightweight as possible, to minimise my bandwidth.
I serve small HTML pages, I cache aggressively, and I compress all my images.
But there's only so much I can do, and if a post gets popular, the bandwidth starts to stack up.

This has been particularly pronounced in the last week – my recent post [Using static websites for tiny archives] was on the front page of Hacker News for about a day.
The extra visitors pushed me close to the limit – 5 days into my 30-day billing period, and I'd used over 80% of my bandwidth allowance.
The threat of another overage charge is what pushed me to make this change now.

I don't object to paying for bandwidth -- it's using resources somewhere and I'm happy to pay my fair share.
But Netlify's pricing is *egregious*.
Charging $0.55/GB is far more than their competitors.
Even AWS, who are notorious for their bandwidth pricing, typically charge less than a third of that.
(My new web server is hosted on Linode, which charges [a mere $0.005/GB][linode].)

I run this website for fun.
I don't get any money from it, and I don't want to pay $55 every other month because something I wrote got popular.
I needed a cheaper host.

[Starter plan]: https://www.netlify.com/pricing/#pricing-table
[Using static websites for tiny archives]: /2024/static-websites/
[linode]: https://techdocs.akamai.com/cloud-computing/docs/network-transfer-usage-and-costs#usage-costs

## Why did I pick Caddy?

Before Netlify, I ran this website on a Linux VPS with Nginx as the web server.
That worked fine, but I remember it being fiddly to set up HTTPS certificates.
I'm fairly sure I had some config bugs as well, because it was much slower than I expected.
Nginx is a powerful web server that should have no issues running my dinky little site, but I'd done something to make it sluggish.

If I was replacing Netlify, I wanted to go back to running a web server on a Linux boox -- I'm fairly comfortable running my own servers, and I'd rather not go to a different proprietary vendor.
Plus I was already paying for a web server for some other projects, so moving this site there wouldn't cost me anything extra.
But I didn't fancy going back to Nginx.

I'd had [Caddy] recommended to me on Twitter a couple of times, I knew it would manage my HTTPS certificates, and it was easy to install.
I got a basic site up and running quickly, and that was enough to try doing the whole thing.

Caddy seems fine for now, and I'm not too worried about finding issues later.
If I do decide to siwtch to something different, I've just done a server-to-server migration and it was pretty smooth.
I'm sure I could do the same again.

[Caddy]: https://caddyserver.com/

## Writing some tests as a safety net

I wanted to make sure I didn't break anything when I moved the site, so I wrote some tests before I made any changes.
A good test suite can catch mistakes, and gives me the peace of mind that nothing is obviously wrong.

My new tests check the behaviour of the live website -- they make requests to `alexwlchan.net` and inspect the responses.

I wrote tests for things like:

*   Are pages being served properly?
*   Are images being served properly?
*   If a page has been redirected, are you sent to the right place?
*   If I've removed a page, does it get the correct HTTP [410 Gone](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/410) response?
*   Are my HTTPS certificates renewing correctly?
*   Am I setting the right HTTP headers on responses? (e.g. for caching)

If you're interested, you can see the complete test suite [on GitHub](https://github.com/alexwlchan/alexwlchan.net/tree/main/tests).

Although I wrote these tests to be a safety net while I was making changes, I'm going to keep them around.
I've created a GitHub Action to run them on a regular schedule, so I can be alerted if anything breaks in future.

## How I did the migration

I run this site at `alexwlchan.net`, but I have a couple of alternative domains and subdomains that I redirect to the same site, like `alexwlchan.co.uk` and `www.alexwlchan.net`.

I set up Caddy on my Linux server, and configured it to serve a basic copy of this website at `www.alexwlchan.net`.
I used the [quick start] in the Caddy docs to write my initial configuration, and I updated the DNS record for `www.alexwlchan.net` to point at my web server.

Then I ran my new tests against this version of the site.
Lots of the tests failed, because I only had a starter configuration.
But then I started porting all my server config to Caddy, and gradually tests started passing.
When all the config was ported and all the tests were passing, I knew I was ready to go.

I updated my Caddyfile to start serving `alexwlchan.net`, and I changed the DNS records to point `alexwlchan.net` at my web server.
It took a minute or so for Caddy to get an HTTPS certificate, and then everything was coming from the new domain.

Bit more fiddling with GitHub Actions to deploy site

[quick start]: https://caddyserver.com/docs/quick-starts/static-files

## Reflections

Everything seems to have migrated correctly, and nothing is obviously broken.

Caddy wasn't too tricky to set up.
It definitely lacks the breadth of example config, compared to the more popular web servers like Apache or Nginx -- but the same was true when I was writing my Netlify config.
The first-party docs were pretty detailed though, and I was able to work out everything I wanted to do.
It's nice to be back writing complete web server configuration, and not trying to shoehorn everything into Netlify's more limited config.
When it's more settled, I'll wrote some [today I learned](/til/) posts about my Caddy config.

Running my own web server is definitely easier than the last time I tried it.
The near-universal deployment of HTTPS is broadly a good thing, but it did introduce some friction for a while.

Netlify is still easier, and it's what I'd recommend if you're getting started -- but I'm glad the DIY approach is improving.
More ways for individuals to run their own websites is only a good thing for the open web.
