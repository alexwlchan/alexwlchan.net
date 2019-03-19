---
layout: post
date: 2017-10-20 17:11:59 +0000
title: Using hooks for custom behaviour in requests
tags: python
summary: I often have code I want to run against every HTTP response (logging, error checking) --- event hooks give me a nice way to do that without repetition.
category: Programming and code
---

Recently I've been writing a lot of scripts with [python-requests][requests] to interact with a new API.
It starts off with a simple GET request:

```python
resp = requests.get('http://example.com/api/v1/assets', params={...})
```

I want to make sure that the request succeeded before I carry on, so I [throw an exception][raise_for_status] if I got an error responses:

```python
resp = requests.get('http://example.com/api/v1/assets', params={...})
resp.raise_for_status()
```

If I get an error, the server response may contain useful debugging information, so let's log that as well (and actually, logging it might be generally useful):

```python
resp = requests.get('http://example.com/api/v1/assets', params={...})

try:
    resp.raise_for_status()
except requests.HTTPError:
    logger.error('Received error %s', resp.text)
    raise
else:
    logger.debug('Received response %s', resp.text)
```

And depending on the API, I may want even more checks or logging.
For example, APIs that always return an HTTP 200 OK, but embedded the real response code in a JSON response.
Or maybe I want to log the URL I requested.

If I'm making lots of calls to the same API, repeating this code gets quite tedious.
Previously I would have wrapped `requests.get` in a helper function, but that relies on me remembering to use the wrapper.

It turns out there's a better way --- today I learnt that requests has a [hook mechanism][hooks] that allows you to provide functions that are called after every response.
In this post, I'll show you some simple examples of hooks that I'm already using to clean up my code.

[requests]: http://docs.python-requests.org/en/master/
[raise_for_status]: http://docs.python-requests.org/en/master/api/#requests.Response.raise_for_status
[hooks]: http://docs.python-requests.org/en/master/user/advanced/#event-hooks

<!-- summary -->

## Defining a hook

A hook function takes a Response object, and some number of args and kwargs.
For example, if we wanted a hook function that called `raise_for_status` on every response, this is what we'd write:

```python
def check_for_errors(resp, *args, **kwargs):
    resp.raise_for_status()
```

If you want requests to call this function on a response, you put it in a dictionary `{'response': check_for_errors}`.
Then you pass this dictionary in the `hooks` parameter to a requests method:

```python
requests.get(
    'http://example.com/api/v1/assets',
    hooks={'response': check_for_errors}
)
```

If you want to call multiple hooks, you can also provide a list of functions.
For example:

```python
def print_resp_url(resp, *args, **kwargs):
    print(resp.url)

requests.get(
    'http://example.com/api/v1/assets',
    hooks={'response': [print_resp_url, check_for_errors]}
)
```

Already, this gives us slightly cleaner code --- but we still have to remember to use the hooks whenever we make an HTTP request.
And what if we think of another hook later, and want to add it to all our existing calls?
It turns out there's an even cleaner way to write this.

## Enter the Session API

So far we've only used requests's functional API, but another way to use requests is with [Session objects][sessions].
Using a Session allows you to share cookies, connections and configuration between multiple requests --- so it's already useful if you're calling the same API repeatedly --- and also hooks!

Using the Session API is very similar to the functional API --- you create a `Session` object, then call methods on the object.
(In fact, the functional API uses sessions [under the hood][hood].)
For example:

```python
sess = requests.Session()

sess.get(
    'http://example.com/api/v1/assets',
    hooks={'response': [print_resp_url, check_for_errors]}
)
```

But Sessions allow us to share configuration between requests.
We don't get any hooks by default:

```python
print(sess.hooks)
# {'response': []}
```

So instead, we add them after we've created the `Session` object:

```python
sess = requests.Session()
sess.hooks['response'] = [print_resp_url, check_for_errors]

sess.get('http://example.com/api/v1/assets')
```

and those hooks will now be used for *every* request made using that session.

Now we can run a consistent set of hooks on every request, but without having repetition throughout our project.
And if we update the hooks once, we update the hooks everywhere.
Win!

[sessions]: http://docs.python-requests.org/en/master/user/advanced/#session-objects
[hood]: https://github.com/requests/requests/blob/22d12b0501fa633b80bcda303a718696e408ebfb/requests/api.py#L57-L58

## Simple examples of hooks

I've already shown you two examples of hooks I've written: one to check for errors, another to log the responses.

```python
def check_for_error(resp, *args, **kwargs):
    resp.raise_for_status()


def log_response_text(resp, *args, **kwargs):
    logger.info('Got response %r from %s', resp.text, resp.url)
```

Because a hook can modify the response object (if it returns a non-`None` value), you could also use it to edit responses for a more consistent downstream API.
Maybe an API that usually returns XML could return JSON instead --- but I haven't experimented with that yet.

Right now, these feel like the most natural use cases for hooks.
I wouldn't want to put business logic in a hook --- suddenly hiding the hook implementation makes the code harder to follow --- but for simple bookkeeping and error handling, I can see this being really useful.

Now I know that hooks exist, I imagine I'll find more uses for them.
If you want to learn more about hooks, there's a bit more detail [in the requests documentation][docs].
I also did a bit of reading of the [source code for requests.sessions][src], but otherwise a bit of experimenting was enough to get me going.

[docs]: http://docs.python-requests.org/en/master/user/advanced/#event-hooks
[src]: http://docs.python-requests.org/en/master/_modules/requests/sessions/?highlight=hooks

<!-- ## Other hook points?

In early versions of requests, you could also fire hooks before the Request object was sent --- `pre_request` and `pre_send` hooks, for example.
These all got removed [in version 1.0][v1], and haven't come back.

[v1]: http://docs.python-requests.org/en/latest/community/updates/#id71 -->
