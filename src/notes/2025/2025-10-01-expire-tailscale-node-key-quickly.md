---
layout: note
title: How to expire a Tailscale node key faster than the min expiry
date: 2025-09-22 09:28:04 +01:00
date_updated: 2026-02-10 17:47:12 +00:00
summary: Use `tailscale debug set-expire --in=<duration>`.
topic: Tailscale
old_syntax_highlighting: true
---
In normal use, you can't set a node key to expire in less than 1 day, which is annoying if you want to test something quickly.
(I wanted to test how the client behaves with expired node keys.)

There's a convenient [`debug` command][cli-debug] that lets you set the key expiry to any duration, in particular short ones:

```console
$ tailscale debug set-expire --in=10m
```

You can also set a negative number, to expire a key immediately:

```console
$ tailscale debug set-expire --in=-1m
```

[cli-debug]: https://github.com/tailscale/tailscale/blob/dc1d811d4838cb73216244ecaf7be923f005548e/cmd/tailscale/cli/debug.go#L309-L319
