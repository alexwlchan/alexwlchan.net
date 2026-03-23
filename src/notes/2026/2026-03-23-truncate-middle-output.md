---
layout: note
date: 2026-03-23 21:02:20 +00:00
title: How to truncate the middle of long command output
summary: Use a command group `{ head -n 3; echo '[…]'; tail -n 5; }` to snip print the first few and last few lines.
topic: Shell scripting
---

If I'm running a command with lots of output, I can use [`head(1)`][head1] to get the first few lines, or [`tail(1)`][tail1] to get the last few lines.
What if I want to get some lines from the beginning and from the end, but truncate the middle?

In bash, I can use [command grouping][bash-command-grouping], which runs all the commands inside curly braces as a single unit.
Here's an example:

```console
$ tailscale exit-node list | { head -n 3; echo ' […]'; tail -n 5; }

 IP                  HOSTNAME                         COUNTRY            CITY                   STATUS
 100.111.189.27      al-tia-wg-003.mullvad.ts.net     Albania            Tirana                 -
 […]
 100.93.242.75       ua-iev-wg-001.mullvad.ts.net     Ukraine            Kyiv                   -

# To view the complete list of exit nodes for a country, use `tailscale exit-node list --filter=` followed by the country name.
# To use an exit node, use `tailscale set --exit-node=` followed by the hostname or IP.
# To have Tailscale suggest an exit node, use `tailscale exit-node suggest`.
```

[bash-command-grouping]: https://www.gnu.org/software/bash/manual/html_node/Command-Grouping.html
[head1]: https://alexwlchan.net/man/man1/head.html
[tail1]: https://alexwlchan.net/man/man1/tail.html
