---
layout: post
title: Setting up Fish to make virtualenv easier
summary: I wrote some shell config to smooth out the experience of using virtual environments in Python.
colors:
  index_light: "#13388f"
  index_dark:  "#edd347"
tags: 
  - python
  - programming
  - fish-shell
card_attribution: |
  Yellow fish by Samarth Singhai on Pexels: https://www.pexels.com/photo/yellow-fish-in-close-up-photography-1145274/
  Used under the Pexels license; retrieved 18 December 2023.
---

Since I started my new job, I've been doing a lot more work in Python.
As I was starting with a completely clean slate, I wanted to try setting up Python the "right" way – or [if not "right"][xkcd], at least better way than my previous pile of hacks and kludges.

(I honestly don't remember the details of my old approach, but I know it was messy.
At one point I used Homebrew and virtual environments, but I got burnt by Homebrew unexpectedly breaking Python, so I scrapped it and started installing everything in my global Python installation.
Don't do that.)

In August I read Glyph's post [Get Your Mac Python From Python.org][glyph] and it all seemed like sensible advice, so I decided to use that as my starting point.
I downloaded Python on my new work laptop from Python.org, and I started using virtual environments for everything.

This worked well enough, but there were some rough edges in my new workflow.
I've been tweaking [my Fish shell config][fish] to smooth them out.

[xkcd]: https://xkcd.com/1987/
[glyph]: https://blog.glyph.im/2023/08/get-your-mac-python-from-python-dot-org.html
[fish]: https://github.com/alexwlchan/scripts

## Requiring virtual environments with PIP_REQUIRE_VIRTUALENV

One recommendation in Glyph's post is that you [always use virtual environments][always], and they suggest a way to enforce that:

> Once you have installed Python from python.org, never `pip install` anything globally into that Python, even using the `--user` flag. Always, always use a virtual environment of some kind. In fact, I recommend configuring it so that it is not even possible to do so, by putting this in your `~/.pip/pip.conf`:
> 
> ```ini
> [global]
> require-virtualenv = true
> ```

I like the idea, but I'm not a fan of having lots of config files in my home directory – I struggle to keep them up-to-date, and after a while I lose track of which config is still in use, and what's leftover cruft from a tool I no longer use.
Each config file also becomes one more thing to remember to set up when I get a new computer.

Fortunately, this config file isn't the only way to ensure you always use a virtual environment.
You can also [set the `PIP_REQUIRE_VIRTUALENV` environment variable][envvar], so I have the following lines in my [fish shell config]:

```shell
# This prevents me from installing packages with pip without being
# in a virtualenv first.
#
# This allows me to keep my system Python clean, and install all my
# packages inside virtualenvs.
#
# See https://docs.python-guide.org/dev/pip-virtualenv/#requiring-an-active-virtual-environment-for-pip
# See https://blog.glyph.im/2023/08/get-your-mac-python-from-python-dot-org.html#and-always-use-virtual-environments
#
set -g -x PIP_REQUIRE_VIRTUALENV true
```

Because I keep my shell config in Git, it's easier to see when I added this variable, and when I get a new computer I'll get this right behaviour "for free".

[always]: https://blog.glyph.im/2023/08/get-your-mac-python-from-python-dot-org.html#and-always-use-virtual-environments
[envvar]: https://docs.python-guide.org/dev/pip-virtualenv/#requiring-an-active-virtual-environment-for-pip

## A function to create and auto-enable new virtual environments

The process of creating new virtual environments is ostensibly simple – you just have to run two commands.

```console
$ python3 -m venv .venv
$ source .venv/bin/activate.fish
```

In practice I only ever remembered to run the first – I'd create my new virtual environment, go to `pip install` something, and then it would complain I hadn't enabled a virtual environment.
I'd mutter and grumble, activate it, then move on.

If I'm creating a virtual environment, I want to use it immediately, so I wrapped this process in a Fish function called `venv`:

```shell
function venv --description "Create and activate a new virtual environment"
    echo "Creating virtual environment in "(pwd)"/.venv"
    python3 -m venv .venv --upgrade-deps
    source .venv/bin/activate.fish

    if test -e .git
        # Append .venv to the Git exclude file, but only if it's not
        # already there.
        set target_file ".git/info/exclude"
        set line_to_append ".venv"
    
        if not grep --quiet --fixed-strings --line-regexp "$line_to_append" "$target_file"
            echo $line_to_append >> $target_file
        end
    end
end
```
