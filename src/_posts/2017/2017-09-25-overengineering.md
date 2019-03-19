---
layout: post
title: What happens when you overengineer a static site?
link: https://github.com/alexwlchan/alexwlchan.net
tags: jekyll
date: 2017-10-03 22:23:38 +0100
summary: I switched back to Jekyll, and posted all the source code for my blog on GitHub.
category: Blogging with Jekyll
---

When I started this site, I was using Jekyll (well, Octopress).
Frequent issues with maintaining a working Ruby installation caused me to look elsewhere for a Python solution.
For a while, I used Pelican, but licensing issues and a sense that the project had been abandoned by maintainers led me to write my own static site generator (SSG).
Recently, I've come full circle and returned to Jekyll.

Writing my own SSG was a fun exercise, but a bit of a time sink.
So I started thinking about switching back to something I didn't have to maintain myself – and the two popular choices seem to be Jekyll or Hugo.

Today, I'm very happy using Docker, which can handle the problems of keeping a working Ruby install.
Jekyll has an edge on longevity, and the plug-in architecture offers lots of room for customisation.
As far as I know, Hugo doesn't have plug-in support – I've built up some pretty esoteric features on this site, so customisation is a must-have.

With the newest rewrite, I wanted to treat this like a proper software project.
Builds in Docker, continuous testing in CI, and automated deployments.
It took more work, but it means I don't just have a pile of hacked-together scripts.

If you're interested, I've put my entire Jekyll setup on GitHub.
It has all of my Jekyll config, the Docker containers I use to build the site, and a bunch of interesting plug-ins – check out the README for more details.
Over time, I might write up some of the interesting bits as standalone blog posts.

Hopefully this is the last rewrite I'll be doing in a while – so I wanted to do this one properly.
