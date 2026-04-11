---
layout: article
date: 2026-04-24 16:14:03 +02:00
title: HTTP GET requests with the Python standard library
summary: For my local scripting, a lightweight wrapper around the Python standard library gets me a friendly API without the dependencies.
topic: Python
---
{#
  Sharing card image from https://www.pexels.com/photo/shallow-focus-of-purple-flowers-533297/
#}

If you're doing HTTP in Python, you're probably using one of three popular libraries: [requests][requests], [httpx][httpx], or [urllib3][urllib3]; I've used each of them at different times.
These libraries are installed with pip, live outside the standard library, and provide more features than the built-in [`urllib.request` module][urllib-request] -- indeed, the documentation for that module recommends using requests.

Recently I've been looking for a new HTTP library, because my previous choice seems abandoned.
I was using httpx, but the maintainer has closed issues on the GitHub repo, there's only been one commit since January,  and the last release was over a year ago.
The easy choice would be switching to requests or urllib3, but I wondered: can I just use the standard library?

My usage is pretty basic -- I have some manually-invoked scripts that make a handful of GET requests to public websites.
I don't have long-running processes; I'm not making thousands of requests at once; I'm not using proxies or authentication.
There are plenty of features you can only get from third-party HTTP libraries -- from connection pooling to HTTP/2 support -- but I don't need any of them.

I started experimenting, and what I realised is that I don't miss the features, but I do miss the API.

Here's how you make a basic GET request with httpx:

```python {"names":{"1":"httpx","2":"resp"}}
import httpx

resp = httpx.get(
    "https://example.com",
    params={"name": "pentagon", "sides": "5"},
    headers={"User-Agent": "Shape-Sorter/1.0"}
)
print(resp.content)
```

Here's the same request with `urllib.request`:

```python {"names":{"1":"urllib","2":"parse","3":"urllib","4":"request","5":"url","6":"params","7":"headers","8":"u","13":"query","31":"req","38":"resp"}}
import urllib.parse
import urllib.request

url = "https://example.com"
params = {"name": "pentagon", "sides": "5"}
headers = {"User-Agent": "Shape-Sorter/1.0"}

u = urllib.parse.urlsplit(url)
query = urllib.parse.urlencode(params)
url = urllib.parse.urlunsplit(
    (u.scheme, u.netloc, u.path, query, u.fragment)
)

req = urllib.request.Request(url, headers=headers)

resp = urllib.request.urlopen(req)
print(resp.read())
```

Verbose!
I've wrapped it in a helper function in [chives][chives], my personal utility library.
Here's the same request a third time:

```python {"names":{"1":"chives","2":"fetch","3":"fetch_url","4":"resp"}}
from chives.fetch import fetch_url

resp = fetch_url(
    "https://example.com",
    params={"name": "pentagon", "sides": "5"},
    headers={"User-Agent": "Shape-Sorter/1.0"}
)
print(resp)
```

Much cleaner!

The code in chives does have one dependency -- [certfi][certifi], a lightweight package that provides Mozilla's collection of root certificates.

There are lots of good reasons to use a third-party HTTP library, but I can do everything I need with the standard library and my personal wrapper.
Let's go through how it works.

{% table_of_contents %}

## Building the `urllib.request.Request` object

The first step is building the [`Request` object][urllib-request-object].
Other HTTP libraries provide helper functions or hide this step for simple requests (notice the basic `httpx.get` call doesn't mention an `httpx.Request`), but for `urllib.request` we have to do it ourselves.
Here's mine:

```python {"names":{"1":"urllib","2":"parse","3":"urllib","4":"request","5":"QueryParams","13":"Headers","17":"build_request","18":"url","20":"params","22":"headers","28":"params_list","36":"u","41":"query","48":"new_query","66":"req"}}
import urllib.parse
import urllib.request


QueryParams = dict[str, str] | list[tuple[str, str]]
Headers = dict[str, str]


def build_request(
    url: str,
    *,
    params: QueryParams | None = None,
    headers: Headers | None = None
) -> urllib.request.Request:
    """
    Build a urllib Request, appending query parameters and attaching headers.
    """
    if params is not None:
        params_list = list(params.items()) if isinstance(params, dict) else params

        u = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qsl(u.query) + params_list
        new_query = urllib.parse.urlencode(query)
        url = urllib.parse.urlunsplit(
            (u.scheme, u.netloc, u.path, new_query, u.fragment)
        )

    req = urllib.request.Request(url, headers=headers or {})

    return req
```

I can pass `params` as a dict or as a list of `(key, value)` tuples; I start by converting it to the list form.
This means I can pass the same query parameter multiple times in a URL.
That's admittedly unusual, but I use it on a couple of my websites so I wanted to support it here.

I'm using the [`urllib.parse` module][urllib-parse] to manipulate the URL and append the query parameters.
I parse the initial URL with [`urlsplit`][urllib-parse-urlsplit], encode the query parameters, then reassemble the URL with [`urlunsplit`][urllib-parse-urlunsplit].
This preserves any existing query parameters and fragments, and returns a complete URL I can pass to the `Request` object.

(If, like me, you'd reach for the [`urlparse` function][urllib-parse-urlparse], you're showing your age -- one thing I learnt during this project is that [`urlparse`][urllib-parse-urlparse] is now obsolete, and [`urlsplit`][urllib-parse-urlsplit] is the replacement.)

This function only handles GET requests, which is all I need for my scripts -- but it wouldn't be difficult to extend it to handle POST requests or form data if the need arises.

This is a pure function, so it's easy to [test thoroughly][chives-test-build-request].

## Getting a web page or an API endpoint

In most cases, I just care about getting the response body from the remote server, not the headers or URL -- for example, if I'm fetching a web page or an API endpoint.
If I want something different in a single script, I'll eschew my wrapper and use `urllib.request` directly.

Here's my `fetch_url` wrapper:

```python {"names":{"1":"certifi","2":"ssl","3":"fetch_url","4":"url","6":"params","8":"headers","11":"req","18":"ssl_context","30":"resp","31":"data"}}
import certifi
import ssl


def fetch_url(
    url: str,
    *,
    params: QueryParams | None = None,
    headers: Headers | None = None
) -> bytes:
    """
    Fetch the contents of a URL and return the body of the response.
    """
    req = build_request(url, params=params, headers=headers)
    
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    with urllib.request.urlopen(req, context=ssl_context) as resp:
        data: bytes = resp.read()

    return data
```

The key function is [`urllib.request.urlopen`][urllib-parse-urlopen], which is what actually makes the HTTP request.
I'm passing it two parameters: a `Request` and an [`SSLContext`][ssl-sslcontext].

We build the `Request` using the `build_request` function.

The `SSLContext` tells `urllib.request` which HTTPS certificates it can trust, in this case by pointing to a "cafile" (Certificate Authority file) file provided by the [`certifi` library][certifi].
This file contains a list of trusted root certificates, and all valid HTTPS certificates should eventually point back to an entry in this list.

The `certifi` library is a lightweight wrapper around [Mozilla's list of trusted Root Certificates][mozilla-ca-certs].
It's not in the standard library because it's important to stay up to date with changes to the list, and you don't want those changes coupled to Python version releases.
Although this exercise is about reducing dependencies, I'm okay with `certifi` because it's tiny -- you can read the whole thing in less than five minutes.
I know what it's doing.

The `urlopen` function looks for a 200 OK status code, and throws an [`HTTPError`][urllib-error-httperror] if it gets an error response from the server.
I considered wrapping that in another type, but for now I'm just catching `HTTPError`.

This function doesn't set a timeout on HTTP requests.
That would be an issue in a lot of contexts, but I'm normally using this from a script I run manually.
If something gets stuck, I can stop the script and debug manually.

This function doesn't support streaming responses; it reads the whole thing into memory at once.
That's fine for web pages or API calls, but I wouldn't use this to download large files or videos.

There's a lot of stuff this function doesn't do, but it works well in all of my scripts, it has a friendly API, and it only has one third-party dependency.

## Downloading images with format-based file extensions

As I started using the `fetch_url` in my projects, I realised the one time I often care about response headers is when I'm downloading images.
I want the filename to have the appropriate filename extension -- `.jpg` for JPEGs, `.png` for PNGs, and so on.
Sometimes I can guess the file format from the URL, but sometimes I need to inspect the [`Content-Type` header][header-content-type].

I considered exposing the headers from `fetch_url`, but since I only need the headers for downloading images and that's a pretty common operation, I decided to make a `download_image` helper instead.

First, I wrote a helper function that picks a filename extension based on the `Content-Type` header:

```python {"names":{"1":"choose_filename_extension","2":"content_type","7":"content_type_mapping"}}
def choose_filename_extension(content_type: str | None) -> str:
    """
    Choose a filename extension for an image downloaded with the given
    Content-Type header.
    """
    if content_type is None:
        raise ValueError(
            "no Content-Type header, cannot determine image format"
        )

    content_type_mapping = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
    }

    try:
        return content_type_mapping[content_type]
    except KeyError:
        raise ValueError(f"unrecognised Content-Type header: {content_type}")
```

The mapping contains the four image formats I encounter in practice; it's easy for me to add more if I try to download a newer format someday.

Then I wrote a function that takes an image URL and an "out prefix" (an initial guess at the path), downloads the image and choose a new file extension, and returns the final path:

```python {"names":{"1":"pathlib","2":"Path","3":"download_image","4":"url","6":"out_prefix","8":"params","10":"headers","13":"req","20":"ssl_context","32":"resp","33":"image_data","37":"image_format","42":"out_path","53":"out_file"}}
from pathlib import Path


def download_image(
    url: str,
    out_prefix: Path,
    *,
    params: QueryParams | None = None,
    headers: Headers | None = None,
) -> Path:
    """
    Download an image from the given URL to the target path, and return
    the path of the downloaded file.

    Add the appropriate file extension, based on the image's Content-Type.

    Throws a FileExistsError if you try to overwrite an existing file.
    """
    req = build_request(url, params=params, headers=headers)

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    with urllib.request.urlopen(req, context=ssl_context) as resp:
        image_data: bytes = resp.read()

    image_format = choose_filename_extension(content_type=resp.headers["content-type"])

    out_path = out_prefix.with_suffix("." + image_format)
    out_path.parent.mkdir(exist_ok=True, parents=True)
    with open(out_path, "xb") as out_file:
        out_file.write(image_data)

    return out_path
```

The first half of this function is the same as `fetch_url`; the second half constructs the final path and writes the download image to disk.
I like this approach because it allows the caller to specify a meaningful directory and filename without worrying about the filename extension (which is important but not meaningful).

The function creates the output directory if it doesn't exist, for convenience.
Nothing grinds my gears like getting a `FileNotFoundError` when trying to write to a file in a folder that doesn't exist.
My text editor is smart enough to auto-create missing folders; I want my code to do the same.

I open the file in [`xb` mode ][open-modes] to avoid overwriting existing files -- if I try to write to an image I've already saved, I get a `FileExistsError`.
I find that a useful safety check, and I use exclusive creation mode in a lot of my scripts now.

## Packaging and testing

A few months ago, I created a personal utility library `chives` for dealing with [tiny archives][tiny-archives], and that was a good place to keep this code.

The HTTP code is in [`chives.fetch`][chives-fetch], and the accompanying tests are in [`test_fetch.py`][chives-test-fetch].
I'm testing it using the [vcrpy library][vcrpy], which knows how to record responses from `urllib.request`.

I now use this code across all my personal scripts, and it's been rock-solid.
There are lots of good reasons to use Python's more advanced HTTP libraries,  but they're for use cases I don't have.

[certifi]: https://github.com/certifi/python-certifi
[chives]: /projects/chives/
[chives-fetch]: /projects/chives/files/src/chives/fetch.py
[chives-test-build-request]: /projects/chives/files/tests/test_fetch.py#:~:text=build_request
[chives-test-fetch]: /projects/chives/files/tests/test_fetch.py
[header-content-type]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type
[httpx]: https://github.com/encode/httpx
[mozilla-ca-certs]: https://wiki.mozilla.org/CA/Included_Certificates
[open-modes]: https://docs.python.org/3/library/functions.html#open
[requests]: https://requests.readthedocs.io/en/latest/
[ssl-sslcontext]: https://docs.python.org/3/library/ssl.html#ssl.SSLContext
[tiny-archives]: /2024/static-websites/
[urllib3]: https://github.com/urllib3/urllib3
[urllib-error-httperror]: https://docs.python.org/3/library/urllib.error.html#urllib.error.HTTPError
[urllib-parse]: https://docs.python.org/3/library/urllib.parse.html
[urllib-parse-urlopen]: https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen
[urllib-parse-urlparse]: https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
[urllib-parse-urlsplit]: https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit
[urllib-parse-urlunsplit]: https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlunsplit
[urllib-request]: https://docs.python.org/3/library/urllib.request.html
[urllib-request-object]: https://docs.python.org/3/library/urllib.request.html#urllib.request.Request
[vcrpy]: /2025/testing-with-vcrpy/
