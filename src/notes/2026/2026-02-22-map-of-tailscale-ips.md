---
layout: note
title: Get a map of IP addresses for devices in my tailnet
date: 2026-02-22 08:10:53 +00:00
topics:
  - Tailscale
  - jq
---
Here's a jq snippet that prints the hostname and IP addresses of every device in my tailnet (or at least, every device my current machine can see):

```console
$ tailscale status --json \
    | jq '[.Self] + [.Peer[]] | map({(.DNSName): (.TailscaleIPs)}) | add'
{
  "phaenna-mac-mini.tailfa84dd.ts.net.": [
    "100.76.19.1",
    "fd7a:115c:a1e0::fb01:1301"
  ],
  …
}
```

How it works:

-   `[.Self] + [.Peer[]]` combines the `.Self` object and `.Peer` array into a single array.
-   `map({(.DNSName): (.TailscaleIPs)})` converts each entry in that array into a map where the DNSName is the key, and the TailscaleIPs array is the value.
    Now the output is an array of objects, each with a single key-value pair.
-   `add` combines all those objects into a single object.

Here's a variant that keys the map by MagicDNS name:

```console
$ tailscale status --json \
    | jq '[.Self] + [.Peer[]] | map({(.DNSName | split(".")[0]): (.TailscaleIPs)}) | add'
{
  "phaenna-mac-mini": [
    "100.76.19.1",
    "fd7a:115c:a1e0::fb01:1301"
  ],
  …
}
```

And another variant that just extracts the IPv4 address:

```console
$ tailscale status --json \
    | jq '[.Self] + [.Peer[]] | map({(.DNSName | split(".")[0]): (.TailscaleIPs[0])}) | add'
{
  "phaenna-mac-mini": "100.76.19.1",
  "go": "100.107.83.99",
  "alexs-macbook-pro": "100.109.169.87",
  …
}
```

I'm planning to paste this directly into the [`hosts` section][ts-hosts] of my policy file.

Tested with Tailscale 1.95.104.
Disclaimer: At time of writing, I'm employed by Tailscale.

[ts-hosts]: https://tailscale.com/docs/reference/syntax/policy-file#hosts
