---
layout: post
date: 2016-11-16 07:48:00 +0000
summary: If you need to store passwords in a Python application, use the keyring module
  to keep them safe.
tags: python security
title: Use keyring to store your credentials
---

I write a lot of Python scripts that interact with online services, which usually means requires my passwords and API keys.
But how to store them?

The simplest approach would be to save my variable in my unencrypted source code:

```python
PASSWORD = 'password!'
```

**This is a terrible idea.  Don't do this.**

This password is now trivially accessible to anybody who has access to the source code.
If I ever want to share my code (and I often do), I have to remember to carefully scrub it of sensitive information.
If I use a version control system like Git, the password is permanently baked into the history of the repository.[^1]

[^1]: There are bots that [continually watch GitHub](http://www.theregister.co.uk/2015/01/06/dev_blunder_shows_github_crawling_with_keyslurping_bots/) for API keys and passwords.
If you ever push unencrypted secrets to a shared repository, you should consider them compromised *instantly*.

So what's the alternative?
If I don't want to put secrets directly in the source code, how can I make them available at runtime?
I use [the keyring module](https://pypi.org/project/keyring/).

<!-- summary -->

The keyring module provides a wrapper around your system's password store: for example, the OS X Keychain, or the Windows Credential Vault.
These typically provide much more security than keeping the password in source control, or in another file that gets included at runtime.
And they're entirely decoupled from your source code: if you always use keyring, you never have to worry about forgetting to expunge secrets from your code.

Most of the time, I use just two functions: `get_password` and `set_password`.
Here's an example of setting and then retrieving a password:

```pycon
>>> import keyring
>>> keyring.set_password('twitter', 'xkcd', 'correct horse battery staple')
>>> keyring.get_password('twitter', 'xkcd')
'correct horse battery staple'
```

If you don't want to type your password in the clear, combine this with [getpass][getpass] like so:

```pycon
>>> keyring.set_password('twitter', 'xkcd', getpass.getpass())
Password: [password is typed here, but not printed to screen]
```

There's also a command line tool you can use if you want to look up passwords in shell scripts:

```console
$ python -m keyring get twitter xkcd
correct horse battery staple
```

I much prefer writing code that uses keyring, because my source code is never contaminated with secret information.
I never have to worry that I'll leak passwords in source code.
All you learn is the name of an entry in my local keychain – and if you're in a position to make use of that information, I'm already screwed.

[getpass]: https://docs.python.org/3.5/library/getpass.html

System keychains definitely aren't perfect, and using keyring doesn't prevent you from leaking your password in other ways.
But it reduces your attack surface, and gives you a bit more peace of mind if you're sharing code.
I'd recommend [giving it a try](https://pypi.org/project/keyring/).
