---
layout: post
date: 2020-03-04 09:42:35 +0000
title: A Jekyll filter for adding non-breaking spaces
summary: Avoiding inconvenient line breaks with a Jekyll plugin.
category: Blogging about blogging
---

I've been using [Jekyll] to build this blog for about two and a half years.
Because the site is quite simple, I've had plenty of time to work on the long tail of small details: stuff that makes me smile, but won't necessarily be apparent to anyone else.
This post is about one of those details.

[Jekyll]: https://jekyllrb.com/

Most people will notice that the site works well on small screens as well as big.
Lots of web traffic comes from smartphones, so I made sure the design would scale down as well as up.
(I think the technical term for this is [responsive design].)

[responsive design]: https://en.wikipedia.org/wiki/Responsive_web_design

One effect of responsive design is that you can't predict where line breaks will appear.
To keep the text a sensible size, lines have to be different lengths on different devices -- for example, 20 words fit comfortably on one line on a desktop monitor, but on a phone screen they'd be unreadably small.

Most of the time, this is fine.
It doesn't matter where the line breaks appear.
But there are a handful of phrases I use regularly where a line break in the middle would be a bit annoying.
Phrases like *"PyCon UK"*, *"RFC 1234"* or *"part 3"*.
If the two words were split over multiple lines, it wouldn't be the end of the world, but it'd be a bit annoying.
It's a digital paper cut.

{% inline_svg "_images/2020/line_breaking.svg" %}

In HTML, you can use a [non-breaking space] to tell a browser "don't put a line break here".
If I write `RFC&nbsp;1234` instead of `RFC 1234`, the two words will always appear on the same line.
If the phrase is too long for one line, both words move down to the next line.

[non-breaking space]: https://en.wikipedia.org/wiki/Non-breaking_space

But I don't want to have to remember that every time I'm writing -- it's only a display issue.
Instead, I've written a [Jekyll filter] that adds these non-breaking spaces for me.
Here's what it looks like:

[Jekyll filter]: https://jekyllrb.com/docs/plugins/filters/

```ruby
module Jekyll
  module AddNonBreakingSpacesFilter
    def add_non_breaking_spaces(input)
      text = input

      text = text.gsub(/RFC (\d+)/, 'RFC&nbsp;\1')
      text = text.gsub(/([Pp]art) (\d+)/, '\1&nbsp;\2')
      text = text.gsub("PyCon ", "PyCon&nbsp;")

      text
    end
  end
end

Liquid::Template::register_filter(Jekyll::AddNonBreakingSpacesFilter)
```

Then I use this filter in one of my base templates, so everything on the site gets these modifications.
Rather than adding the non-breaking spaces as I write, I type as I would normally (with a regular space), and the non-breaking version is added at build time.
It's an improvement that I don't think anyone but me has ever noticed, but it avoids a tiny paper cut every once in a while.

This is one of the nice things about using an existing, stable tool like Jekyll.
All the baseline functionality is good enough that I don't need to worry about it, and I have time to work on fun bits of polish like this.
