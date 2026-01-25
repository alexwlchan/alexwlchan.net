---
layout: til
title: Disable HTTP Basic Auth for certain pages in Caddy
summary: Define a matcher that negates the routes you want to be public, then use that with your `basic_auth` directive.
date: 2025-07-18 10:20:52 +01:00
tags:
  - caddy
---
Suppose I have a web server using Caddy, and I'm protecting it with HTTP Basic Authentication using the [`basic_auth` directive](https://caddyserver.com/docs/caddyfile/directives/basic_auth).

## When all routes are private

Here's a simple Caddyfile where every route requires auth:

<!-- caddy -->

```
:2016 {
	basic_auth {
		# $ caddy hash-password --plaintext correct-horse-battery-staple
		xkcd $2a$14$jOkhzoZwxmKxUSUAS0WRBOClNxeDgFUSq4GZ0cnHVpNqxazmnNt4G
	}

	respond "This page is secret!"
}
```

If we try to load any page, it returns an HTTP 401 unless we pass the username and password:

```console
$ curl \
    --write-out '%{response_code}\n' \
    'http://localhost:2016'
401

$ curl \
    --write-out '%{response_code}\n' \
    --user 'xkcd:correct-horse-battery-staple' \
    'http://localhost:2016'
This page is secret!
200
```

## When some routes aren't private

I want routes that skip the authentication (e.g. a publicly-accessible healthcheck endpoint).

The way to do this is to define a [matcher](https://caddyserver.com/docs/caddyfile/matchers) that matches all the pages *except* the ones I want to make public, and then use that matcher with my `basic_auth` directive.

<!-- caddy -->

```
:2016 {
	@private {
		not path /public/*
	}

	basic_auth @private {
		# $ caddy hash-password --plaintext correct-horse-battery-staple
		xkcd $2a$14$jOkhzoZwxmKxUSUAS0WRBOClNxeDgFUSq4GZ0cnHVpNqxazmnNt4G
	}

	handle /public/* {
		respond "This page is public!"
	}

	respond "This page is secret!"
}
```

Now most pages are still private, but we can request public pages without using authentication:

```console
$ curl \
    --write-out '%{response_code}\n' \
    'http://localhost:2016'
401

$ curl \
    --write-out '%{response_code}\n' \
    'http://localhost:2016/public/'
This page is public!
200
```
