---
layout: post
date: 2015-05-26 19:13:00 +0000
summary: I made a clone of GitHub's Contributions graph to use as a motivational tool.
title: Cloning GitHub's Contributions chart
---

I'm a total sucker for gamification[^1]. If you put a pretty chart in front of me to measure my progress, I fall for it every time. One place I've noticed this recently is with the Contributions graph on my user page on GitHub. This is a year-long calendar that shows a heatmap of all your activity. Here's what mine looks like:

![](/images/2015/github_chart.png)

You can see that my activity started to pick up around March, which is when I started using GitHub at work. I was seeing this chart almost every day, and I began feeling guilty about the amount of blank space. So I've been trying to be more active &ndash; whether that's on my own repos, or pull requests against other people's work &ndash; and I think the change is noticeable.

The GitHub chart has been a particular effective motivator. I think it's the long tail that does it: if I don't do something now, I'll be looking at the blank space for another year. So it got me wondering, could I use this design for something else?

<!-- summary -->

I had a look to see if I could simply repurpose GitHub's existing code, but it's some sort of complex HTML5 canvas object. It goes right over my head, so I couldn't use that. I had to write my own implementation.

My web dev skills aren't great, but I came up with a rough approximation:

![](/images/2015/github_green.png)

It's rendered entirely in plain HTML and CSS. There are also tooltips (if you hover over a calendar cell, it shows how many contributions you made that day), which I tried in JavaScript, but the performance was awful. It's not a perfect clone, but it's fine for my purposes.

Modern CSS means that it's fairly easy to change the look and feel of the graph. Here's another look that I quite like:

![](/images/2015/github_blue.png)

This is accompanied by a Python script that takes a simple plain text file recording "contributions", and returns the HTML. All the code is [on GitHub](https://github.com/alexwlchan/contributions-graph), along with instructions and an example.

I have a few more ideas for some cosmetic tweaks, but it basically works. Now all I have to do is decide what I want to track.

[^1]: <p>The gamification of [physical activity](http://www.marco.org/2015/05/24/filling-the-green-circle) is one of the few reasons I've become interested in the Apple Watch (although not enough to buy one). I was thinking of it only as a device for notifications; I find the fitness aspects much more intriguing.</p><p>This may be driven by some recent surgery. I was stuck in bed, unable to do anything physically intensive, while reading about people doing exercise with their new Watches. I'm sure my desire for the former rubbed off on the latter.