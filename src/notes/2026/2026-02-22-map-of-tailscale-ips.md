---
layout: note
title: Get a map of IP addresses for devices in my tailnet
date: 2026-02-22 08:10:53 +00:00
date_updated: 2026-05-10 04:26:06 +01:00
topics:
  - Tailscale
  - jq
summary: |
  Use `tailscale status --json` and filter the output using `jq`.
---
Here's a jq snippet that prints the hostname and IP addresses of every device in my tailnet (or at least, every device my current machine can see):

<pre class="lng-console"><code><span class="gp">$</span><span class="w"> </span>tailscale status --json <span class="p">\</span>
<span class="w">    </span><span class="p">|</span><span class="w"> </span>jq<span class="w"> </span><span class="s">'[.Self] + [.Peer[]]</span>
<span class="s">          | sort_by(.DNSName)</span>
<span class="s">          | map({(.DNSName): (.TailscaleIPs)}) </span>
<span class="s">          | add'</span>
<span class="go">{</span>
<span class="go">  "phaenna-mac-mini.tailfa84dd.ts.net.": [</span>
<span class="go">    "100.76.19.1",</span>
<span class="go">    "fd7a:115c:a1e0::fb01:1301"</span>
<span class="go">  ],</span>
<span class="go">  …</span>
<span class="go">}</span></code></pre>

How it works:

-   `[.Self] + [.Peer[]]` combines the `.Self` object and `.Peer` array into a single array.
-   `sort_by(.DNSName)` sorts the array based on the `DNSName` field.
-   `map({(.DNSName): (.TailscaleIPs)})` converts each entry in that array into a map where the `DNSName` is the key, and the `TailscaleIPs` array is the value.
    Now the output is an array of objects, each with a single key-value pair.
-   `add` combines all those objects into a single object.

Here's a variant that keys the map by MagicDNS name:

<pre class="lng-console"><code><span class="gp">$</span><span class="w"> </span>tailscale status --json <span class="p">\</span>
<span class="w">    </span><span class="p">|</span><span class="w"> </span>jq<span class="w"> </span><span class="s">'[.Self] + [.Peer[]]</span>
<span class="s">          | sort_by(.DNSName)</span>
<span class="s">          | map({(.DNSName | split(".")[0]): (.TailscaleIPs)}) </span>
<span class="s">          | add'</span>
<span class="go">{</span>
<span class="go">  "phaenna-mac-mini": [</span>
<span class="go">    "100.76.19.1",</span>
<span class="go">    "fd7a:115c:a1e0::fb01:1301"</span>
<span class="go">  ],</span>
<span class="go">  …</span>
<span class="go">}</span></code></pre>

Another variant that just extracts the IPv4 address:

<pre class="lng-console"><code><span class="gp">$</span><span class="w"> </span>tailscale status --json <span class="p">\</span>
<span class="w">    </span><span class="p">|</span><span class="w"> </span>jq<span class="w"> </span><span class="s">'[.Self] + [.Peer[]]</span>
<span class="s">          | sort_by(.DNSName)</span>
<span class="s">          | map({(.DNSName | split(".")[0]): (.TailscaleIPs[0])}) </span>
<span class="s">          | add'</span>
<span class="go">{</span>
<span class="go">  "linode-vps": "100.98.193.6",</span>
<span class="go">  "palaemon-macbook-air": "100.120.194.127",</span>
<span class="go">  "phaenna-mac-mini": "100.76.19.1",</span>
<span class="go">  …</span>
<span class="go">}</span></code></pre>

I paste this directly into the [`hosts` section][ts-hosts] of my policy file.

If you have Mullvad nodes in your Tailnet, you can filter them out of this map with:

<pre class="lng-console"><code><span class="gp">$</span><span class="w"> </span>tailscale status --json <span class="p">\</span>
<span class="w">    </span><span class="p">|</span><span class="w"> </span>jq<span class="w"> </span><span class="s">'[.Self] + [.Peer[]]</span>
<span class="s">          | map(select(.Tags == null or (.Tags | contains(["tag:mullvad-exit-node"]) | not)))</span>
<span class="s">          | sort_by(.DNSName)</span>
<span class="s">          | map({(.DNSName | split(".")[0]): (.TailscaleIPs[0])}) </span>
<span class="s">          | add'</span>
<span class="go">{</span>
<span class="go">  "linode-vps": "100.98.193.6",</span>
<span class="go">  "palaemon-macbook-air": "100.120.194.127",</span>
<span class="go">  "phaenna-mac-mini": "100.76.19.1",</span>
<span class="go">  …</span>
<span class="go">}</span></code></pre>

Tested with Tailscale 1.95.104.
Disclaimer: At time of writing, I'm employed by Tailscale.

[ts-hosts]: https://tailscale.com/docs/reference/syntax/policy-file#hosts
