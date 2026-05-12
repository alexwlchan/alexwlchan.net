---
layout: article
date: 2026-05-12 07:25:36 +01:00
title: Watching for file changes in my browser
topics:
  - Computers and code
  - Blogging about blogging
colours:
  css_light: "#8b7434"
  css_dark:  "#dfcf96"
---
{#
  Sharing image from Pixabay: https://pixabay.com/illustrations/domino-game-set-plate-strategy-9602003/
#}

in previous post, explained how I use FSEvents API to detect file changes on macOS
part of livereload mechanism for local dev on this blog
I make a change to soruce fiels,detected by FSEvents, site rebuilt, and then trigger refrehs of all open browser windows
i'm trying to build this all myself, with no third-party deps required

suppose the site has been rebuilt
in this post i'll explain how i run a small server that serves a long-running http connection, and how i detect in browser to trigger automatic reloads
http long polling to trigger an automatic reload in my browser

## http long polling

### what is http long polling?

on most http servers i've worked on, when the http server serves a response, i want it to return as quickly as possible
when i'm writing http clients that fetch from servers, i expect the server to return in a timely fashion, or for the connection to time out
… but it doesn't have to be that way

http long polling is a technique where a client makes an http request as noral, but the server doesn't have to respond immediately
rather than closing or timing out the connection, both sides hold it open, until the server sends an http response with new data to the client
we can use this to trigger a reload -- open a long-running http connection when the page loads, then the server doesn't send a response until it's time to reload the page

i thought of this idea because we use it very heavily at tailscale
tailscale clients use http long polling to get netmap updates from the control plane
specifically, the tailscaled daemon opens a long-running connection with the control plane servers, and when something changes in the network, the control plane sends the updated network information (or "netmap") through that connection

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