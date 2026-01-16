---
layout: til
title: How to get the expiry date of an HTTPS certificate with Ruby
date: 2024-11-25 10:26:42 +00:00
tags:
  - ruby
summary: Connect to the domain using `net/http`, then you can inspect the `peer_cert`/`not_after` property on the response.
---
I was tinkering with some HTTPS certificates, and I wanted to write a scheduled test that would check the certifcates weren't about to expire.
This is the sort of thing that should be handled by a good certificate provider -- for example, Let's Encrypt sends me emails when my certificates are close to expiry -- but another check is a good belt-and-braces measure.

I did this [with Python](/til/2024/expiry-date-of-https-certificate/) back in August, and I wanted to write similar checks in a codebase which is primarily Ruby.
Fortunately Ruby's `net/http` library exposes information about the HTTPS certificate, so it's a bit simpler than in Python:

```python
require 'net/http'

# Get the expiry date of the HTTPS certificate for this domain name
def get_cert_expiry(hostname)
  uri = URI::HTTPS.build(host: hostname)
  response = Net::HTTP.start(uri.host, uri.port, use_ssl: true)

  cert = response.peer_cert
  cert.not_after
end

puts get_cert_expiry("alexwlchan.net")
# 2025-02-17 08:34:57 UTC
```

The `not_after` property is a [`Time`](https://ruby-doc.org/core-2.6.8/Time.html) which can be used directly in datetime comparisons and calculations.
