---
layout: post
title: IP and DNS addresses for documentation
date: 2018-01-18 23:26:28 +0000
summary: If you're writing technical documentation and need placeholder IP addresses or DNS hostnames, there are some special values just for you!
---

If you're writing documentation that includes IP addresses, you may want to check out [RFC 5737][rfc5737] and [RFC 3849][rfc3849], which specify IPv4 and IPv6 addresses for use in documentation.

These addresses are "reserved", meaning they should never be used for anything else -- not on the public Internet, nor within internal networks.
That means you can use them in examples, and they should never conflict or be confused with real systems.

Here's RFC 5737 for IPv4:

> The blocks 192.0.2.0/24 (TEST-NET-1), 198.51.100.0/24 (TEST-NET-2),
> and 203.0.113.0/24 (TEST-NET-3) are provided for use in
> documentation.

and RFC 3849 for IPv6:

> The prefix allocated for documentation purposes is 2001:DB8::/32.

In a similar vein, [RFC 2606][rfc2606] provides a number of TLDs and domain names for use in documentation -- for example, `.test` and `example.net`.
Again, the idea is that these are reserved for documentation, and will never start resolving to a real system at an unknown point in the future.

Of course, you can use any IP address or DNS name in your docs, but if the exact values are unimportant, you may want to consider using these reserved blocks.
They're good placeholder values, because they can't be mixed up with anything else.

These RFCs have come up several times in the Write The Docs Slack, which is why I decided to create a more permanent signpost.
If you care about technical writing, you may want to join the Slack, where this sort of thing is often discussed -- sign up through [the WTD website][slack].

[rfc5737]: https://tools.ietf.org/html/rfc5737
[rfc3849]: https://tools.ietf.org/html/rfc3849
[rfc2606]: https://tools.ietf.org/html/rfc2606
[slack]: http://www.writethedocs.org/slack/
