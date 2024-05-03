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

I've shied away from this question for ages, because it feels a bit conceited to imagine I have an "audience" -- but I do, even if it's only a small one.
If I want to take my writing more seriously, I have to think about who I'm writing for.

(This site gets about 10,000 unique visitors per month.
Maybe that's not big in Internet terms, but if I imagine that many people gathered in one place to hear me speak, it's mildly terrifying.)

There are three groups I think about when I'm writing:

1.  **Me!**
    When I started this site, I was just writing for myself -- writing was fun and I wanted to get better at it.
    I posted online because it gave me a vague sense of accountability, but I wasn't fussed about whether anybody was actually reading it.

    I also find writing a useful way to capture [periods of hyperfixation][hyperfixation].
    I'll have an idea, spend a week or so thinking about it in great detail, and then my brain moves on to something else.
    Writing an article gives me a sense of completion that makes it easier to move on, and ensures I don't forget all that thinking.
    I refer back to old articles regularly.

    I want everything I write to be fun, interesting, or something I'll want to look back on later.

2.  **Casual searchers.**
    A lot of people arrive on the site from Google or another search engine, looking for answers to a specific problem.
    My posts do pretty well in search queries, because they have descriptive titles and they contain practical information.

    These people land on the site, read one post to get the info they need, then disappear.
    They want for a quick and easy fix to their current problem, and they're unlikely to look around at the rest of the site.
    They usually only look at a single page.

    This group is the majority of traffic -- about two-thirds of my visitors come from a search engine, and almost all of that is from Google.

3.  **Dedicated readers.**
    These are people who know who I am and want to read something written by me, because they like me and what I write.
    They aren't looking for specific information; they're looking for something interesting and engaging.

    I think this is mostly people who know me well -- friends, family, colleagues.
    It's a smaller group, but I care about their opinions more than those of casual searchers.

So how am I doing?
I'm pretty happy with how the site is going for me, and I think it works pretty well for casual searchers -- but I'm not sure how good it is for dedicated readers.
(Which probably includes you, if you've read this far into the post!)

I've spoken to people in the past who seemed genuinely interested, visited the site, and were turned off because they only saw posts with very specific titles that they didn't understand.
I'm sure I have articles they'd have found interesting, but they was too difficult for them to find.
This has been a long-standing problem with the site, and it's one I'm keen to solve.
I want to do more of the sort of writing that appeals to dedicated readers, and I don't want it to get buried.

This is the stuff that was on my mind as I was rethinking the content model.

[hyperfixation]: https://wellcomecollection.org/articles/ZRrH3RIAACIAALP5

## Different posts for different audiences

Once I'd thought about my audience, the limitations of my old content model became clear.

I'd been writing my posts as if they'd be read by both casual searchers and dedicated readers, even though that almost never happens.
Most of my posts do well with one group, and get ignored by the other.
Trying to serve both groups is a fool's errand, and it makes the posts worse for everyone.

For example, when writing practical how-tos about specific problems, I'd include some extra information or commentary.
I was trying to add colour; to make the post more interesting to a dedicated reader.
But this isn't helping anyone -- a casual searcher will skip that paragraph because it's not about their immediate problem, and most dedicated readers will skip the entire post because it's about a problem they don't have.
They'll never see that extra info!

I realised that having a single list of "posts" was wrong -- I needed two different types of post, one for casual searchers and one for dedicated readers.
This led me to create split the post type in my content model, one for each group:

{%
  picture
  filename="new_content_model.png"
  width="500"
%}

Now I have two sub-types of post:

1.  A *Today I Learned (TIL)* post is for casual searchers.
    They explain one thing: how to solve a specific problem in a particular circumstance.
    This makes them really useful if you have that exact problem, and fairly boring if you don't.

    I can write TIL posts pretty quickly, and give them descriptive titles so they're easily discoverable from Google.

    Examples: [How to see the HTTP requests being made by pywikibot], [Why is Pillow rotating my image when I save it?]

    [How to see the HTTP requests being made by pywikibot]: /til/2024/how-to-see-pywikibot-http-requests/
    [Why is Pillow rotating my image when I save it?]: /til/2024/photos-can-have-orientation-in-exif/

2.  An *article* is an longer, in-depth piece of writing meant for dedicated readers.
    It might include broader topic, personal reflections or deeper insights than an immediate "how-to".
    This sort of writing is meant to be appealing to a wide audience.

    These posts take more time to write, and I need to work harder to keep readers engaged -- I don't have the easy hook of a promise to a pressing problem.
    But I find these posts more satisfying to write, and I'm more proud of them when they're done.

    Examples: [Taking regular screenshots of my website](/2024/scheduled-screenshots/), [Making a PDF that’s larger than Germany](/2024/big-pdf/), [Hyperfocus and hobbies](/2023/hyperfocus-and-hobbies/)

With this structure, I could also think about how some of my pages fit into this model.
The homepage is meant to help dedicated readers find interesting articles; the contact page is where they go afterward.
Now these pages have a purpose, and aren't just free-floating.

Splitting my posts allows the two types to diverge, and each type can be optimised for its strengths.
TIL posts can be short, succinct, and I can ditch the lyrical prose -- making it faster for casual searchers to find the information they want.
Articles can be longer, more detailed, and contain more stuff that dedicated readers find interesting about my style.

had a profound impact on how I think about my writing

can also blend them with the magic of ~hyperlinks~
e.g screenshots

this is content modelling 101, but took me long time to realise
(even watching people write content models for other webistes)
but I got there in the end

meta-goal for this site has been testing ground for new ideas and approaches
writing, programming, and now content design

## How's it going?

really well!

floor to posting has dropped to zero
has filled gap left by twitter

using it as a sort of public notes, seed stuff for google

hyperlinks for the win

---

I actually started doing this in January, but I’m only talking about it now
bad habit of having great ideas that don't last
In previous attempts, I’ve shoved them on site domains or side blogs and quickly withered and died

I’ve already written 54 TIL posts this year (about one every two days)
This feels like it’s going to stick

and pages still need work

still a few rough edges, e.g. tags
how do I show same tag across both post types. do I need to?


I don’t want to pretend that splitting out TILd into their own section
Is some sort of miracle cure, But I do think it solves a bunch of My low-grade frustrations about the site
Maybe it’s just confirmation bias, but this change feels right



---

articles will slow down
TILs will speed up
