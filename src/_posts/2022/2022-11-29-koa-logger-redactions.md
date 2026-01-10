---
layout: post
date: 2022-11-29 23:39:11 +0000
title: Redacting sensitive query parameters with koa and koa-logger
summary: Using a custom transporter to modify the log message and remove secret information.
tags:
  - javascript
  - javascript:koa
colors:
  index_light: "#054f17"
  index_dark:  "#08af2f"
---

<!-- Card image based on https://www.pexels.com/photo/photo-of-green-fern-leaves-1687341/ and Wikipedia article -->

At work, we use the [Koa framework][koa] and [koa-logger middleware][koa-logger] as part of our website.
Together, they give us nice request-response logs for all our traffic:

```
<-- GET /
--> GET / 200 754ms 57.28kb

<-- GET /stories
--> GET /stories 200 374ms 71.29kb

<-- GET /works?query=trees
--> GET /works?query=trees 200 524ms 72.08kb
```

The default behaviour for koa-logger is to log the complete URL, including all query parameters.
As we've added identity-related services like sign-up for library membership, that became untenable.

For example, we use Auth0 to manage user accounts, and after you sign up in Auth0, it redirects you to our application with a session token in the query parameters:

```
<-- GET /account/registration?session_token=eyJhbGc…
```

That session token is [a JWT][jwt] which can be decoded to reveal your email and your current IP address -- neither of which we want or need in our application logs.
We wanted to redact these tokens, and any other sensitive query parameters.
(This information is still in the Auth0 logs, if we really need it for debugging, but access to Auth0 is more tightly controlled than our general application logs.)

The koa-logger documentation has a vague mention of "custom transporters", but doesn't really explain them in much detail.
I had to read the source code and look at some examples to understand it, and eventually I got it working.

This is an example Koa server that uses koa-logger, and which calls a function `redactUrl()` to redact portions of a URL before logging it:

{% code lang="javascript" names="0:Koa 2:logger 4:app 11:args 12:format 13:method 14:url 15:status 16:time 17:length 19:redactedUrl 22:newArgs" %}
const Koa = require('koa');            // ^2.13.4
const logger = require('koa-logger');  // ^3.2.1

const app = new Koa();

app.use(
  logger({
    transporter: (_, args) => {
      // `args` contains the pieces of the log.
      //
      // `format` is a template string, e.g. `<!-- %s %s`, and the other
      // variables are log values that are substituted into the template.
      const [format, method, url, status, time, length] = args;

      // redactUrl is a function that takes a string (the requested URL)
      // and returns another string (the redacted URL)
      const redactedUrl = redactUrl(url);

      // Some of these values may be null/undefined, e.g. koa-logger will
      // create a log for an incoming request, when we don't yet have
      // a status/time/length
      const newArgs = [format, method, redactedUrl, status, time, length].filter(Boolean);

      console.log(...newArgs);
    },
  })
);

app.use(async ctx => {
  ctx.body = 'Hello World';
});

app.listen(3000);
{% endcode %}

and here's our implementation of `redactUrl()`, which redacts every query parameter:

{% code lang="javascript" names="0:url 2:redactUrl 3:u 4:parsedUrl 11:params 15:key" %}
const url = require('url');

/** Redact every query parameter from a URL */
function redactUrl(u) {

  // Note: we use a deprecated API here because we're working with
  // relative URLs, e.g. `/account`.
  //
  // The WHATWG URL API that the deprecation message suggests doesn't
  // work for this use case; it wants absolute URLs.
  const parsedUrl = url.parse(u);

  // If there are no query parameters to redact, we don't need to do anything.
  if (parsedUrl.query === null) {
    return u;
  }

  const params = new URLSearchParams(parsedUrl.query);

  for (const key of params.keys()) {
    params.set(key, '[redacted]');
  }

  parsedUrl.query = params.toString();
  parsedUrl.search = `?${params.toString()}`;

  // When the square brackets get URL-encoded, they're replaced with
  // percent characters, e.g. `/account?token=%5Bredacted%5D`.
  //
  // Because they aren't actually URL characters, we put back the
  // original brackets for ease of readability.
  return url.format(parsedUrl).replace(/%5Bredacted%5D/g, '[redacted]');
}
{% endcode %}

You could modify this if you only wanted to redact specific query parameters, or you wanted to redact some other part of the URL.

Here's an example of the new logs:

```
<-- GET /account/registration?session_token=[redacted]&redirect_uri=[redacted]&state=[redacted]
--> GET /account/registration?session_token=[redacted]&redirect_uri=[redacted]&state=[redacted] 200 353ms 104.91kb
```

No sensitive data here!

We put this in place several months ago, and I meant to write about it after it had settled in, but it's been working fine and  I completely forgot.
Yesterday's announcement of [sensitive data redaction in CloudWatch][cloudwatch] reminded me that I had this post in my drafts folder, and I finished it off.

[koa]: https://www.npmjs.com/package/koa
[koa-logger]: https://www.npmjs.com/package/koa-logger
[jwt]: https://en.wikipedia.org/wiki/JSON_Web_Token
[cloudwatch]: https://aws.amazon.com/blogs/aws/protect-sensitive-data-with-amazon-cloudwatch-logs/
