---
layout: note
date: 2026-03-28 10:23:58 +00:00
title: Why can't Python connect to example.com?
summary: The Python SSL libraries only know about the certificates sent by the server and in my local store. They can't retrieve missing certificates.
topic: Python
---
I've been experimenting with Python HTTP libraries, and I ran into an unexpected error connecting to `example.com`:

```pycon {"names":{"1":"certifi","2":"ssl","3":"urllib","4":"request","5":"ssl_context"}}
>>> import certifi, ssl, urllib.request
>>> ssl_context = ssl.create_default_context(cafile=certifi.where())
>>> urllib.request.urlopen("https://example.com", context=ssl_context)
Traceback (most recent call last):
  […]
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1081)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  […]
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1081)>```
```

I get similar errors if I use `httpx` or `requests`.

If you look up this error, the usual advice is to make sure you're using certifi, you have the latest version installed, run `Install Certificates.command`, and so on.
Everything looks fine on my system, and I can connect to other websites just fine:

```pycon
>>> certifi.__version__
'2026.02.25'
>>> certifi.where()
'/tmp/tmp.ZzvjQtkeZT/.venv/lib/python3.14/site-packages/certifi/cacert.pem'
>>> urllib.request.urlopen("https://alexwlchan.net", context=ssl_context)
<http.client.HTTPResponse object at 0x1056722f0>
```

I can also open `example.com` in my web browser, but not in Python -- what's up?

## A mistrusted certificate and Authority Information Access

I found [a certifi issue][certifi-393] filed by Clément Beaujoin which describes this exact issue:

> As of February 14, 2026, many automated tests and features relying on example.com began failing with ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1016).
>
> This is caused by example.com (Cloudflare) transitioning to a new certificate chain that roots into AAA Certificate Services, which was officially distrusted by major certificate stores (including certifi) in early February 2026. Because Python's requests/urllib3 does not support AIA (Authority Information Access) to fetch missing intermediates, the verification fails in environments with updated root stores, even though browsers (which support AIA) show the site as secure.

Alex Gaynor, one of the maintainers, explained this isn't something certifi is going to change:

> If example.com is not shipping the necessary intermediates, that's a bug in their TLS serving configuration impacting all non-browser clients, not something we're going to work around.

This explanation sounds right to me, but I wanted to understand more.
Is there a way to print the certificate chain sent by the server, so I can see the missing intermediate and the AIA that tells my client where to fetch the missing intermediates?
How could I have worked this out myself?

I tried running various `openssl` commands and Python scripts that were supposedly printing the certificate chain, but I don't understand TLS well enough to really know what's going on.

I was able to see that certifi no longer trusts AAA Certificate Services, and when.
I tried older versions of certifi, and `example.com` loads with 2025.1.31 but not with 2025.4.26.
Then I looked at the [diff for 2025.4.26][certifi-347], and I can see a certificate with the same name being removed:

```diff {"line_numbers":"128-131"}
-# Issuer: CN=AAA Certificate Services O=Comodo CA Limited
-# Subject: CN=AAA Certificate Services O=Comodo CA Limited
-# Label: "Comodo AAA Services root"
-# Serial: 1
```

I also found a [CPython issue][cpython-62817] where Authority Information Access is mentioned where the topic is discussed, and Alex explained that it's unlikely to be added to Python:

> No, and at this point [the issue] should probably be wontfix'd (IMO), as AIA chasing is relatively out of favor compared to intermediate preloading.

I still don't really understand HTTPS or TLS certificates and I'm not sure how to fix this if I encounter another misconfigured website -- but I only use `example.com` for testing, so for now I can just pick another website to test instead.

[certifi-393]: https://github.com/certifi/python-certifi/issues/393
[certifi-347]: https://github.com/certifi/python-certifi/pull/347/changes
[cpython-62817]: https://github.com/python/cpython/issues/62817
