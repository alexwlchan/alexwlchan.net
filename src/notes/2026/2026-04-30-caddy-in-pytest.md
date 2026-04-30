---
layout: note
date: 2026-04-30 09:04:38 +01:00
title: Start a Caddy server in a subprocess during a Python session
summary: Start the server with `subprocess.Popen`, poll until it's available, yield the base URL, then clean up the process when you're done.
topics:
  - Python
  - Caddy
  - Software testing
---
For local developemnt and testing of this site, I've started to run a Caddy server with my real config to be a better replica of my real setup.
I wanted to start a Caddy server in my automated tests, and shut it down when I'm done.

Here's the fixture I came up with:

```python {"names":{"1":"collections","2":"abc","3":"Iterator","4":"subprocess","5":"subprocess","6":"PIPE","7":"time","8":"urllib","9":"error","10":"urllib","11":"request","12":"pytest","16":"caddy_server_url","19":"port","20":"cmd","29":"proc","30":"url","32":"t0","48":"exc"}}
from collections.abc import Iterator
import subprocess
from subprocess import PIPE
import time
import urllib.error
import urllib.request

import pytest


@pytest.fixture(scope="session")
def caddy_server_url() -> Iterator[str]:
    """
    Start an instance of Caddy running in the current directory, and
    return the base URL.
    """
    port = 5858
    cmd = ["caddy", "file-server", "--listen", f":{port}"]

    with subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE) as proc:
        url = f"http://localhost:{port}/"

        # Wait for up to a second waiting for the server to start.
        #
        # If we get a ConnectionRefusedError, the server hasn't started yet.
        # If we get an HTTPError or a 200 OK, we've connected to the server
        # and it's serving HTTP traffic, so it's started.
        t0 = time.time()
        while time.time() - t0 < 1:
            try:
                urllib.request.urlopen(url)
            except urllib.error.HTTPError:
                break
            except urllib.error.URLError as exc:
                if exc.args and isinstance(exc.args[0], ConnectionRefusedError):
                    pass
                else:
                    raise
            else:
                break

        assert not proc.poll()

        yield url

        proc.terminate()
        proc.wait(timeout=1)
```

And here's what a test looks like:

```python {"names":{"1":"test_can_start_web_server","2":"caddy_server_url","4":"resp"}}
def test_can_start_web_server(caddy_server_url: str) -> None:
    """
    Fetch a page from the running web server.
    """
    resp = urllib.request.urlopen(caddy_server_url + "example.py")
    assert b"test_can_start_web_server" in resp.read()
```

The fixture starts a file server with `subprocess`, then polls until the server is available.
On my Mac mini, Caddy takes ~0.01s to start -- long enough I can't start running tests immediately, fast enough that any fixed sleep would be inefficient (especially as it'll be slower in CI).

At the end of the fixture, I call `proc.terminate()` and `proc.wait()` to clean everything up.
The `terminate()` sends a SIGTERM; the `wait()` blocks until the child process terminates.
The process shuts down quickly, but I do need to wait or I get warnings from pytest that I have an unterminated process.

The fixture is session-scoped so I only have to start/stop the server once across my test suite.

In my real codebase, this code is split across two functions -- a function that starts the server, and a function that wraps it in a pytest fixture.
I reuse the server function in my `serve_site.py` script, which runs a local development server for the site.
I'm also pointing it at a `Caddyfile` with my site config, rather than running a bare `file_server`.

This is similar to [Simon Willison's recipe][simonwillison-server].

[simonwillison-server]: https://til.simonwillison.net/pytest/subprocess-server
