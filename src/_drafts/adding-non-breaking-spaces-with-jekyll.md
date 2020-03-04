---
layout: post
title: Adding non-breaking spaces with Jekyll
summary: Avoiding inconvenient line breaks with a Jekyll plugin.
category: Blogging about blogging
---

I've been using [Jekyll] to build this blog for about two and a half years.
Because the site is quite simple, I've had plenty of time to work on the long tail of small details: stuff that makes me smile, but won't necessarily be apparent to anyone else.
This post is about one of those details.

[Jekyll]: https://jekyllrb.com/

Most people will notice that the site works well on small screens as well as big.
Lots of web traffic comes from smartphones, so I made sure the design would scale up as well as down.
(I think the technical term for this is [responsive design].)

[responsive design]: https://en.wikipedia.org/wiki/Responsive_web_design

One effect of responsive design is that you can't tell where line breaks will appear.
To keep the text a sensible size, lines have to be different lengths on different devices -- for example, 20 words fit comfortably on a single line on a desktop monitor, but on a phone screen they'd be unreadably small.

Most of the time, this is fine.
It doesn't matter where the line breaks appear.

---

One of the projects I've been working on recently is the [website for PyCon UK 2020][pyconuk].
Because I'm responsible for the site this year, we're using a static site created with [Jekyll], the same tool I use to create this blog.
One of the nice things about using Jekyll is that I can reuse a lot of the tooling from this blog

[pyconuk]: https://2020.pyconuk.org/
