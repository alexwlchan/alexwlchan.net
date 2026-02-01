---
layout: til
date: 2023-12-07 20:53:08 +00:00
title: Telling mechanize how to find local issuer certificates
summary: Calling `browser.set_ca_data(cafile=certifi.where())` will tell where mechanize can find some local SSL certificates.
colors:
  index_light: "#554741"
  index_dark:  "#c3c6ca"
tags:
  - python
  - "python:mechanize"
  - "python:certifi"
card_attribution: Cover image from https://www.pexels.com/photo/gray-and-gold-steel-gears-159275/
---

I was doing some work on [my library lookup tool] recently, and I ran into an issue with [mechanize], the Python library I use to simulate a web browser.
I'd upgraded my version of Python and mechanize, and now I wasn't able to connect to HTTPS sites.

If I tried a simple example:

```python
import mechanize

browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.open("https://www.example.net/").read()
```

it would fail with an error:

```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate
verify failed: unable to get local issuer certificate (_ssl.c:1000)
```

My first instinct was to check Google and GitHub; I couldn't find any other instances of people finding and fixing this issue.
The most I could find was [a quickstart example] that starts with an HTTP example, then suggests disabling SSL verification to access HTTPS sites.
I found a few instances of people following this suggestion on GitHub – but I wasn't keen on that.
SSL verification exists for a reason; I don't want to get rid of it!

A bit later I found a page [about changing the certificates] used by your mechanize browser with `browser.set_ca_data()`.
I knew from my work on HTTP libraries that [certifi] is a bundle of SSL certificates often used in Python libraries, so I decided to try pointing mechanize at certifi:

```diff
 import mechanize
 import certifi

 browser = mechanize.Browser()
 browser.set_handle_robots(False)
+browser.set_ca_data(cafile=certifi.where())
 browser.open("https://www.example.net/").read()
```

That seemed to work, and my mechanize browser was once again able to browse the HTTPS web.

If you use popular HTTP libraries like [httpx] or [requests], they install and load SSL certificates from certifi automatically.
I don't know why mechanize doesn't do the same, but it was just a one-line change to get it working correctly.

[my library lookup tool]: /2022/library-lookup/
[mechanize]: https://pypi.org/project/mechanize/
[about changing the certificates]: https://mechanize.readthedocs.io/en/latest/advanced.html#using-custom-ca-certificates
[a quickstart example]: https://mechanize.readthedocs.io/en/latest/index.html
[certifi]: https://github.com/certifi/python-certifi
[httpx]: https://www.python-httpx.org/advanced/#ssl-certificates
[requests]: https://requests.readthedocs.io/en/latest/user/advanced/?highlight=certifi#ca-certificates

<!--

Traceback (most recent call last):
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/.venv/lib/python3.12/site-packages/mechanize/_urllib2_fork.py", line 1242, in do_open
    h.request(str(req.get_method()), str(req.get_selector()), req.data,
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/http/client.py", line 1319, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/http/client.py", line 1365, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/http/client.py", line 1314, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/http/client.py", line 1074, in _send_output
    self.send(msg)
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/http/client.py", line 1018, in send
    self.connect()
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/http/client.py", line 1460, in connect
    self.sock = self._context.wrap_socket(self.sock,
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/ssl.py", line 1046, in _create
    self.do_handshake()
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/ssl.py", line 1317, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/s.py", line 5, in <module>
    browser.open("https://www.example.net/").read()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/.venv/lib/python3.12/site-packages/mechanize/_mechanize.py", line 257, in open
    return self._mech_open(url_or_request, data, timeout=timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/.venv/lib/python3.12/site-packages/mechanize/_mechanize.py", line 287, in _mech_open
    response = UserAgentBase.open(self, request, data)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/.venv/lib/python3.12/site-packages/mechanize/_opener.py", line 193, in open
    response = urlopen(self, req, data)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/.venv/lib/python3.12/site-packages/mechanize/_urllib2_fork.py", line 431, in _open
    result = self._call_chain(self.handle_open, protocol, protocol +
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/.venv/lib/python3.12/site-packages/mechanize/_urllib2_fork.py", line 420, in _call_chain
    result = func(*args)
             ^^^^^^^^^^^
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/.venv/lib/python3.12/site-packages/mechanize/_urllib2_fork.py", line 1296, in https_open
    return self.do_open(conn_factory, req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/folders/3s/tb0f2zjd6gq7f9x0k2_r0ndw0000gn/T/tmp.i2QQ1FRh/.venv/lib/python3.12/site-packages/mechanize/_urllib2_fork.py", line 1246, in do_open
    raise URLError(err)
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)>

-->
