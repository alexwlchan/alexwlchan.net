---
layout: til
title: How to get the expiry date of an HTTPS certificate with Python
date: 2024-08-31 18:27:49 +01:00
tags:
  - python
summary: Connect to the domain using the `socket` module, then use the `getpeercert()` method on the connection to get information about the HTTPS certificate.
---

I was tinkering with some HTTPS certificates, and I wanted to write a scheduled test that would check the certificates weren't about to expire.
This is the sort of thing that should be handled by a good certificate provider -- for example, Let's Encrypt sends me emails when my certificates are close to expiry -- but another check is a good belt-and-braces measure.

With a bit of help from Stack Overflow, I wrote a Python function that works out when the HTTPS certificate for a domain expires:

```python
import contextlib
from datetime import datetime
import socket
import ssl


def get_https_expiry_date(hostname: str) -> datetime:
    """
    Get the expiry date of the HTTPS certificate for a domain.
    """
    ctx = ssl.create_default_context()

    with contextlib.closing(socket.socket(socket.AF_INET)) as sock:
        conn = ctx.wrap_socket(sock, server_hostname=hostname)

        conn.settimeout(5.0)
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()

        # Example date: "Oct 17 12:32:16 2024 GMT"
        expiry_date_str = ssl_info["notAfter"]
        expiry_date = datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y %Z")

    return expiry_date


if __name__ == "__main__":
    print(get_https_expiry_date("alexwlchan.net"))
```

I call that from a test, and assert the delta between now and the expiry date is at least two weeks.
I can adjust that threshold as I think is useful.

As an example, here's what `ssl_info` looks like for my domain:

```
{'OCSP': ('http://e5.o.lencr.org',),
 'caIssuers': ('http://e5.i.lencr.org/',),
 'issuer': ((('countryName', 'US'),),
            (('organizationName', "Let's Encrypt"),),
            (('commonName', 'E5'),)),
 'notAfter': 'Oct 17 12:32:16 2024 GMT',
 'notBefore': 'Jul 19 12:32:17 2024 GMT',
 'serialNumber': '04D4D59A60990543FD74EA616776AB2274DE',
 'subject': ((('commonName', 'alexwlchan.co.uk'),),),
 'subjectAltName': (('DNS', 'alexwlchan.co.uk'),
                    ('DNS', 'alexwlchan.com'),
                    ('DNS', 'alexwlchan.net'),
                    ('DNS', 'www.alexwlchan.net')),
 'version': 3}
```
