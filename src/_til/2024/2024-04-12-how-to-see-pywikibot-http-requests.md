---
layout: til
date: 2024-04-12 14:48:47 +01:00
title: How to see the HTTP requests being made by pywikibot
summary: |
  To see exactly what HTTP requests were being made, I modified the library so that betamax would record requests.
tags:
  - python
  - python:requests
  - python:pywikibot
---
I was trying to debug an issue in some code for interacting with Wikimedia Commons (see [village pump discussion][vpump]).
I had my broken code using httpx, and another Wikimedian had given me working code with pywikibot.
I wanted to see the exact HTTP requests that pywikibot was making, so that I could compare them to my code.

I fiddled around with lots of `print()` statements for a while, before I had a much better idea.

If you dig through the code, you end up [in the file `http.py`][http.py], which is where the HTTP request is actually made.
It's using the [requests] library with a Session object.
And in the documentation [for `comms.http`][comms.http], it explains that you can swap out the Session object if necessary.

If you combine this with the [betamax library][betamax], you can get an instance of pywikibot that will record all its HTTP requests:

```python
import betamax
import requests
import pywikibot
from pywikibot.comms import http


class RecordingSession(requests.Session):
    def request(self, *args, **kwargs):
        recorder = betamax.Betamax(self, cassette_library_dir="cassettes")

        with recorder.use_cassette("recorded_request", record="all"):
            return super().request(*args, **kwargs)


http.session = RecordingSession()

site = pywikibot.Site("commons", "commons")
site.login()
```

(In case it's important later, I'm using betamax&nbsp;0.9.0 and pywikibot&nbsp;9.0.0.)

[vpump]: https://commons.wikimedia.org/wiki/Commons:Village_pump/Technical#How_do_I_flag_my_bot%E2%80%99s_edits_as_coming_from_a_bot?
[http.py]: https://gerrit.wikimedia.org/r/plugins/gitiles/pywikibot/core/+/refs/tags/9.0.0/pywikibot/comms/http.py
[requests]: https://requests.readthedocs.io/en/latest/
[comms.http]: https://doc.wikimedia.org/pywikibot/stable/api_ref/pywikibot.comms.html#module-comms.http
[betamax]: https://pypi.org/project/betamax/
