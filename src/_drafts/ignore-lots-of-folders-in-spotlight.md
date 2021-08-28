---
layout: post
title: Programatically ignoring lots of folders in Spotlight
summary: A script that allows me to ignore folders like "target" and "node_modules", so they don't appear in search results.
tags: macos python
---

I was searching my Mac today, and my search results were cluttered with files from various `node_modules` folders:

<img src="/images/2021/cluttered_search_results_2x.png" srcset="/images/2021/cluttered_search_results_2x.png 2x, /images/2021/cluttered_search_results_2x.png 1x" style="width: 714px;" alt="Screenshot of a search tool for the word 'inspect'. It shows a list of nine results, each with a path under it that goes to a subpath of a node_modules folder.">

This makes sense -- I've been working on several Node projects recently, and the `node_modules` folder is a cache of external dependencies downloaded from npm.
It contains all the third-party code used in those projects, and that's a lot of files.
It's unsurprising that some of them would look like the files I'm actually looking for.

It's also very annoying.
Most of the time, I want to search the code that I've written, not the third-party code I happen to be using.
I pretty much never want to see these files in a global file search.

On the Mac, file search is powered by [Spotlight][spotlight].
You can either search in Spotlight directly, or other apps can use the Spotlight search index.
(That's what you see in the screenshot -- I'm using an app called Alfred rather than Spotlight, but Alfred is [using the Spotlight index][index] to get a list of files.)

I can [exclude a file or folder from Spotlight][exclude] by adding it to a list in System Preferences, but it's a manual process that needs me to click around.
I have dozens of `node_modules` folders I want to ignore -- is there a faster way to get them out of search results?

(The projects use a microservices pattern: they're collections of small apps that work together.
Each app has its own `node_modules` folder I want to ignore.)

I found a blog post that explains how to [programmatically add Spotlight exclusions][programmatically].
The Spotlight configuration is kept in a [plist file][plist], and the post explains several shell commands using [`plutil`][plutil] which add the config to exclude a folder.

I've wrapped these commands in a Python script that looks for every folder called `node_modules`, and excludes it from Spotlight.
It also looks for folders called `target`, which is the output folder used by the Rust and Scala compilers.

How it works:

-   Make a backup of the Spotlight config file
-   Walk a directory tree, looking for folders named `node_modules` or `target`
-   Add any matching folders to the list of exclusions in the Spotlight config file using `plutil`
-   Restart Spotlight to pick up the updated list of exclusions

You need to run as the root user or using `sudo`, because regular users can't modify the Spotlight configuration file directly.

If you'd find this useful, you can download the script:

{% download /files/2021/ignore_folders_in_spotlight.py %}

[spotlight]: https://support.apple.com/en-gb/guide/mac-help/mchlp1008/mac
[index]: https://www.alfredapp.com/help/troubleshooting/indexing/spotlight/
[exclude]: https://support.apple.com/en-gb/guide/mac-help/mchlp2811/11.0/mac/11.0
[programmatically]: https://blog.christovic.com/2021/02/programatically-adding-spotlight.html
[plist]: https://en.wikipedia.org/wiki/Property_list
[plutil]: https://www.youtube.com/watch?t=5s&v=e1QAw18lpUE
