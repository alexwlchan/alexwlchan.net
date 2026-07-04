---
layout: article
date: 2026-07-03 16:52:05 +01:00
title: I don't want to repeat repeat myself
summary: I wrote a pair of regular expressions to find repeated words and phrases in my source code.
topic: Regular expressions
---
Yesterday at work, a customer spotted a typo in our UI: "you can **use the use the** Tailscale CLI".
After the typo was fixed, I wanted to find other cases of accidentally repeated words or phrases.
I used two regular expressions to search every codebase for unnecessary repetition.

The first regex finds repeated words:

<pre class="wrap"><code><span class="c">\b([A-Za-z]+) \1\b</span>

Backfill product data <strong>from from</strong> Stripe
Learn more <strong>about about</strong> inviting users
Argument must <strong>be be</strong> one of host name, IP set name, IP prefix, or IP
</code></pre>

There's a capturing group for a single word made up of letters `([A-Za-z]+)`, a space, then a backreference to the group.
I used `[A-Za-z]` rather than the word metacharacter `\w` because I didn't want to include numbers, which would dramatically increase the number of matches in a codebase.
This skips repetitions which include accented characters, but that's fine because those are rare in my writing.

That expression is surrounded by word boundary assertions `\b`, which check that I'm at the start/end of a word -- this avoids finding repeated character sequences within longer words, like "wi<strong>th th</strong>e reason".

The second regex finds repeated phrases:

<pre class="wrap"><code><span cxswlass="c">\b([A-Za-z]+ [A-Za-z]+) \1\b</span>

Follow the steps <strong>in the in the</strong> "How to" section
Log <strong>in to in to</strong> your account
To configure <strong>federated identities federated identities</strong> using the Go SDK</code></pre>

I've changed the capturing group, so now it looks for two words separated by a space.

Sometimes repetition is useful, like when I really really want to emphasise a point, but often it's just a typo.
Cleaning up these mistakes has been a fun Friday cleanup task.
