---
layout: article
date: 2026-04-10 18:00:35 +01:00
title: Auditing my local Python packages
summary: Python's virtual environments mean I can have many versions of the same package scattered across my machine. I've started keeping a list of my environments so I can see exactly what's installed, and where.
topic: Python
---
{#
  Sharing card image from https://www.pexels.com/photo/close-up-photo-of-stacked-carton-boxes-6169669/
#}

Is it just me, or are chain attacks on the rise?
It feels like there are more and more incidents where a bad actor publishes a malicious version of a popular package, people install it on their machines, and they get compromised.
In March alone, such attacks included [Axios npm package][news-axios], the [Trivy vulnerability scanner][news-trivy], and the [LiteLLM Python package][news-litellm].

So far I've been unaffected, because the attacks have only involved libraries or packages I don't use -- but it would be foolish to imagine that will always be the case.
I have a lot of local Python projects, and I've been thinking about how I'd react if a Python package I use was compromised.

The first step is detection: once I know a package version is malicious, how do I know if I've installed it?
Because I use virtual environments, this turns out to be a non-trivial question.

## What are virtual environments?

[Virtual environments][pydoc-venv] (or "virtualenvs") are a tool to create isolated Python environments, each with its own set of installed packages.
They allow you to have different dependencies for different projects.
For example, if two projects depend on different versions of the same package, you can create per-project virtualenvs, each with the appropriate version.

A virtualenv is stored in a folder that includes symlinks to the global Python interpreter and the packages you've installed in the virtualenv.
When you "activate" the virtualenv, commands like `pip install` install packages in the virtualenv folder rather than your global Python.

Here's an example:

```console
$ # `python3` points to my global interpreter
$ which python3
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3

$ # Create the virtualenv
$ python3 -m venv .venv

$ # Activate the virtualenv, so now `python3` and `pip` commands will
$ # run inside the virtualenv
$ source .venv/bin/activate

$ # `python3` now points to the symlink in the virtualenv
$ which python3
/private/tmp/example/.venv/bin/python3

$ # Pillow will be installed inside the `.venv` folder
$ pip install Pillow
```

I create a new virtualenv for every Python project, so I have a lot of different virtualenvs on my personal Mac.

To check if I'd installed version&nbsp;X of package&nbsp;Y, I'd have to check each of my virtualenvs.
Python itself doesn't keep a running list of virtualenvs I've created, so I have to manage that list myself.

## Getting a list of my virtualenvs

I'm very consistent about naming my virtualenvs: the folder is always named `.venv`.
(I actually have a [shell function][fish-fn] for creating virtualenvs, which enforces that convention.)

This means I can find all the virtualenvs in my home directory with a one-line command:

```console
$ find ~ -type d -name .venv
/Users/alexwlchan/repos/snippets/.venv
/Users/alexwlchan/repos/alexwlchan.net/.venv
/Users/alexwlchan/repos/colour-scheme/.venv
…
```

I can similarly search external drives and volumes where I have virtualenvs:

```console
$ find /Volumes/Media/ -type d -name .venv
/Volumes/Media/Screenshots/.venv
/Volumes/Media/Social Media/.venv
/Volumes/Media/Bookmarks/.venv
…
```

These commands take about 30 seconds to run -- just long enough to be annoying -- so I've saved the results to a text file:

```console
$ find ~ -type d -name .venv >> ~/.venv_registry
$ find /Volumes/Media/ -type d -name .venv >> ~/.venv_registry
```

I've also modified my shell function that creates virtualenvs to update this file whenever I create a new virtualenv.
Now I have an up-to-date list of all my virtualenvs that I can use to search for vulnerable dependencies.

## What about Python packages installed outside virtualenvs?

If you run `pip install` without activating a virtualenv, the packages will get installed in your global Python installation, and they wouldn't be included in this list.
This is generally a bad idea, because you're back to the problem of different projects using incompatible dependencies.

You can tell pip that it should [only use virtualenvs][pip-require-venv], either with an environment variable or a config file.
Once you set up that config, pip will refuse to install packages outside a virtualenv.

Alternatively, if you use uv instead of pip, you can't install packages outside a virtualenv unless you explicitly pass the `--system` flag to modify your system Python.

I set the `PIP_REQUIRE_VIRTUALENV=true` in my shell config file, and I use uv, so I don't have any Python packages installed outside virtualenvs.

## Searching my virtualenvs for package versions

Now I have a text file with a list of all my virtualenvs, I can write scripts that run commands in each of them.

For example, here's a bash script that runs `uv pip freeze` in every virtualenv to print a list of installed dependencies:

<pre class="lng-bash"><code><span class="ch">#!/usr/bin/env bash</span>

set -o errexit
set -o nounset

<span class="k">while</span> read -r <span class="n">venv_dir</span><span class="p">;</span> <span class="k">do</span>
  <span class="k">if</span> ! test -d <span class="s2">"</span>$venv_dir<span class="s2">"</span><span class="p">;</span> <span class="k">then</span>
    echo <span class="s2">"does not exist: </span>$venv_dir<span class="s2">"</span> &gt;&2
    continue
  <span class="k">fi</span>
  
  echo <span class="s2">"== </span>$venv_dir<span class="s2"> =="</span>
  uv pip freeze --python <span class="s2">"</span>$venv_dir<span class="s2">/bin/python"</span>
  echo <span class="s2">""</span>
<span class="k">done</span> &lt; ~/.venv_registry</code></pre>

Within half a second, I have a complete list of every Python package installed in every virtualenv on my Mac.
I dump the output to a text file, and then I can look for compromised package versions -- or reassure myself that I don't have a package installed, not even as an indirect dependency.

I skip missing virtualenvs because they're probably temporary environments I have yet to clean up from my registry, or virtualenvs on external drives that are currently unmounted.

I like that this script doesn't run the Python interpreter itself, so I won't make things worse if I've already installed a malicious package.
In particular, uv is a Rust tool that doesn't run any Python code, it just knows how to understand Python installations.

For example, with the recent LiteLLM compromise, the attackers [installed a `.pth` file][news-litellm-pth] which would run as soon as you started Python, even if you didn't import LiteLLM.
Even a basic `python --version` or `pip freeze` would compromise your machine.
I could easily modify this script to look for the malicious `.pth` file in all of my Python environments, without ever running Python.

## Other uses for a virtualenv registry 

I originally wrote this to detect compromised packages, but I found other uses:

*   I can find outdated versions of packages, and make sure all my virtualenvs are up-to-date.

*   If I'm trying to stop using a package, I can find any places I'm stll using it and remove it.
    For example, I'm trying to replace some third-party HTTP libraries with the standard library, and these scripts help me find where I'm still using the third-party libraries.

*   I can search all my Python code for places where I use specific functions or features, in a more efficient way than grepping my entire disk.
    For example, I have a couple of personal utility libraries, and I can see which functions I'm still using and which can be deleted.
    I do this by searching the parent directory of each `.venv` path, which is the root of each project.

I hope none of the libraries I use are ever compromised, but if they are, I'll be ready -- and in the meantime, this is a useful tool to have around.

[fish-fn]: /2023/fish-venv/#create-function
[news-axios]: https://cloud.google.com/blog/topics/threat-intelligence/north-korea-threat-actor-targets-axios-npm-package
[news-litellm]: https://www.stepsecurity.io/blog/litellm-credential-stealer-hidden-in-pypi-wheel
[news-litellm-pth]: https://www.stepsecurity.io/blog/litellm-credential-stealer-hidden-in-pypi-wheel#the-entry-points-two-versions-two-injection-techniques
[news-trivy]: https://www.stepsecurity.io/blog/trivy-compromised-a-second-time---malicious-v0-69-4-release
[pip-require-venv]: https://docs.python-guide.org/dev/pip-virtualenv/#requiring-an-active-virtual-environment-for-pip
[pydoc-venv]: https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments
