---
layout: til
date: 2024-05-23 09:30:27 +01:00
title: How to simulate an `[Errno 54] Connection reset by peer` when using pytest
summary: |
  You can run a TCP server in the background using a fixture, and using the `SO_LINGER` socket option can reset the connection.
tags:
  - python
  - python:httpx
  - python:pytest
---
I was making some requests with httpx, and one of them failed with an exception:

```python
ConnectError("[Errno 54] Connection reset by peer")
```

This exception is thrown when httpx [fails to read data from the network](https://www.python-httpx.org/exceptions/).

I wanted to add some code to my library to retry this error, and I wanted a test that it was being retried correctly.
That meant I wanted a way to reliably reproduce the error in my test suite.

(I later discovered that httpx's exceptions are [very simple](https://github.com/encode/httpx/blob/37593c1952f4972040f6163da67e3777fd3d2e94/httpx/_exceptions.py#L74-L95) and would be easy to replicate.
I was expecting a more complex object, with attributes I could compare to `errno.ECONNRESET` or something -- but no, it looks like they just pass the string value along directly.)

I did some Googling and found a few useful pointers:

-   I found [an article by Asaf Mesika][Asaf] that explains you can simulate this connection by sending an RST command to the TCP socket.
    His sample code is in Java, but it gave me some useful stuff to search for.
-   Looking for socket stuff, I found a Stack Overflow answers by [tdelaney] and [crowbent] that translate this idea into Python.
-   I reread an article that runs a [TCP server in a background thread in pytest][threading].
    I can't remember when or why, but I know I've read it before and used it for something.

Here's the code I ended up writing:

```python
import socket
import struct
import threading

import pytest


class ConnectionResetServer:
    """
    This is a server which will cause all requests to fail with
    a "Connection reset by peer" error.
    """

    def __init__(self, port: int):
        self.port = port
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __enter__(self):
        self.sock.bind(("127.0.0.1", self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.sock.close()

    def listen_for_traffic(self):
        while True:
            self.sock.listen(1)

            connection, _ = self.sock.accept()

            # When we get a connection, we set some socket options that
            # will cause us to reset the connection.
            #
            # Quoting crowbent (https://stackoverflow.com/a/6440364/1558022):
            #
            #     Turn the SO_LINGER socket option on and set the linger time
            #     to 0 seconds. This will cause TCP to abort the connection
            #     when it is closed, flush the data and send a RST.
            #     See section 7.5 and example 15.21 in UNP.
            #
            linger_on_off = 1
            linger_time = 0

            connection.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_LINGER,
                struct.pack("ii", linger_on_off, linger_time),
            )
            connection.close()


@pytest.fixture
def connection_reset_server_url():
    """
    Fixture that returns the URL of the server that will reliably cause
    a "Connection reset by peer" error

    e.g. ``http://127.0.0.1:9500/``

    """
    port = 9500

    with ConnectionResetServer(port=port) as server:
        thread = threading.Thread(target=server.listen_for_traffic)
        thread.daemon = True
        thread.start()
        yield f"http://127.0.0.1:{port}/"


@pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")
def test_throws_connection_reset(connection_reset_server_url: str) -> None:
    import httpx

    with pytest.raises(httpx.ReadError) as err:
        httpx.get(connection_reset_server_url)

    assert err.value.args == ("[Errno 54] Connection reset by peer",)
```

It creates a TCP server that will reset all requests, and runs that as a background in my pytest fixture.
Then I connect to that URL, and I get a `ReadError` with the error message I was expecting.

This isn't quite what I was going for -- it's a `ReadError` instead of a `ConnectError` -- but it's a useful standalone piece.
I'm going to keep trying for a `ConnectError` for a bit longer, and I'll write that up as another TIL if I'm successful.

[Asaf]: https://medium.com/@asafmesika/simulating-connection-reset-by-peer-exception-in-unit-testing-using-java-7ceb2e5713b3
[tdelaney]: https://stackoverflow.com/a/40779258/1558022
[crowbent]: https://stackoverflow.com/a/6440364/1558022
[threading]: https://dev.to/ghost/pytest-with-background-thread-fixtures-3599
