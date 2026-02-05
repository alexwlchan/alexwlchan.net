---
layout: post
title: Creating Caddyfiles with Cog
summary: Cog is a tool for doing in-place text generation for static files. It's useful for generating repetitive config, like my web server redirects.
date: 2026-02-05 08:21:14 +00:00
topic: Python
---
I'm currently restructuring my site, and I'm going to change some of the URLs.
I don't want to [break inbound links][wiki-link-rot] to the old URLs, so I'm creating [redirects][wiki-redirects] between old and new.

My current web server is [Caddy][caddy], so I define redirects in my Caddyfile with the [`redir` directive][caddy-redir].
Here's an example that creates permanent redirects for three URLs:

<pre><code><span class="n">alexwlchan.net</span> <span class="p">{</span>
  redir /videos/crossness_flywheel.mp4  /files/2017/crossness_flywheel.mp4 permanent
  redir /2021/12/2021-in-reading/       /2021/2021-in-reading/ permanent
  redir /2022/12/print-sbt/             /til/2022/print-sbt/ permanent
<span class="p">}</span></code></pre>

This syntax is easy to write by hand, but it's annoying if I want to define lots of redirects -- and when I'm doing a big restructure, I do.
In particular, it's tricky to write scripts to modify this file.

This is a good use case for [Cog][cog], made by Ned Batchelder.

## How I automate this with Cog

Cog is a tool for running snippets of Python inside text files, allowing you to generate content without external templates or additional files.
When you process a file with Cog, it finds those snippets of Python, executes them, then inserts the output back into the original file.

Here's an example:

<pre><code><span class="n">alexwlchan.net</span> <span class="p">{</span>
  <span class="c">#[[[cog
  # import cog
  # 
  # redirects = [
  #     {"old_url": "/videos/crossness_flywheel.mp4", "new_url": "/files/2017/crossness_flywheel.mp4"},
  #     {"old_url": "/2021/12/2021-in-reading/", "new_url": "/2021/2021-in-reading/"},
  #     {"old_url": "/2022/12/print-sbt/", "new_url": "/til/2022/print-sbt/"},
  # ]
  # 
  # for r in redirects:
  #     cog.outl(f"redir {r['old_url']} {r['new_url']} permanent")
  #]]]
  #[[[end]]]</span>
<span class="p">}</span></code></pre>

All the Python code that Cog runs is inside a comment, so it will be ignored by Caddy.
The `[[[cog …]]]` and `[[[end]]]` markers tell Cog where to find the code, and it's smart enough to remove the leading whitespace and comment markers.

When I process this file with Cog (`pip install cogapp; cog Caddyfile`), it runs the Python snippet, and anything passed to `cog.outl()` is written between the markers.
This is the output, which gets printed to stdout:

<pre><code><span class="n">alexwlchan.net</span> <span class="p">{</span>
  <span class="c">#[[[cog
  # import cog
  # 
  # redirects = [
  #     {"old_url": "/videos/crossness_flywheel.mp4", "new_url": "/files/2017/crossness_flywheel.mp4"},
  #     {"old_url": "/2021/12/2021-in-reading/", "new_url": "/2021/2021-in-reading/"},
  #     {"old_url": "/2022/12/print-sbt/", "new_url": "/til/2022/print-sbt/"},
  # ]
  # 
  # for r in redirects:
  #     cog.outl(f"redir {r['old_url']} {r['new_url']} permanent")
  #]]]</span>
  redir /videos/crossness_flywheel.mp4 /files/2017/crossness_flywheel.mp4 permanent
  redir /2021/12/2021-in-reading/ /2021/2021-in-reading/ permanent
  redir /2022/12/print-sbt/ /til/2022/print-sbt/ permanent
  <span class="c">#[[[end]]]</span>
<span class="p">}</span></code></pre>

If I want to write the output back to the file, I run Cog with the `-r` flag (`cog -r Caddyfile`).
All the original Cog code is preserved, so I can run it again and again to regenerate the file.
This means that if I want to add a new redirect, I can edit the list and run Cog again.

Cog is running a full version of Python, so I can rewrite the snippet to read the list of redirects *from an external file*.
Here's another example:

<pre><code><span class="n">alexwlchan.net</span> <span class="p">{</span>
  <span class="c">#[[[cog
  # import cog
  # import json
  #
  # with open("redirects.json") as in_file:
  #     redirects = json.load(in_file)
  # 
  # for r in redirects:
  #     cog.outl(f"redir {r['old_url']} {r['new_url']} permanent")
  #]]]</span>
  redir /videos/crossness_flywheel.mp4 /files/2017/crossness_flywheel.mp4 permanent
  redir /2021/12/2021-in-reading/ /2021/2021-in-reading/ permanent
  redir /2022/12/print-sbt/ /til/2022/print-sbt/ permanent
  <span class="c">#[[[end]]]</span>
<span class="p">}</span></code></pre>

This is a powerful change -- unlike the original Caddyfile, it's easy to write scripts that insert entries in this external JSON file, and now I can programatically update this file.

My scripts that are rearranging my URLs can populate `redirects.json`, then I only need to re-run Cog and I have a complete set of redirects in my Caddyfile.

I usually run Cog with two flags:

*   `-r` writes the output back to the original file, and
*   `-c` adds a checksum to the end marker, like `[[[end]]] (sum: Rwh4n2CfQD)`.
    This checksum allows Cog to detect if the output has been manually edited since it last processed the file -- and if so, it will refuse to overwrite those changes.
    You have to revert the manual edits or remove the checksum.

You can also run Cog with a `--check` flag, which checks if a file is up-to-date.
I run this as a [continuous integration task][cog-ci], to make sure I've updated my files properly.

## Why I like Cog

What separates Cog from traditional templating engines like Jinja2 or Liquid is that it operates entirely in-place on the original file.
Usually, you have a source template file and a build step which produce a separate output file, but with Cog, the source and the result are stored in the same document.
Storing templates in separate files is useful for larger projects, but it's overkill for something like my Caddyfiles.

Having everything in a single file makes it easy to resume working on a file managed with Cog.
I don't need to remember where I saved the build script or the template; I can operate directly on that single text file.
If I come back to this project in six months, the instructions for how the file is generated are right in front of me.

The design also means that I'm not locked into using Cog.
At any point, I could delete the Cog comments and still have a fully functional file.

Cog isn't a replacement for a full-blown templating language, and it's not the right tool for larger projects -- but it's indispensable for small amounts of automation.
If you've never used it, I recommend [giving it a look][cog] -- it's a handy tool to know.

[caddy]: https://caddyserver.com/
[caddy-redir]: https://caddyserver.com/docs/caddyfile/directives/redir
[cog]: https://cog.readthedocs.io/en/latest/
[cog-ci]: https://cog.readthedocs.io/en/latest/running.html#continuous-integration
[wiki-link-rot]: https://en.wikipedia.org/wiki/Link_rot
[wiki-redirects]: https://en.wikipedia.org/wiki/Http_redirect
