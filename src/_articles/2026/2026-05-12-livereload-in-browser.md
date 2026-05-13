---
layout: article
date: 2026-05-12 07:25:36 +01:00
title: Waiting for website changes in my browser
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
I make a change to a source file, it's detected by FSEvents, that triggers of rebuild the site, and then the development site automatically refreshes in my web browser.
I'm trying to build this all myself, with no third-party dependencies.

Once we've detected a changed file and rebuild the site, how do we automatically refresh my open browser windows?
In this post, I'll explain how I use HTTP long polling to tell pages when it's time to reload.

[me-fsevents]: /2026/watch-files-on-macos/

## HTTP long polling

### What is long polling?

In most HTTP servers I've built, when the server sends a response to a client, I want it to return as quickly as possible.
When I'm writing HTTP clients that fetch data from servers, I expect the server to respond quickly.
The entire interaction is handled in the initial response -- but it doesn't have to be that way.

HTTP long polling is a technique where a client makes a normal HTTP request, but the server doesn't respond immediately.
Rather than closing or timing out the connection, both sides hold it open, and the server can send new data to the client over time.

We can use this to trigger a reload -- open a long-lived HTTP connection from the browser when the page reloads, then the server doesn't send a response until something's changed.
When the browser receives data, it knows it's time to reload the page.

I thought of this idea because HTTP polling is a core mechanic at Tailscale.
Specifically, Tailscale clients use HTTP long polling to get network updates from the control plane.
The `tailscaled` opens a long-running connection to the control plane servers, and when something changes in the network, the control plane sends the updated network information (or "netmap") down that connection.
Clients can hold open the connection for a long time, and receive many updates on the same connection.

### making a long-polling server in python

here's a basic python web server that writes to the connection every 1 second:

[[code]]

curl http://localhost:123

we could wire this to check if there are any changes since the last write, and if so, write a different message to the response -- but now back to polling, and introduced a 1s latency into browser getting updates
we really want to send response as soon as update ready
how to coordinate wthin python process?

threading event!
tracks a single true/false flag, can block until flag is true

create event:

[[code]]

set to true after rebuild, then reset:

[[code]]

wait for flag to be true, then send response:

[[code]]

curl http://localhost:123

this minimises latency in the http response, allows for very fast reloads

### waiting for a long-polling server in javascript

can use built-in `fetch()` to make request to server, wait for 200 OK response, trigger page reload:

[[code]]

if livereload server is on different server to main pages, need to tweak ACAO headers in python to allow cross-origin requests:

[[code]]

## making this code more robust

### threading in the server

default http sevrer is single-threaded, can only handle one req at a time
two browser windows => oh no, one will get stuck, only one receives each reload event

better: wrap in threadingserver

### avoiding default fetch timeouts

browsers enforce a default timeout on fetch(),
e.g. chrome is 5 mins
if server doesn't respond in that time, connection is closed

change server so it responds within 30 seconds and closes conn with 204 No Content if no changes:

[[code]]

then replace the client with a while true loop that ignores 204 responses:

[[code]]

so reset timeout every 30 seconds, avoid hitting browser timeouts

considered trying to set custom timeout of "forever", but wasn't obvious how to do that and is swimming against the tide
browsers clearly don't want you doing that + even if you can set it today, might break tomorrow

### allow disabling reload on a per-page basis

occasionally useful to disable livereload on a page
e.g. debug mode for code

[[screenshot]]

fortunately v simple:

[[code]]

## rejected approaches

use a third-party lib
-> not the point of this exercise

client polling
e.g. store timestamp in disk at end of build, poll file, wait for change
-> similar concerns about power usage and disk longevity

manipulate browser directly
-> e.g. with AppleScript, walk tabs
-> mostly safari, occasionally test compat in firefox and chrome
-> need new code for every browser

websockets
-> used for two-way comms (e.g. Slack)
-> more complicated to implement
-> would need a third-party dep

## the result

here's the final python server:

[[python server]]

and here's the javascript i embed in page:

[[javascript]]

## closing thoughts

site builder      threading.event     http server     web browser
                        <------------wait for true
                                        <-------------- wait for response

  build completes  ---> event = true
                          ----------> unblock wait()
                              -++
                                |
            event = false <-----+
                                          --------------> send 200 OK
                                                          reload page
                                      <------------------ wait for response

combined with previous post, effect is near-instant reflection of changes in browser 
(informal timing shows there's about 150 milliseconds between saving a file in my text editor + browser reloading in the changes, which is on par with fastest human reaction times)

makes working on the site feel smooth
can work on complex layouts or templates, or edit a tricky sentence -- site looks different to monospaced code of text editor, often spot new mistakes or issues that way

long time this sort of thing seemed insurmountable, too complicated for me
now i understand all the moving peices