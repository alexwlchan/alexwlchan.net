---
layout: til
title: Redacting sensitive information from gunicorn access logs
date: 2025-07-04 12:56:59 +0100
summary: Create a subclass of `gunicorn.glogging.Logger`, and redact information in the `atoms()` method.
tags:
  - python
  - python:gunicorn
---
I'm working on a Python web app that's running with gunicorn, and I'm writing access logs to a file.
By default, these logs include the full URL requested by the user, with any query parameters.

This app uses OAuth to authenticate with a third-party service, so at some point users get redirected back to the app with some OAuth tokens in the URL:

```
127.0.0.1 - - [01/Jan/2001:01:01:01 +0000] "GET /callback?oauth_token=72157720950195922-ddd4617fd8594560&oauth_verifier=51be7d7b0c701ba6 HTTP/1.1" 302 201 "https://www.flickr.com/" "Mozilla/5.0"
```

This feels risky, especially because the access logs are being written in plain text.

I don't think there's a substantial risk in this app, because those OAuth tokens are immediately used to fetch an OAuth access token, and the third-party service should prevent token reuse.
But it got me thinking about how to redact information from gunicorn logs, and I couldn't find any instructions, so I went digging.

## A minimal gunicorn app

Let's start by creating a minimal gunicorn app to test with.
Normally I'm running gunicorn with Flask apps, but gunicorn's logging is completely separate from Flask.

The gunicorn documentation [includes a simple test app](https://docs.gunicorn.org/en/stable/run.html#gunicorn), which I'll save to `test.py`:

```python
def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
```

I can start the app and save the access logs to a file:

```console
$ gunicorn test:app --access-logfile access.log
```

Then I can make a request with curl, and see the request appear in the access log:

```console
$ curl 'http://127.0.0.1:8000'
Hello, World!

$ curl 'http://127.0.0.1:8000/callback?oauth_token=123'
Hello, World!

$ cat access.log
127.0.0.1 - - [04/Jul/2025:17:05:28 +0100] "GET / HTTP/1.1" 200 14 "-" "curl/8.7.1"
127.0.0.1 - - [04/Jul/2025:17:06:03 +0100] "GET /callback?oauth_token=123 HTTP/1.1" 200 14 "-" "curl/8.7.1"
```

Let's hide that `oauth_token` query parameter from the access log.

## Customising the gunicorn logging behaviour

I found a setting `logger_class` [in the documentation](https://docs.gunicorn.org/en/stable/settings.html#logger-class):

> The logger you want to use to log events in Gunicorn.
>
> The default class (`gunicorn.glogging.Logger`) handles most normal usages in logging. It provides error and access logging.
>
> You can provide your own logger by giving Gunicorn a Python path to a class that quacks like `gunicorn.glogging.Logger`.

I read the source code for [the `Logeer` class](https://github.com/benoitc/gunicorn/blob/a86ea1e4e6c271d1cd1823c7e14490123f9238fe/gunicorn/glogging.py#L164-L473), and I think the best approach is to subclass it and override the `atoms()` method.
This returns "atoms for log formatting", which are the different tokens you can [use in the access log](https://docs.gunicorn.org/en/stable/settings.html#access-log-format) -- like `%(h)s` for remote address, or `%(t)s` for the date of the request.
(Although I'm overriding existing atoms, it occurs to me you could also use this to add new fields you want to log.)

Here's a subclass of `Logger` which replaces sensitive query parameters with `[redacted]`, which I've saved to `mylogging.py`:

{% annotatedhighlight lang="python" %}
from datetime import timedelta
import typing
import urllib.parse

from gunicorn.glogging import Logger
from gunicorn.http.message import Request
from gunicorn.http.wsgi import Response


SENSITIVE_QUERY_PARAMS = ['oauth_token']


def redact_uri(uri: str) -> str:
    """Redact the query parameters in a complete URI."""
    u = urllib.parse.urlparse(uri)

    u = u._replace(query=redact_query(u.query))

    return urllib.parse.urlunparse(u)


def redact_query(query: str | None) -> str | None:
    """Redact the query parameters in a URI query string."""
    if query is None:
        return None

    qsl = urllib.parse.parse_qsl(query)

    for idx, (name, _) in enumerate(qsl):
        if name in SENSITIVE_QUERY_PARAMS:
            qsl[idx] = (name, '[redacted]')

    query = urllib.parse.urlencode(qsl)

    # The square brackets will get URL-encoded; undo the encoding
    # so they're more readable in the log.
    query = query.replace('%5Bredacted%5D', '[redacted]')

    return query


class RedactingLogger(Logger):
    def atoms(
        self,
        resp: Response,
        req: Request,
        environ: dict[str, typing.Any],
        request_time: timedelta,
    ) -> dict[str, None]:
        atoms = super().atoms(resp, req, environ, request_time)

        # r = "status line (e.g. GET / HTTP/1.1)"
        atoms["r"] = (
            "%s %s %s"
            % (
                environ["REQUEST_METHOD"],
                redact_uri(environ["RAW_URI"]),
                environ["SERVER_PROTOCOL"],
            )
        )

        # q = query string
        atoms["q"] = redact_query(environ.get("QUERY_STRING"))

        return atoms
{% endannotatedhighlight %}

I can restart my gunicorn app and tell it to use this logger class:

```console
$ gunicorn test:app --access-logfile access.log --logger-class 'mylogging.RedactingLogger'
```

And now the `oauth_token` query parameter gets redacted in my access logs:

```console
$ curl 'http://127.0.0.1:8000'
Hello, World!

$ curl 'http://127.0.0.1:8000/callback?oauth_token=123'
Hello, World!

$ cat access.log
127.0.0.1 - - [04/Jul/2025:17:31:12 +0100] "GET / HTTP/1.1" 200 14 "-" "curl/8.7.1"
127.0.0.1 - - [04/Jul/2025:17:31:13 +0100] "GET /callback?oauth_token=[redacted] HTTP/1.1" 200 14 "-" "curl/8.7.1"
```