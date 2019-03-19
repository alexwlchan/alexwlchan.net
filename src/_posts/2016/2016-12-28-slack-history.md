---
layout: post
date: 2016-12-28 10:29:00 +0000
link: https://pypi.org/project/slack-history/
tags: python slack
title: A tool for backing up your message history from Slack
category: Programming and code
---

I've just pushed a small tool to PyPI for backing up message history from Slack.
It downloads your message history as a collection of JSON files, including public/private channels and DM threads.

This is mainly scratching my own itch: I don't like having my data tied up in somebody's proprietary system.
Luckily, Slack [provides an API][api] that lets you get this data out into a plaintext form.
This allows me to correct what I see as two deficiencies in the [data exports provided by Slack][exports]:

*   They only back up public channels, not private channels or direct messages.
*   They're only available to team admins, not individual users.

Installation is `pip install slack_history`, then run `slack_history --help` for usage instructions.

Enjoy!

[api]: https://api.slack.com/
[exports]: https://get.slack.help/hc/en-us/articles/204897248
