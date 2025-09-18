---
layout: til
title: Seeing the public node key of a Tailscale node
date: 2025-09-18 13:27:49 +0100
tags:
  - tailscale
---
I've been doing some work on [Tailscale key expiry](https://tailscale.com/kb/1028/key-expiry#renewing-keys-for-an-expired-device), in particular renewing keys with `tailscale up --force-reauth`.
As part of this work, I want to see when a node key has (or hasn't) changed.

I've found some CLI commands that let me see the current node key.
Note that these use unstable interface, so these commands might break on newer versions -- I'm using v1.88.1.

## Seeing your own node key

This is the public key of the current node:

```console
$ tailscale status --self --json | jq -r .Self.PublicKey
nodekey:46f9c8656ef1224b5ce5220fbdf96ce38e52aaabeccc9b7358b06481e9481821
```

Here's what [the key prefixes](https://github.com/tailscale/tailscale/blob/cd153aa644dd861602e386e71df20a61733b56a8/types/key/node.go#L21-L39) mean:

*   The `nodekey:` prefix is for hex-encoded public keys (so safe to publish in a blog post)
*   The `np:` prefix is for binary-encoded public keys
*   The `privkey:` prefix is for hex-encoded *private* keys

## Seeing a peer's node key

This is the public key of the `linode-vps` node:

```console
$ tailscale debug netmap | jq -r '.Peers | map(select(.ComputedName == "linode-vps")) | .[].Key'
nodekey:731cd9e2560f29c655b674e4033d7cdffeb210aea917b225099b2d601533502d
```

I'm sure this is possible with `tailscale status --peers --json`, but that doesn't include MagicDNS names so it's a bit less convenient for me -- plus, I already had this command working.
