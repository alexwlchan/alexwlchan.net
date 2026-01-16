---
layout: til
title: With Flask-Login, you want `current_user == None`, not `current_user is None`
summary: "`current_user` is a proxy object that happens to be wrapping `None`, but isn't actually `None`."
date: 2024-09-03 10:23:25 +01:00
tags:
  - python
  - flask
---
I was writing some code that uses Flask-Login, and I wanted to test the scenario where a user wasn't logged in.

I get the value of `current_user`, and it's `None`:

```pycon
>>> from flask_login import current_user
>>> current_user
None
```

Great!
So now I can check if this value is `None`, and react accordingly:

```pycon
>>> if current_user is None:
...     print("Nobody is logged in!")
...
>>>
```

Hmm.

If you look at [how Flask-Login works](https://github.com/maxcountryman/flask-login/blob/2ad14589b1022462db298133063b291459b71782/src/flask_login/utils.py#L23-L25), you see that `current_user` is defined as a `LocalProxy` that wraps the `_get_user()` function:

```python
from werkzeug.local import LocalProxy

...

#: A proxy for the current user. If no user is logged in, this will be an
#: anonymous user
current_user = LocalProxy(lambda: _get_user())
```

This `LocalProxy` class is some sort of wrapper.
The [Werkzeug docstring](https://github.com/pallets/werkzeug/blob/5add63c955131fd73531d7369f16b2f1b4e342d4/src/werkzeug/local.py#L389C8-L389C61) describes it as *"a proxy to the object bound to a context-local object"* which doesn't mean much to me, but I can see that it's getting in the way of the identity checks.

In particular, the wrapper is equal to `None` but not identical to it:

```pycon
>>> p = LocalProxy(lambda: None)
>>> p
None
>>> p == None
True
>>> p is None
False
>>> id(p)
4349196416
>>> id(None)
4343995648
```

This means my code has to use `current_user == None`, not `current_user is None`.
This looks odd -- generally it's better Python to use `is None` as a comparison, but in this case it won't work.
