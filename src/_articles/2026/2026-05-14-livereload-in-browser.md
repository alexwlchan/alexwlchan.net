---
layout: article
date: 2026-05-14 08:51:01 +01:00
date_updated: 2026-05-17 13:51:11 +01:00
title: Waiting for website changes in the browser
summary: I'm using HTTP long polling and Python's threading module to tell my browser when my site has finished rebuilding. This gives me near-instant reloading, with no third-party dependencies.
topics:
  - Computers and code
  - Blogging about blogging
colours:
  css_light: "#8b7434"
  css_dark:  "#dfcf96"
---
{#
  Sharing image from Pexels: https://www.pexels.com/photo/colorful-threads-on-white-background-15415991/
#}

In my [previous post][me-fsevents], I explained how I use the FSEvents API to detect changed files on macOS.
It's part of my livereload mechanism for working on this site.
I make a change to a source file, that triggers a rebuild of the site, and then the development site automatically refreshes in my web browser.
I'm trying to build this all myself, with no third-party dependencies.

Once I've detected a changed file and rebuilt the site, how do I automatically refresh my open browser windows?
In this post, I'll explain how I use HTTP long polling to tell pages when it's time to reload.

{% table_of_contents %}

## HTTP long polling

### Faster isn't always better

In most HTTP servers I've built, when the server sends a response to a client, I want it to return as quickly as possible.
When I'm writing HTTP clients that fetch data from servers, I expect the server to respond quickly.
The entire interaction happens within a few seconds of the request -- but it doesn't have to be that way.

HTTP [long polling][wiki-long-polling] is a technique where a client makes a normal HTTP request, but the server doesn't respond immediately.
Rather than closing or timing out the connection, both sides hold it open, and the server can send more data to the client over time.

This mechanism can allow the server to tell the browser when it's time to reload the page.
When the browser loads a page, it opens a long-lived HTTP connection to the server.
The server only sends data when something has changed, so the browser waits to receive data and then reloads the page.

This technique is used in Tailscale -- clients use HTTP long polling to get network updates from the control plane.
When the `tailscaled` daemon starts, it opens a long-running connection to the control servers, and when something changes in the network, the servers send the updated network information (or "netmap") down that connection.
Clients can hold open a connection for a long time, and receive many updates on the same connection.

### Sending reload events from a Python web server

All the scripts for my blog are written in Python, so I want to use Python to write a web server that serves a long-lived connection and tells the browser when to reload.
For production Python web servers I'd use a proper server framework like [Gunicorn][pypi-gunicorn] or [uWSGI][pypi-uwsgi], but for a small and low-traffic local server, I can just use the standard library's [`http.server` module][pydoc-http-server].

To create a server, I need to create a subclass of [`BaseHTTPRequestHandler`][pydoc-http-server-BaseHTTPRequestHandler] that handles GET requests, then pass that to an instance of [`HTTPServer`][pydoc-http-server-HTTPServer].

Here's a server that receives a GET request, holds open the connection, and writes "waiting..." once every second:

```python {"names":{"1":"http","2":"server","3":"HTTPServer","4":"BaseHTTPRequestHandler","5":"time","6":"SlowHandler","8":"do_GET","21":"server_address","22":"server"}}
from http.server import HTTPServer, BaseHTTPRequestHandler
import time


class SlowHandler(BaseHTTPRequestHandler):
    """
    An HTTP handler that sends "waiting..." once a second on
    a long-running connection.
    """

    def do_GET(self) -> None:
        """
        Handle a new GET request from a client.
        """
        print("Client connected")
        
        # Send the initial HTTP headers.
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        try:
            while True:
                self.wfile.write(b"waiting...\n")
                
                # Flush to stdout to ensure the client receives the data
                # immediately, without buffering.
                self.wfile.flush()
                
                # Sleep until we're ready to write again.
                time.sleep(1)
              
        # If the client closes the connection, we'll get a BrokenPipeError
        # the next time we try to write data.
        except BrokenPipeError:
            print("Client disconnected")


server_address = ("localhost", 5555)
server = HTTPServer(server_address, SlowHandler)
server.serve_forever()
```

If you run this script and make a GET request with curl, you'll see "waiting..." printed in a loop:

```console
$ curl http://localhost:5555/
waiting...
waiting...
waiting...
```

We could wire this up to check if there have been any changes in the last second, and write a different message to the connection -- but that would introduce at least a second of latency into the browser getting updates.
Ideally, we'd send a response as soon as an update is ready.
How can we coordinate that within a single Python script?

The solution is another standard library feature I've not used before: [`threading.Event`][pydoc-threading-Event].
This allows us to track the value of a single true/false flag, and we can use [the `wait()` method][pydoc-threading-Event-wait] to block until the flag is set to true.

First I create the event:

```python {"names":{"1":"threading","2":"rebuild_event"}}
import threading

rebuild_event = threading.Event()
```

When the site is finished rebuilding, we set the flag to true, then clear it immediately (waiting for the next rebuild):

```python {"names":{"1":"changeset"}}
for changeset in watch_for_changed_files():
    rebuild_site(based_on=changeset)
    rebuild_event.set()
    rebuild_event.clear()
```

Then in the HTTP handler, we wait for the flag to be set and only then send a response:

```python {"names":{"1":"WaitForChangesHandler","3":"do_GET"}}
class WaitForChangesHandler(BaseHTTPRequestHandler):
    """
    An HTTP handler that waits until the site is rebuilt to send a response.
    """

    def do_GET(self) -> None:
        """
        Handle a new GET request from a browser.
        """
        print("Client connected")
        
        try:
            rebuild_event.wait()

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            self.wfile.write(b"reload\n")
            self.wfile.flush()
        except BrokenPipeError:
            print("Client disconnected")
```

We can also use `threading` to start the server in a background thread, and wait for file changes in the main thread:

```python {"names":{"1":"server_address","2":"server","13":"changeset"}}
server_address = ("localhost", 5555)
server = HTTPServer(server_address, WaitForChangesHandler)

threading.Thread(target=server.serve_forever, daemon=True).start()

for changeset in watch_for_changed_files():
    rebuild_site(based_on=changeset)
    rebuild_event.set()
    rebuild_event.clear()
```

When we make an HTTP call to the web server, it now waits until something changes, and only then sends a response:

```console
$ curl http://localhost:5555/
time to reload
```

This minimises the delay between rebuilding the site and refreshing the page, which allows for very fast reloads when I change a source file.

### Waiting for a long-polling server in JavaScript

We can use the [built-in `fetch()` method][mdn-fetch] to make a request to the server, wait for a response, and then trigger a page reload.
This only requires a few lines of JavaScript:

```javascript {"names":{"1":"waitForChanges"}}
async function waitForChanges() {
  await fetch('http://localhost:5555/wait-for-changes');
  window.location.reload();
}

window.addEventListener("DOMContentLoaded", waitForChanges);
```

This is only added to local builds, so the live site won't fetch `localhost:5555` on your computer.

If the livereload server is different to the server that's serving this JavaScript, we need to tweak the [`Access-Control-Allow-Origin` header][mdn-acao-header] to allow the page to talk to the livereload server:

```python
self.send_response(200)
self.send_header("Access-Control-Allow-Origin", "*")
self.send_header("Content-type", "text/plain")
self.end_headers()
```

For a live application we'd want to scope this more tightly than `*`, but for a server that's only used for local development it's fine.

## Making this code more robust

### Using threading to support multiple connections

The basic `HTTPServer` can only handle one connection at a time, so if I have two browser windows open, only one of them can receive the reload event.
This is sub-optimal -- when something changes, every browser window should reload.

We can fix this by replacing `HTTPServer` with [`ThreadingHTTPServer`][pydoc-http-server-ThreadingHTTPServer], which creates a new thread for every request:

```python {"names":{"1":"http","2":"server","3":"ThreadingHTTPServer","4":"server_address","5":"server"}}
from http.server import ThreadingHTTPServer

server_address = ("localhost", 5555)
server = ThreadingHTTPServer(server_address, WaitForChangesHandler)

threading.Thread(target=server.serve_forever, daemon=True).start()
```

I'm not sure how this scales for a very large number of long-running requests, but I'll only ever have a small, single-digit number of browser windows open, and it's plenty for that.

### Avoiding default `fetch()` timeouts

Although we don't set an explicit timeout in our `fetch()` call, browsers apply their own default timeout.
For example, a quick search suggests Firefox used to set a 30 second timeout (I couldn't immediately find a reference about whether that's still true).
If the server doesn't respond in that time, the connection is closed and no more data is received.

That means that if I go longer than the default timeout without making changes, the browser will close the connection to the livereload server, and then it won't be notified about further changes.

We can fix this by changing the server so it always responds within 20 seconds (or another timeout of our choice).
It sends a 200 OK immediately if there's a change, or a 204 No Content if it hits the timeout before a change happens.
Then the on-page JavaScript can run in a loop, and only reload when it gets a 200 OK.

We can pass a `timeout` parameter to `rebuild_event.wait()`, which blocks until the flag is set or the timeout expires, and returns the current value of the flag.
Here's the updated server:

```python {"names":{"1":"WaitForChangesHandler","3":"do_GET","4":"has_changes"}}
class WaitForChangesHandler(BaseHTTPRequestHandler):
    """
    An HTTP handler that sends one of two responses:
    
    *   200 OK -- the site has changed, reload the page, or
    *   204 No Content -- nothing has changed recently, make a new GET request
    
    """

    def do_GET(self) -> None:
        """
        Handle a new GET request from a browser.
        """                
        try:
            has_changes = rebuild_event.wait(timeout=20)
            
            if has_changes:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                self.wfile.write(b"reload\n")
                self.wfile.flush()
            else:
                self.send_response(204)
                self.end_headers()
        except BrokenPipeError:
            pass
```

Then in the JavaScript, we make requests in a loop, check the status code of each response, and only reload if we get a 200 OK:

```javascript {"names":{"1":"waitForChanges","2":"response"}}
async function waitForChanges() {
  while (true) {
    const response = await fetch('http://localhost:5555/wait-for-changes');

    if (response.status === 200) {
      window.location.reload();
      break;
    }
  }
}
```

If the `fetch()` call fails -- for example, if the server gets restarted -- the loop will break, and then the window will stop receiving updates.
We can fix this by wrapping the body of the loop with a `try … except`, and in the `except` we tell the function to wait a second before trying again:

```javascript {"names":{"1":"waitForChanges","2":"response"}}
async function waitForChanges() {
  while (true) {
    try {
      const response = await fetch('http://localhost:5555/wait-for-changes');

      if (response.status === 200) {
        window.location.reload();
        break;
      }
    } catch {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
}
```

This is the code I've been using for several weeks now, and it's held up well.

## Rejected approaches

**Using third-party libraries.**
Initially I was using the [python-livereload library][gh-python-livereload], which bundles a copy of [livereload-js][gh-livereload-js], but I wanted to write my own implementation -- partly to avoid dependencies, partly to understand how it works.

**Polling the client.**
I could write a timestamp to a file at the end of a build, serve that file as part of the site, and have JavaScript on the page continuously poll that file for changes.
I prefer waiting for changes, because it avoids unnecessary work and CPU cycles.

**Manipulate the browser directly.**
The server and my web browser are almost always on the same machine.
Rather than have the browser trigger the reload, the rebuild script could use something like AppleScript to find matching browser windows and trigger a reload.

That would be the ultimate "only has to work on my machine" solution, but it might be more complicated, because I'd have to write new code for every browser I use.
(I routinely test with Safari, Firefox, and Chrome.)
It also wouldn't work if I'm using a web browser on a different machine, for example when I'm testing how the site looks on a phone.

**Use [WebSockets][mdn-websockets] to tell the web page about changes.**
That's how [livereload-js][gh-livereload-js] works, and WebSockets are a good tool for creating a persistent connection between a server and a client.
They're capable of two-way communication -- for example, Slack uses WebSockets to maintain a connection between the Slack app and their servers.

I didn't use WebSockets because they're more complicated to implement on the server (there's no WebSockets server in the Python standard library), and I don't need their flexibility.
My server--browser communication is strictly one-way, so HTTP long polling is fine.

{% update date="2026-05-17" %}
  Dion Williams [pointed out][mastodon-dion-williams] that my long polling pattern is so common, it's been formalised as a standard:

  {% mastodon "https://toot.wales/@dionrhys/116574251642161508" %}

  I'm not going to rewrite my code to use `EventSource` given my current code works fine and I only have a single type of message, but it's cool to know this pattern exists and is something I could use in a larger project.
  
  [mastodon-dion-williams]: https://toot.wales/@dionrhys/116574251642161508
{% endupdate %}

## The result

Here's a diagram which illustrates the code we've written: when the site is rebuilt, we call `rebuild_event.set()`, which unblocks a `rebuild_event.wait()` in the web server.
The web server sends an HTTP 200 OK to the web browser, which has been waiting for a response to `GET /wait-for-changes`.
The browser reloads the page, and the cycle starts again.
(Click for a larger version.)

<figure>
  {%
    inline_svg
    filename="livereload-in-browser.svg"
    link_to="original"
    class="dark_aware"
    style="width: 600px;"
  %}
</figure>

Here's the final Python web server:

```python {"names":{"1":"http","2":"server","3":"BaseHTTPRequestHandler","4":"ThreadingHTTPServer","5":"threading","6":"rebuild_event","9":"WaitForChangesHandler","11":"do_GET","12":"has_changes","29":"server_address","30":"server","41":"changeset"}}
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading


rebuild_event = threading.Event()


class WaitForChangesHandler(BaseHTTPRequestHandler):
    """
    An HTTP handler that sends one of two responses:
    
    *   200 OK -- the site has changed, reload the page, or
    *   204 No Content -- nothing has changed recently, make a new GET request
    
    """

    def do_GET(self) -> None:
        """
        Handle a new GET request from a browser.
        """                
        try:
            has_changes = rebuild_event.wait(timeout=20)
            
            if has_changes:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")            
                self.send_header("Content-type", "text/plain")
                self.end_headers()

                self.wfile.write(b"reload\n")
                self.wfile.flush()
            else:
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")            
                self.end_headers()
        except BrokenPipeError:
            pass


server_address = ("localhost", 5555)
server = ThreadingHTTPServer(server_address, WaitForChangesHandler)

threading.Thread(target=server.serve_forever, daemon=True).start()

for changeset in watch_for_changed_files():
    rebuild_site(based_on=changeset)
    rebuild_event.set()
    rebuild_event.clear()
```

and here's the JavaScript that gets embedded in the page:

```javascript {"names":{"1":"waitForChanges","2":"response"}}
async function waitForChanges() {
  while (true) {
    try {
      const response = await fetch('http://localhost:5555/wait-for-changes');

      if (response.status === 200) {
        window.location.reload();
        break;
      }
    } catch {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
}

window.addEventListener("DOMContentLoaded", waitForChanges);
```

Combined with the previous post, whenever I make a change to a source file, the effect is reflected near-instantly in my web browser.
Informal benchmarking shows there's only about 150 milliseconds between saving a file in my text editor and my browser reloading with the changes, which is on par with the fastest human reaction times.

This makes working on the site feel incredibly smooth.
As I'm working on complex layouts or editing a tricky sentence, I can save my work and see the changes.
The rendered site looks different to monospaced code in my text editor, and I often spot new mistakes or issues that way.

For a long time I'd have reached for a third-party library to do this, and it's pretty satisfying to have written my own.
The whole thing is only 150 lines of code, and I understand exactly what it's doing.

[gh-livereload-js]: https://github.com/livereload/livereload-js
[gh-python-livereload]: https://github.com/lepture/python-livereload
[mdn-acao-header]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Origin
[mdn-fetch]: https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch
[mdn-websockets]: https://developer.mozilla.org/en-US/docs/Glossary/WebSockets
[me-fsevents]: /2026/watch-files-on-macos/
[pydoc-http-server]: https://docs.python.org/3/library/http.server.html
[pydoc-http-server-BaseHTTPRequestHandler]: https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler
[pydoc-http-server-HTTPServer]: https://docs.python.org/3/library/http.server.html#http.server.HTTPServer
[pydoc-http-server-ThreadingHTTPServer]: https://docs.python.org/3/library/http.server.html#http.server.ThreadingHTTPServer
[pydoc-threading-Event]: https://docs.python.org/3/library/threading.html#threading.Event
[pydoc-threading-Event-wait]: https://docs.python.org/3/library/threading.html#threading.Event.wait
[pypi-gunicorn]: https://gunicorn.org/
[pypi-uwsgi]: https://uwsgi-docs.readthedocs.io/en/latest/
[wiki-long-polling]: https://en.wikipedia.org/wiki/Push_technology#Long_polling
