---
layout: post
title: 'Adding a new site section: Today I Learned'
summary: |
  I'm splitting my site into longer-form articles and shorter how-to style posts, which I hope will make the site better for everyone.
tags:
  - blogging-about-blogging
colors:
  index_light: "#6d5648"
  index_dark:  "#c5b5a9"
---
Today I'm splitting my site into two sections: [*articles*](/articles/) and [*today I learned (TIL)*](/til/).
The articles section is where I'll write my longer, more in-depth posts, meant for a wide audience.
The today I learned section is for shorter, how-to style posts, mostly read by people arriving from Google.
I've already created separate indexes and RSS feeds, and over time I expect these sections will diverge further.

The new TIL section already has [over 50 posts](/til/), because I've been working on it quietly for a while.
I didn't want to talk about it until I thought it was likely to stick.

The idea of a "today I learned" microblog is pretty popular -- [plenty][simonwillison] [of other][jbranchaud] [people][github] have already done it -- but that alone isn't a reason to do it.
I had a vague sense that it was a good idea for me, but it was only vibes rather than a concrete reason.

Before I shared this more widely, I wanted to be able to articulate why I thought a separate TIL section was a good idea for *me*.
It's taken a while, but now I think I can explain what it's for, why it should be separate, and how it will make the site better.

[simonwillison]: https://til.simonwillison.net/
[jbranchaud]: https://github.com/jbranchaud/til
[github]: https://github.com/search?type=repositories&q=today+i+learned

## What do I want on this site?

Although I've been pondering this for a while, the trigger for actually making changes was a great article by Kori about [designing a personal website][melankorin].
It's about planning the structure of your content, not the visual design.
What sort of stuff do you want on your website?
(I think the technical term is *content modelling*.)

Although the ideas isn't new to me, that article was the first time I'd seen anyone talk about content modelling on a personal site.
Previously I'd only ever seen people do it for much large sites, typically owned by companies and with multiple contributors.

The old content model for this site was pretty typical for blog-style sites: a list of dated posts, and then one-off pages for everything else.
I hadn't thought much about it; it just comes from the default configuration of [Jekyll], the software I use to build this site.

{%
  picture
  filename="existing_model.png"
  width="500"
%}

Once I thought about it, I could see this model was a bit creaky, and not a great fit for the site I've actually built.
I knew that if I thought about it, I could come up with a better structure, but first I wanted to answer a different question:

[Jekyll]: https://jekyllrb.com/
[melankorin]: https://melankorin.net/blog/2023/06/19/

## Who are you writing for?

This is a question I've ignored for a long time

10,000 unique visitors a month.
That's small by web standards

## what's audience of this site?



  - bit late to ask, better late than never
  - 1/ me
      - initially no visitors
      - writing to practice
      - posting online gave sense of accountability
  - 2/ casual searchers
      - looking in google for answer to specific problem
      - my posts do well here
      - land on site, read one post, go away
      - looking for something quick and easy
      - v unlikely to look around
  - 3/ dedicated readers
      - friends, family, colleagues
      - know who I am and want to read stuff I've written
      - not looking for specific info

how am I doing?
  1/ I'm fine
  2/ site works well
  3/ not convinced it works well -- content is too variable
  
chances are, if you're this far into this post, you're in bucket 3 (or I hope you'll be!)
  
## better content model!

TILs
  - these are for casual searchers
  - typically explain one thing
  - solve specific problem in particular circumstances
  - v descriptive titles => good in google
  - great if you have problem, boring if everything else
  - pretty quick to write, can often write in an hour or so

articles
  - these are for dedicated readers
  - longer prose, take more time
  - more engaging for readers, broader appeal
  - but harder to write! no hook
  - but this is what I want to write more of
  
previously had them shoved into one bucket, neither was good

splitting them out = many advantages

TILs
  - can be short, to the point
  - no attempts at lyrical prose
  - no pretence that will be read by anybody who isn't coming from google
  - shorter, tighter, better for those readers

articles
  - can be longer, more spaced-out
  - homepage only features articles, easier to find
  - easier for dedicated readers to find articles
  - no longer drowned out by TIL posts

can also blend them with the magic of ~hyperlinks~
e.g screenshots

this is content modelling 101, but took me long time to realise
(even watching people write content models for other webistes)
but I got there in the end

meta-goal for this site has been testing ground for new ideas and approaches
writing, programming, and now content design

---

I actually started doing this in January, but I’m only talking about it now
bad habit of having great ideas that don't last
In previous attempts, I’ve shoved them on site domains or side blogs and quickly withered and died

I’ve already written 54 TIL posts this year (about one every two days)
This feels like it’s going to stick

still a few rough edges, e.g. tags
how do I show same tag across both post types. do I need to?


I don’t want to pretend that splitting out TILd into their own section 
Is some sort of miracle cure, But I do think it solves a bunch of My low-grade frustrations about the site
Maybe it’s just confirmation bias, but this change feels right



---

articles will slow down
TILs will speed up
