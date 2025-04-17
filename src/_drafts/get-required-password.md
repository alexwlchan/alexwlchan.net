---
layout: post
title: My wrapper around `keyring.get_password()`
summary: If `get_password()` can't find a password, I throw an exception with an error that explains how to set the password, and what password you should choose.
tags:
  - python
  - error messages
---
I'm a big fan of [keyring][pypi], a Python module made by [Jason R. Coombs][jaraco] for storing secrets in the system keyring.
It works on multiple operating systems, and it knows what password store to use for each of them.
For example, if you're using macOS it puts secrets in the [Keychain], but if you're on Windows it uses [Credential Locker].

The keyring module is a safe and portable way to store passwords, more secure than using a plaintext config file or an environment variable.
The same code will work on different platforms, because keyring handles the hard work of choosing which password store to use.

It has a straightforward API: the `keyring.set_password` and `keyring.get_password` functions will handle a lot of use cases.

```pycon
>>> import keyring
>>> keyring.set_password("xkcd", "alexwlchan", "correct-horse-battery-staple")
>>> keyring.get_password("xkcd", "alexwlchan")
"correct-horse-battery-staple"
```

Although this API is simple, it's not perfect -- I have some frustrations with the `get_password` function.
In a lot of my projects, I'm now using a small function that wraps `get_password`.

[pypi]: https://pypi.org/project/keyring/
[jaraco]: https://github.com/jaraco
[Keychain]: https://en.wikipedia.org/wiki/Keychain_%28software%29
[Credential Locker]: https://learn.microsoft.com/en-us/windows/apps/develop/security/credential-locker

## What do I find frustrating about `keyring.get_password`?

If you look up a password that isn't in the system keyring, `get_password` returns `None` rather than throwing an exception:

```pycon
>>> print(keyring.get_password("xkcd", "the_invisible_man"))
None
```

I can see why this makes sense for the library overall -- a non-existent password is very normal, and not exceptional behaviour -- but in my projects, `None` is rarely a usable value.

I normally use keyring to retrieve secrets that I need to access protected resources -- for example, an API key to call an API that requires authentication.
If I can't get the right secrets, I know I can't continue.
Indeed, continuing often leads to more confusing errors when some other function unexpectedly gets `None`, rather than a string.

For a while, I wrapped `get_password` in a function that would throw an exception if it couldn't find the password:

```python
def get_required_password(service_name: str, username: str) -> str:
    """
    Get password from the specified service.

    If a matching password is not found in the system keyring,
    this function will throw an exception.
    """
    password = keyring.get_password(service_name, username)

    if password is None:
        raise RuntimeError(f"Could not retrieve password {(service_name, username)}")

    return password
```

When I use this function, my code will fail as soon as it fails to retrieve a password, rather than when it tries to use `None` as the password.

This worked well enough for my personal projects, but it wasn't a great fit for shared projects.
I could make sense of the error, but not everyone could do the same.

## What's that password meant to be?

A good error message explains what's gone wrong, and gives the reader clear steps for fixing the issue.
The error message above is only doing half the job.
It tells you what's gone wrong (it couldn't get the password) but it doesn't tell you how to fix it.

As I started using this snippet in codebases that I work on with other developers, I got questions when other people hit this error.
They could guess that they needed to set a password, but the error message doesn't explain how, or what password they should be setting.

For example, is this a secret they should pick themselves?
Is it a password in our shared password vault?
Or do they need an API key for a third-party service?
If so, where do they find it?

I still think my initial error was an improvement over letting `None` be used in the rest of the codebase, but I realised I could go further.

This is my extended wrapper:

```python
def get_required_password(service_name: str, username: str, explanation: str) -> str:
    """
    Get password from the specified service.

    If a matching password is not found in the system keyring,
    this function will throw an exception and explain to the user
    how to set the required password.
    """
    password = keyring.get_password(service_name, username)

    if password is None:
        raise RuntimeError(
            "Unable to retrieve required password from the system keyring!\n"
            "\n"
            "You need to:\n"
            "\n"
            f"1/ Get the password. Here's how: {explanation}\n"
            "\n"
            "2/ Save the new password in the system keyring:\n"
            "\n"
            f"       keyring set {service_name} {username}\n"
        )

    return password
```

The `explanation` argument allows me to explain what the password is for to a future reader, and what value it should have.
That information can often be found in a code comment or in documentation, but putting it in an error message makes it more visible.

Here's one example:

```python
get_required_password(
    "flask_app",
    "secret_key",
    explanation=(
        "Pick a random value, e.g. with\n"
        "\n"
        "       python3 -c 'import secrets; print(secrets.token_hex())'\n"
        "\n"
        "This password is used to securely sign the Flask session cookie. "
        "See https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY"
    ),
)
```

If you call this function and there's no keyring entry for `flask_app/secret_key`, you get the following error:

```
Unable to retrieve required password from the system keyring!

You need to:

1/ Get the password. Here's how: Pick a random value, e.g. with

       python3 -c 'import secrets; print(secrets.token_hex())'

This password is used to securely sign the Flask session cookie. See https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY

2/ Save the new password in the system keyring:

       keyring set flask_app secret_key
```

It's longer, but this error message is far more informative.
It tells you what's wrong, how to save a password, and what the password should be.

This is based on a real example where the previous error message led to a misunderstanding.
A co-worker saw a missing password called "secret key" and thought it referred to a secret key for calling an API, and didn't realise it was actually [for signing Flask session cookies][secret_key].
Now I can write a more informative error message, I can prevent that misunderstanding happening again.
(We also renamed the secret, for additional clarity.)

It takes time to write this explanation, which will only ever be seen by a handful of people, but I think it's important.
If somebody sees it at all, it'll be when they're setting up the project for the first time.
I want that setup process to be smooth and straightforward.

I don't use this wrapper in all my code, particularly small or throwaway toys that won't last long enough for this to be an issue.
But in larger codebases that will be used by other developers, and which I expect to last a long time, I use it extensively.
Writing a good explanation now can avoid frustration later.

[secret_key]: https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY
