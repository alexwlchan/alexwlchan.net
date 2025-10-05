---
layout: til
title: |
    The "MCP" in Archivematica stands for "Master Control Program"
summary: It's nothing to do with generative AI.
date: 2025-09-22 09:28:04 +0100
tags:
  - digital preservation
  - archivematica
  - naming things
---
The acronym "MCP" has been used a lot recently in the context of Large Language Models.
It stands for ["Model Context Protocol"][mcp_ai], and it's a way for generative AI to communicate with external systems.
For example, you could run an MCP Server for Spotify, and then an MCP Client running in an AI chatbot could control your music.

I've heard that acronym before!

The phrases "MCP server" and "MCP client" also appear in [Archivematica], an open-source digital preservation tool I used while I worked at Wellcome Collection.
We used Archivematica to process born-digital files before adding them to our permanent storage repository.

The MCP server and client in Archivematica are nothing to do with AI.
Instead, they handle a series of "microservices" that run inside the application.
(Microservices -- another term that later became popular with a completely different meaning.)
In Archivematica, each microservice ran a different preservation task -- like identifying file formats, scanning for viruses, or adding checksums.
The MCP server would orchestrate the tasks, and the clients would run them.

I'd forgotten what MCP stood for in the context of Archivematica, and I found it again in some [Archivematica source code][src]:

> MCPServer (Master Control Program Server) determines the jobs/tasks/microservices
> run by Archivematica and arranges for their execution.

Unlike the [1982 sci-fi antagonist of the same name][tron], Archivematica has never turned evil or tried to take over the world.
Let's hope it stays that way.

[mcp_ai]: https://www.anthropic.com/news/model-context-protocol
[Archivematica]: https://archivematica.org/en/
[src]: https://github.com/artefactual/archivematica/blob/8df5aeeadcdd23b58946b36df45b11de75b60267/src/archivematica/MCPServer/server/__init__.py#L2-L3
[tron]: https://en.wikipedia.org/wiki/List_of_Tron_characters#Master_Control_Program
