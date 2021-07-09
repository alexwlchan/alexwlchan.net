---
layout: post
date: 2021-07-09 06:27:58 +0000
title: A few useful GitHub searches
summary:
tags: github
---

For good and for ill, GitHub dominates the open source world.
A huge amount of open source code is available there, even if it's only a mirror or a fork of a project that's primarily maintained elsewhere -- and that makes it available to GitHub search.

I use GitHub search multiple times a day, and I find it an invaluable tool.
I have a couple of shortcuts set up [in Alfred](https://www.alfredapp.com) so I can search even faster:

<img src="/images/2021/alfred_github_search.png" style="width: 595px;" alt="A search box with the query 'gh ExpressionAttributeValues' and a single result highlighted in red: 'Search GitHub for ExpressionAttributeValues'.">

I set up these shortcuts with Alfred's [web search features](https://www.alfredapp.com/help/features/web-search/); any good launcher should be able to set up similar shortcuts if you'd find that convenient.
Setting up the shortcut isn't really the point of this post; how I search GitHub is.

These are a couple of searches I find especially useful:

-   Search GitHub for code: <https://github.com/search?type=Code&q={query}> (shortcut "gh")

    I often find examples more useful than library documentation.
    Seeing how somebody else is using a particular method or class can help me understand how to use it myself, and GitHub usually has plenty of examples.

    Even if there are no matches, that can be a clue -- if I'm using a popular library and there's nobody using it the same way as me, maybe I'm doing something wrong.
    It's a prompt to double-check what I'm doing, and check I'm really taking the best approach.

-   Search GitHub repositories: <https://github.com/search?q={query}> (shortcut "ghr")

    I have shortcuts set up for the repositories I use at most often, but sometimes I want to look at a different repo -- say, the code for a library I'm using.
    This search is the first step to finding that repo, and then doing a search within that repo for useful information.

-   Search code in a GitHub organisation: <https://github.com/search?type=Code&q=org:wellcomecollection+{query}> (shortcut "ghw")

    GitHub search has a bunch of [advanced options](https://github.com/search/advanced); restricting my search to a single organisation (where I work) is a particularly convenient one.
    I can find uses of a shared class or function across our different repos without finding similarly-named-but-unrelated code from the rest of the world.

    I often use this if I'm doing some sort of refactor.
    If I'm changing from one approach to the other, I can find every use of the old approach and upgrade it in one go, rather than having a prolonged period where we run both approaches in parallel.

GitHub code search is far from perfect, but it's good enough to be useful and it's helped me out a bunch of times.
It's hard to imagine going back to a time where I don't have a large corpus of similar code to search when I get stuck on something tricky.
