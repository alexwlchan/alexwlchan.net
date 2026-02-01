---
layout: topic
title: Go
date_updated: 2026-02-01 22:23:50 +00:00
topics: 
  - Computing
---
Go is a programming language designed at Google with a particular focus on concurrency.
Apps written in Go include [Docker][wiki-docker], [Kubernetes][wiki-kubernetes], and [Caddy][wiki-caddy] (the web server that runs this blog).

I started learning Go in summer 2025, when I started working at Tailscale (which uses Go for both the end-user client and back-end coordination server).

[wiki-caddy]: https://en.wikipedia.org/wiki/Caddy_(web_server)
[wiki-docker]: https://en.wikipedia.org/wiki/Docker_(software)
[wiki-kubernetes]: https://en.wikipedia.org/wiki/Kubernetes

{% from "partials/topic_entries.html" import subtopics, topic_entries %}
{{ subtopics(page) }}

Here’s everything I’ve posted about Go:

{{ topic_entries(page) }}
