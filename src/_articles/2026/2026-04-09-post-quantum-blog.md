---
layout: article
date: 2026-04-09 09:28:09 +01:00
title: Quietly quantum-resistant blogging
summary: Recent developments have the cryptography world on alert, fearing a quantum computer capable of breaking public key cryptography is imminent. Unbeknownst to me, my blog is already protected.
topic: Blogging about blogging
---
Among the other fun news recently, [two papers were published][aaronson] that suggest quantum computers capable of breaking classical public-key cryptography algorithms are much closer than previously believed.
What was thought to be years away might now be months.

I found [Filippo Valsorda's post][filippo] especially helpful in understanding the scale of the risk.
We should assume that practical quantum computers are arriving imminently, and roll out quantum-resistant cryptography everywhere, lest we be caught unprepared and leave ourselves at risk.

Google have [set a 2029 deadline][google] for moving to quantum-resistant cryptography; Cloudflare [have done similar][cloudflare].
(Similar internal discussions are happening at [my workplace][tailscale] but there aren't any public announcements yet.)

Amidst all the concern, I was pleasantly surprised to discover that my website is already using quantum-resistant cryptography, and I didn't even realise.

## What's the threat?

All "classical" public-key cryptography relies on hard mathematical problems -- operations that are easy to compute in one direction, but incredibly difficult to do in reverse.

For example, it's easy to multiply two prime numbers together and compute the result, but working out those two prime numbers if you only have the result is impossibly hard.
Even for fairly small numbers, you could be working until the heat death of the universe and still not have an answer.

Quantum computers work differently to traditional computers, and a sufficiently powerful one can reverse these one-way computations.
That would break all of our existing cryptography.

This is the cryptography that underpins almost everything we do online -- protecting banks, governments, militaries, and pretty much everyone else.
If somebody had a quantum computer that could crack it, all of that information would become readable to them.
It would be disastrous.

Small-scale quantum computers already exist in labs, but nothing powerful enough to break public key cryptography -- for now.
Researchers have been trying to build bigger and better quantum computers, but they were a long way away from building anything this powerful.
They'd likely get there eventually, but that was expected to be a long time away -- late 2030s at the earliest.

Other researchers have been developing new cryptographic algorithms that rely on different maths problems, which can't be easily broken by quantum computers.
These new algorithms are the so-called "post-quantum cryptography (PQC)" or "quantum-resistant cryptography".
They've gradually been formalised as standards, and are starting to be used by our devices.
For example, all the popular web browsers now support PQC for HTTPS certificates.

Previously, organisations like the NCSC or NIST recommended [a 2035 deadline][ncsc] for migrating to PQC.
The idea was to be fully migrated long before quantum computers became a practical threat.
That recommendation wasn't just an abundance of caution -- it's to eliminate the risk of [Harvest Now, Decrypt Later (HNDL)][wiki-hndl] attacks, where an adversary records data encrypted with classical cryptography, and waits until they have a quantum computer that can unlock it.
The sooner we migrate to PQC, the more expensive and less valuable such an attack becomes.

Now, it appears we need more urgency.

The two recently published papers narrow the gap between the experimental machines we have today and a practical threat.
They describe efficiency improvements that would allow quantum computers to reverse these mathematical operations with far less computing power.
It's become more plausible that somebody could build a "sufficiently powerful" machine within a few years.
It's also becoming a smarter bet to throw lots of money at building one right now, where previously the odds of success were so low as to make that an unwise bet.

This is why Google, Cloudflare, and others are moving forward their deadlines for migrating to post-quantum cryptography.
The threat has gone from "late 2030s if we're unlucky" to "early 2030s, maybe sooner".

## What about this blog?

While reading the recent news about this issue, I found Cloudflare's [post-quantum encryption radar][cloudflare-radar], which tells you how many websites are protected using post-quantum cryptography.
My website isn't hosted on Cloudflare but I decided to try it anyway, and I was surprised by the result.
I'm already protected!

{%
  picture
  filename="cf_radar_pqc.png"
  width="512"
  class="screenshot"
  alt="A form to check if a host supports post-quantum TLS key exchange. I’ve entered my site ‘alexwlchan.net’ and Cloudflare reports that ‘alexwlchan.net:443 is using X25519MLKEM768, which is post-quantum secure’."
%}

I never set up post-quantum cryptography for this site, but it's enabled anyway, because I'm using [Caddy][caddy] as my web server, and Caddy's [default TLS settings][caddy-tls] include PQC support.
At some point I updated to a new version of Caddy, I got these new defaults, and my site started quietly serving traffic with quantum-resistant cryptography.

This is exactly what I wanted when I switched to Caddy.
I'm not an expert on cryptography, or TLS, or securing servers, so I wanted a web server that would make sensible decisions for me.
I've mostly been ignorant of post-quantum cryptography and developments in quantum computing, but Caddy was protecting me anyway.

There's a lot more work to do to use quantum-resistant cryptography everywhere, and recent announcements have made it far more urgent -- but we can all sleep easier knowing my little blog is safe from quantum computers.

[aaronson]: https://scottaaronson.blog/?p=9665
[caddy]: https://caddyserver.com
[caddy-tls]: https://caddyserver.com/docs/caddyfile/directives/tls
[filippo]: https://words.filippo.io/crqc-timeline/
[google]: https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/
[cloudflare]: https://blog.cloudflare.com/post-quantum-roadmap/
[cloudflare-radar]: https://radar.cloudflare.com/post-quantum
[tailscale]: https://tailscale.com/
[ncsc]: https://www.ncsc.gov.uk/guidance/pqc-migration-timelines
[wiki-hndl]: https://en.wikipedia.org/wiki/Harvest_now,_decrypt_later
