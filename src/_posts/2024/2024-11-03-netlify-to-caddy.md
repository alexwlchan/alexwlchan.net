---
layout: post
date: 2024-11-03 12:15:30 +00:00
title: Moving my website from Netlify to Caddy
summary: |
  To avoid getting stung by Netlify's bandwidth charges, I moved this site to a Linux server running Caddy as my web server.
tags:
  - blogging about blogging
  - caddy
  - netlify
---
I had a long train journey on Tuesday, and I spent the time moving this website from Netlify to a Linux server running [Caddy].
(Yes, the Wi-Fi on European trains is reliable enough to make that possible, even pleasant.)

Hopefully nobody noticed!
When I flipped the DNS records to point at the new server, there was only about a minute of downtime, and everything should be working as it was before.

These are a few notes on why and how I made this transition.

[Caddy]: https://caddyserver.com/



## Why did I want to move away from Netlify?

I'm feeling the squeeze of Netlify's bandwidth pricing.

I was on their [Starter plan], so I could serve 100GB of bandwidth per month, for free.
If I went over that, I had to buy extra bandwidth packs -- $55 for 100GB.

The 100GB limit was fine for a while, but my bandwidth usage has been creeping up and I've already been stung by several overage charges.
This is particularly pronounced when a post gets popular and I get a big influx of traffic.
I try to make this site as small and lightweight as possible, but that only goes so far.

This has been particularly pronounced in the last week – my recent post [Using static websites for tiny archives] was on the front page of Hacker News for about a day.
I got lots of extra readers, which pushed me close to the limit – 5 days into my 30-day billing period, and I'd used over 80% of my bandwidth allowance.

The threat of another overage charge is what pushed me to make this change now.

I don't object to paying for bandwidth, but Netlify's pricing is egregious.
Charging $0.55/GB is far more than their competitors.
Even AWS, who are notorious for their egress bandwidth pricing, charge [a fraction of that](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer).
(My new web server is hosted at Linode, who charge [a mere $0.005/GB][linode].)

I run this website for fun.
I don't make any money from it, and I don't want to pay $55 every other month because something I wrote got popular.
I needed a cheaper host.

[Starter plan]: https://www.netlify.com/pricing/#pricing-table
[Using static websites for tiny archives]: /2024/static-websites/
[linode]: https://techdocs.akamai.com/cloud-computing/docs/network-transfer-usage-and-costs#usage-costs

## Why did I pick Linux/Caddy?

If I was ditching Netlify, I knew I wanted to go back to a web server on a Linux box.
I ran this site that way for a number of years, I'm comfortable running my own servers, and it's nice not to be as tied to a proprietary vendor.

The web server I'm using is a Linode ["Nanode 1GB" virtual machine](https://www.linode.com/pricing/), which costs $5 a month, including 1TB of bandwidth.
Even a tiny server has plenty of power to serve my website.
Overall this should be cheaper than Netlify, the cost will be more predictable, and it gives me flexibility to do more fun stuff with this site in future.

In the past I used [nginx](https://nginx.org/en/) as my web server software, but it was fiddly to configure, especially the HTTPS certificates.
I wanted to try something different.

Several people had recommended [Caddy] to me on Twitter, so I gave it a look.
It was easy to install and get a basic site running, and it claimed it could handle my HTTPS certificates.
The first-run experience was good enough that I was happy to try getting the whole site on to Caddy.

I didn't look at any alternatives.
Caddy is fine for now, and I'm not too worried about finding issues later.
If I do find a deal-breaker and I need to switch to something different, I've just done a server-to-server migration.
It was pretty smooth.
I'm sure I could do the same again.

[Caddy]: https://caddyserver.com/

## Writing some tests as a safety net

I wanted to make sure I didn't break anything when I moved the site, so I wrote some tests before I made any changes.
A good test suite can catch mistakes, and gives me the peace of mind that nothing is obviously wrong.

I wrote some tests to check the behaviour of the live website -- they make requests to `alexwlchan.net` and inspect the responses.
This includes things like:

* Content delivery:
  * Are pages being served properly?
  * Are images being served properly?

* HTTP behaviour:
  * If a page has been redirected, are you sent to the right place?
  * If I'm removed a page, does it return the correct HTTP [410 Gone](/410/) response?
  * If a page is missing, do you get my custom HTTP [404 Not Found](/404/) page?
  * Am I setting the right HTTP headers to cache images and files?

* Security:
  * Are HTTPS certificates renewing correctly?
  * Am I setting the right [HTTP security headers](https://securityheaders.com/)?

These tests actually uncovered several mistakes in the way I'd set up the site on Netlify, which I fixed before moving on.

If you're interested, you can see the complete test suite [on GitHub](https://github.com/alexwlchan/alexwlchan.net/tree/main/tests).

Although I wrote these tests to be a safety net while I was making changes, I'm going to keep them around.
I've created [a GitHub Action][action] to run them on a regular schedule, so I can be alerted if anything breaks in future.

[action]: https://github.com/alexwlchan/alexwlchan.net/blob/main/.github/workflows/check_website_is_up.yml

## How I did the migration

There's a common approach to big website migrations: run the new site at an alternative domain name, so you can make changes without breaking the existing site.
You don't change your real domain name to point at the new site until you're sure the new setup is working correctly.

So that's what I did:

1.  I updated the DNS records for `www.alexwlchan.net` to point at my Linux server (normally it redirects to `alexwlchan.net`).

2.  I set up Caddy on my Linux server to serve a copy of my site at `www.alexwlchan.net`.
    I used the [static files quick-start][quick start] in the Caddy docs to write this initial configuration.

3.  I ran my website tests against `www.alexwlchan.net`.
    Lots of the tests failed, because I only had a basic configuration.
    As I ported all my server config to Caddy, the tests started passing.
    
    This step took the longest, but it was still straightforward -- it only took a few hours or so.
    Caddy doesn't have the breadth of example config that's available for more popular web servers like Apache or nginx, but the [Caddy docs] were detailed enough that I could work out everything I wanted to do.
    
    Eventually all the config was ported, and all the tests were passing.

4.  I updated the DNS records for `alexwlchan.net` to point at my Linux server.

5.  I updated Caddy to serve my website at `alexwlchan.net`.

If you're interested, my Caddyfile [is on GitHub](https://github.com/alexwlchan/alexwlchan.net/blob/main/Caddyfile).

There was a minute or so of downtime after I updated the DNS, while I was waiting for Caddy to get HTTPS certificates.
I'm sure I could have avoided that downtime if I really cared, but it would have been more work and this website doesn't need 100% uptime.

[Caddy docs]: https://caddyserver.com/docs
[quick start]: https://caddyserver.com/docs/quick-starts/static-files

## Reflections

Everything seems to have migrated correctly.
Yay!

It's nice to be back running a proper web server, and not trying to shoehorn everything into Netlify's more limited config model.
When it's more settled, I'll wrote some [today I learned](/til/) posts about my Caddy config, so there are more examples of Caddyfiles in search results.

Running my own web server is definitely smoother than the last time I tried it.
The near-universal deployment of HTTPS is broadly a good thing, but it introduced some friction for a while.

Netlify is still what I'd recommend if you're getting started, but I'm glad the DIY approach is improving.
Making it easier for individuals to run their a website on their own server can only be a good thing for the open web.
