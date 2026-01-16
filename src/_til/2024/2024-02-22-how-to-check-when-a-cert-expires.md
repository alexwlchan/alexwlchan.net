---
layout: til
date: 2024-02-22 12:33:03 +00:00
title: How to check when an HTTPS certificate expires
tags:
  - http
  - curl
---
You can check whether a certificate is about to expire using the following `openssl` command:

```shell
openssl s_client -connect example.com:443 </dev/null 2>/dev/null \
  | openssl x509 -checkend "$SECONDS"
```

This will exit with status 0 if the certificate won't expire before `$SECONDS` have passed, and status 1 if it will.

## Alternatives considered

*   My first thought was to try using curl and parse the output (like this post in [Nick Janetakis’s blog](https://nickjanetakis.com/blog/using-curl-to-check-an-ssl-certificate-expiration-date-and-details)) but that felt a bit fragile.
    Additionally, curl doesn't print the certificate details if you get an immediate redirect.

    This led me to a [Server Fault question](https://serverfault.com/q/700812/206273), where I was pointed to the `openssl x509` command.
