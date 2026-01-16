---
layout: til
title: How to get the IP address of a device in my Tailnet
date: 2024-12-26 22:06:45 +00:00
tags:
  - tailscale
  - jq
summary: |
  Use `tailscale status --json` and filter the output using `jq`.
---
I'm using Tailscale to connect my personal devices, and I wanted a way to get the IP address of my home desktop from the command line.

I have the Tailscale CLI installed but it wasn't immediately obvious which subcommand I should be using -- a quick Google suggested I should be using `tailscale status --json`.
The help text says the output format is subject to change, so for reference here's the relevant output I'm working from:

```
{
  "Version": "1.78.1-t8903926f7-gc4163954e",
  "Peer": {
    "nodekey:b0aed7b8…": {
      "HostName": "Phaenna",
      "DNSName": "phaenna.tailfa84dd.ts.net.",
      "OS": "macOS",
      "TailscaleIPs": [
        "100.98.5.48",
        "fd7a:115c:a1e0::2701:530"
      ],
      …
    }
  },
  …
}
```

Then I can use `jq` to filter the output and get the IP address I need:

```shell
tailscale status --json \
  | jq --join-output --raw-output '.Peer[] | select(.HostName  == "Phaenna") | .TailscaleIPs[0]'
```

I've wrapped this command in [a shell script `get_phaenna_ip`](https://github.com/alexwlchan/scripts/blob/main/web/get_phaenna_ip).
