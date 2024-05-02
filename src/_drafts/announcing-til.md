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
Today I'm splitting my site into two sections: [*Articles*](/articles/) and [*Today I Learned (TIL)*](/til/).
The articles section is where I'll write longer, in-depth posts meant to be interesting to a broad audience.
The new TIL section will have shorter posts with quick, practical insights, ideal for people arriving from Google and looking for immediate solutions.

The concept of a "today I learned" microblog isn't new -- [plenty][simonwillison] [of other][jbranchaud] [people][github] have been doing it for years.
I felt like it might be useful for me as well, but I couldn't explain why.
There are good reasons for having a TIL section, but "lots of other people are doing it" isn't one of them.
It took a while before I could explain why I think it's a good idea for me. 

My new TIL section already has [over 50 posts](/til/), because I've been working on it quietly for a while.
Writing it in private for several months has given me a better sense of what a TIL section is good for, why it should be separate, and how it will make the site better.

My goal is simple: to help people find interesting, useful stuff that I've written.
In this post, I'll explain what I've learnt from writing the TIL section, how I'm thinking about the structure of the site, and why I think this change will help my goal.

[simonwillison]: https://til.simonwillison.net/
[jbranchaud]: https://github.com/jbranchaud/til
[github]: https://github.com/search?type=repositories&q=today+i+learned

## What do I want on this site?

The impetus for these changes was an interesting article by Kori about [designing a personal website][melankorin].
It talks about the structure of your content, not the aesthetic design -- what do you want to include, how do you organise it, how do you lay it out effectively.

I've come across these ideas before, but never in the context of a personal site.
I'm used to seeing content modelling applied to larger, corporate websites with multiple contributors.

I'd never thought much about my own content model; I'd just used the default setup from [Jekyll], the software I use to build this site.
Before I started this work, my site was a chronological list of posts, with tags for organisation, plus a collection of static pages for everything else.

{%
  picture
  filename="existing_model.png"
  width="500"
%}

This is pretty typical for personal blog-style sites, and it's a good starting point -- but I was feeling the limits of this model.
Once I drew it out on paper, I realised that I wanted something more granular.
I was trying to put too much different stuff in the "posts" collection, and I wasn't keeping track of what I'd put in the "pages" collection.
(As part of this work, I found one page that was at least a year out of date, and still talked in detail about a previous employer.)

I wanted to think more carefully about how I organise this site, and what a better content model might look like, but first I had to answer a different question:

[Jekyll]: https://jekyllrb.com/
[melankorin]: https://melankorin.net/blog/2023/06/19/

## Who are you writing for?

I've been avoiding this question for ages, because it feels a bit conceited to imagine I have an "audience" -- but like it or not, I do.
This website gets about 10,000 unique visitors a month.


**The main reason I write for this site is because I want to.**
Nobody is paying me


When I started this site, I didn't have any readers.
I was doing it to practice my writing skills, and posting my work online gave me a vague sense of accountability.

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
