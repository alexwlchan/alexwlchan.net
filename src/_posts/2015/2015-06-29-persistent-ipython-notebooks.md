---
layout: post
date: 2015-06-29 17:55:00 +0000
summary: Configuring an IPython notebook server that is always running and easily
  accessible in Windows.
tags: python windows
title: Persistent IPython notebooks in Windows
category: Programming and code
---

I've been using [IPython][ipy] for about six months, and I've grown to love the [web-based notebook interface][notebook]. It's became my go-to environment when I want to do simple calculations, or test a new idea in Python. It's also a lovely environment for [literate programming][litprog], and I wish I'd had it for my university coursework.[^1]

On my Mac, I've been using [some scripts by Nathan Grigg][ngrigg] to keep my IPython notebook server running continuously, and to give it a nicer hostname. Over the weekend, I realised that 1) IPython would be really useful at work, and 2) since my work computer is a PC, I need to adapt his scripts to work with Windows.

This post explains how to get a persistent IPython notebook on Windows. The ideas are based on Nathan's post, but the implementation is a little different.

<!-- summary -->

## Install IPython

I installed Python 3.4[^2], then set up a virtualenv and installed IPython:

```
C:\Users\AWLC> C:\Python34\Scripts\virtualenv.exe ipython
C:\Users\AWLC> ipython\Scripts\activate.bat
(ipython) C:\Users\AWLC> pip install ipython
```

For some reason, this didn't install all the notebook dependencies. I needed to install a few more modules:

```
(ipython) C:\Users\AWLC> pip install pyzmq jinja2 tornado jsonschema
```

Then I could start an IPython notebook server with `ipython notebook`, but I had to run that command myself, every time I logged in. Time to automate that step.

## Always running server with Task Scheduler

First I created a Batch script that started my IPython server:

```batch
C:\Users\AWLC\ipython\Scripts\ipython.exe notebook^
 --no-browser^
 --port=80^
 --ip=127.0.0.13^
 --notebook-dir=C:\Users\AWLC\Drive\Notebooks
PAUSE
```

Most of those options are fairly self-explanatory. The only line worth discussing is `--ip`, where I've used 127.0.0.13 instead of the conventional 127.0.0.1. In IPv4, the entire 127.0.0.0/8 address block is available for loopback. That means any 127.x.x.x address can act like a localhost address (at least on Windows; a [little extra work][super] is required to set this up on OS X).

Like Nathan, I have lots of processes serving to localhost, but I use different loopback addresses – rather than different ports – to keep them separate. I find this simpler than setting up Apache and configuring port forwarding.

Having created this script, now it needs to run whenever I log in. I created a new item in Task Scheduler with a "Start a program" action, and the following program:

```
cmd /c start "IPython notebook" /min "C:\Users\AWLC\bin\start_ipython.bat"
```

Here `start_ipython.bat` is the Batch script I wrote above. I also supply the `/min` flag, which auto-minimises the command window. I haven't found a way to hide it entirely (at least not without giving the script admin permissions), but it's better than nothing.

I also tweaked the task settings so that it auto-runs at login and tries to resume if the task fails.

So now I have an always-running IPython server at <http://127.0.0.13>. Finally, let's give it a nicer hostname.

## Setting a virtual host

The hosts file in Windows lives at `C:\Windows\System32\drivers\etc\hosts`. After opening that (as an administrator), I added the following line:

```
127.0.0.13 py
```

The change took effect immediately: now `py` resolves to `127.0.0.13`, and I can access my IPython server by going to `py` in my browser.

[^1]: My second and third year coursework, called [CATAM][catam], was a mixture of programming and mathematics. We had to write programs for solving mathematical problems that were difficult to solve by hand. I wrote my programs in Python, and my writeup in LaTeX, because I needed to interleave program code and the underlying maths.</p><p>IPython notebooks allow you to intersperse Markdown, MathJax and code in an easy way. If you have to write something that combines maths and programming, I really suggest you give these notebooks a look.

[^2]: I've finally seen the light and switched to writing Python 3 for my new projects, after being stuck on Python 2 for years. There wasn't a single big thing that persuaded me to change, just a growing collection of little "ooh, that looks nice" moments that pushed me over the edge.

[ipy]: http://ipython.org/
[notebook]: http://ipython.org/notebook.html
[litprog]: https://en.wikipedia.org/wiki/Literate_programming
[ngrigg]: http://nathangrigg.net/2015/03/ipython-virtualhost-proxy/
[catam]: http://www.maths.cam.ac.uk/undergrad/catam/
[super]: http://superuser.com/a/458877/243137