---
layout: post
date: 2022-06-26 20:53:03 +00:00
title: Creating an Alfred Workflow to open GitHub repos
summary: Automations for my automations.
tags:
  - alfred
  - github
link: https://github.com/alexwlchan/github_alfred_shortcuts
colors:
  index_light: "#1c1c1c"
  index_dark:  "#898f93"
---

I've written a script which lets me build an [Alfred workflow] to open GitHub repositories quickly.
I type a few characters in the launcher, and it offers to open the repo:

{%
  picture
  filename="alfred_search.png"
  alt="A large search bar with the query 'dotorg', showing two results: a GitHub link to the wellcomecollection.org repo, and a local folder called 'dotorg'."
  width="694"
%}

You don't need a custom workflow to do this -- Alfred already has built-in features for [web search] and [using bookmarks] -- but to set those up, you have to click around in the GUI.
At work, our code is scattered across a lot of different repositories, and I find it easier to manage with a script.

This also allows me to get similar GitHub shortcuts at work and at home.
I can't use Alfred's [built-in preference syncing][sync] because I have no shared file sync between my personal and professional machines; I try to keep them isolated.
Defining these bookmarks in a workflow I can build separately on each Mac gets me consistent behaviour, wherever I'm working.

I define my repos in an ini-like config file:

```
[repos]
alexwlchan =
    docstore
    dominant_colours
    pathscripts

wellcomecollection  =
    wellcomecollection.org (dotorg)
    storage-service

scanamo =
    scanamo
```

This is slightly abusing the file format used by Python's [configparser] module; this is a series of key-value pairs in which [the values are multi-line strings][ms_strings] that get broken up within the script.

The Python script reads this config and builds a workflow package, which I can open in Alfred:

{%
  picture
  filename="alfred_workflow_screenshot.png"
  alt="Screenshot of an Alfred workflow. There are three inputs with a GitHub logo, linked to three 'Open URL' actions, all for github.com."
  width="565"
%}

The text-based config means I can add and remove repos very quickly.
I don't have a shortcut for every repo I use; just the ones in which I'm actively working.
I open GitHub dozens of times a day, and I use these shortcuts a similar amount.

I don't know how many other people will want this exact shortcut, but there might still be some ideas here you can reuse: in particular the multi-line values in a configparser file, and programatically creating an Alfred Workflow with Python.

[web search]: https://www.alfredapp.com/help/features/web-search/
[using bookmarks]: https://www.alfredapp.com/help/features/bookmarks/
[Alfred workflow]: https://www.alfredapp.com/workflows/
[sync]: https://www.alfredapp.com/help/advanced/sync/
[configparser]: https://docs.python.org/3/library/configparser.html
[ms_strings]: https://stackoverflow.com/a/11866695/1558022
