---
layout: post
date: 2025-07-08 15:51:22 +00:00
title: Moving my Glitch apps to my own web server
summary: I've moved almost all of my Glitch apps to websites running on my own web server, on this domain.
tags:
  - glitch
  - fun stuff
---
About six weeks ago, Glitch [announced that they're shutting down][sunset].
Glitch was a platform where you could make websites and web apps, with a heavy emphasis on creativity and sharing.
You could read the source code for any project to understand how it worked, and remix somebody else's project to create your own thing.

Unfortunately, Glitch is shutting down project hosting today.
If you had an app on Glitch, it's about to stop running, but you can set up redirects to another copy of it running elsewhere.

I've created redirects for all of my apps, and moved them to the web server that runs this site.
This was pretty straightforward, because all of my "apps" were static websites that I can upload to my server, and they get served like the rest of my site:

*   [Checkbox text adventure](/fun-stuff/checkbox-text-adventure/) is a silly game where you can click, lick, and smell a checkbox.
    I made it with [Twine](https://twinery.org) as a response to Nolen Royalty (eieio)’s game [One Million Checkboxes](https://eieio.games/blog/one-million-checkboxes/).

*   [How long is my data?](/fun-stuff/howlongismydata/) is an app that measures your data in the world's most practical unit: the length of shelving you'd need to store it on 3½&Prime; floppy disks.

*   [Looped squares](/fun-stuff/looped-squares/) lets you draw looped shapes based on the [Mac's command ⌘ icon](/2024/command-icon/).

*   [Marquee rocket](/fun-stuff/marquee-rocket/) is a perverse experiment in trying to [use the `<marquee>` tag](/2022/marquee-rocket/) to make an interactive web app.

*   [Rainbow hearts](/fun-stuff/rainbow-hearts/) and [Rainbow valknuts](/fun-stuff/rainbow-valknuts/) are two Pride-themed apps that draw geometric shapes based on different flags.

*   [UK stations map](/fun-stuff/uk-stations-map/) lets you plot a map of all the railway stations you've visited in the UK.

Not all of my Glitch apps made the jump -- I deleted a couple of very early-stage experiments, and I have yet to spin up new copies of my [Chinese vocabulary graph](/2020/storing-language-vocabulary-as-a-graph/) or the [dominant colours web app](/2022/dominant-web-colours/).
I might port them later, but they're not static websites so they're a bit more complicated to move.

Glitch felt like a throwback to the spirit of the early web -- the platonic ideal of "view source" and "anyone can make a website".
I always liked the idea of Glitch, and I enjoyed making the fun apps that I hosted there.
I'm sad to see it close -- another space for playful creativity crushed by the commercial tide of the web.

[sunset]: https://blog.glitch.com/post/changes-are-coming-to-glitch/
