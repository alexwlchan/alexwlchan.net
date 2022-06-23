---
layout: post
title: Creating an Alfred Workflow to open GitHub repos
summary: Automations for my automations.
tags: alfred github
link: https://github.com/alexwlchan/github_alfred_shortcuts
theme:
  image: /images/2022/alfred_workflow_screenshot_1x.png
index:
  tint_color: "#1d1d1d"
---

I've written a script which lets me build an [Alfred workflow] to open GitHub repositories quickly.
I type a few characters in the launcher, and it offers to open the repo:

<img src="/images/2022/alfred_search_1x.png" srcset="/images/2022/alfred_search_1x.png 1x, /images/2022/alfred_search_2x.png 2x" style="width: 694px;">

You don't need a custom workflow to do this -- Alfred already has built-in features for [web search] and [using bookmarks] -- but to set those up, you have to click around in the GUI.
At work, our code is scattered across a lot of different repositories, and I find it easier to manage with a script.

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

<img src="/images/2022/alfred_workflow_screenshot_1x.png" srcset="/images/2022/alfred_workflow_screenshot_1x.png 1x, /images/2022/alfred_workflow_screenshot_2x.png 2x">

The text-based config means I can add and remove repos very quickly.
I don't have a shortcut for every repo I use; just the ones in which I'm actively working.
I open GitHub dozens of times a day, and I use these shortcuts a similar amount.

I don't know how many people will want this exact shortcut, but there might be some ideas here you can reuse: in particular the multi-line values in a configparser file, and programatically creating an Alfred Workflow with Python.

[web search]: https://www.alfredapp.com/help/features/web-search/
[using bookmarks]: https://www.alfredapp.com/help/features/bookmarks/
[Alfred workflow]: https://www.alfredapp.com/workflows/
[configparser]: https://docs.python.org/3/library/configparser.html
[ms_strings]: https://stackoverflow.com/a/11866695/1558022
