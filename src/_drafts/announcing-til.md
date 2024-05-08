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
I'm splitting my posts into two sections: [*Articles*][articles] and [*Today I Learned (TIL)*][til].
The articles section is where I'll write longer, in-depth posts meant to be appealing to a wide audience.
The new TIL section will have shorter posts with quick, practical insights, ideal for people arriving from Google and looking for immediate solutions.

The idea of a "today I learned" microblog isn't new -- [plenty][simonwillison] [of other][jbranchaud] [people][github] have been doing it for years.
I've felt for a while that it would be good for me as well, but I couldn't explain why.
There are good reasons for having a TIL section, but "lots of other people are doing it" isn't one of them.
It took a while before I could articlulate why I think it's a good idea for me.

My new TIL section already has [over 50 posts][til], because I've been working on it quietly for a while.
Doing so has given me a better sense of what a TIL section is good for, why I should keep it separate, and how it solves some long-standing issues with the site.

When I write, I want people to find stuff that's interesting and useful.
In this post, I'll explain what I've learnt from writing the TIL section, how I'm thinking about the structure of the site, and why I think this change will make the site better.

[simonwillison]: https://til.simonwillison.net/
[jbranchaud]: https://github.com/jbranchaud/til
[github]: https://github.com/search?type=repositories&q=today+i+learned
[articles]: /articles/
[til]: /til/

## Designing for more than aesthetics

Although I've been pondering this for a while, the recent impetus for these changes was a thoughtful article by Kori about [designing a personal website][melankorin].
It talkes about the structure of your content, not the visual design -- what do you want to include, how to organise it, how do you make it discoverable.

I've come across these ideas before, but never in the context of  a personal site.
I'm used to seeing content modelling applied to much larger websites that have multiple contributors.

My old content model was pretty typical for blog-style websites: a chronological list of posts, plus a collection of static pages for everything else.
I'd never really thought about this; I just used the default setup from [Jekyll], the software I use to build this site.

{%
  picture
  filename="existing_model.png"
  width="500"
%}

It's an excellent default, but I was feeling the limits of this model.
I was trying to put too many different types of writing in posts, and it's difficult to find the best stuff.
Meanwhile, my pages were a disorganised mess that I wasn't maintaining properly.
(I recently found a page that said I worked at a job I actually left eight months ago. Eek!)

I wanted to be more intentional about how I organise my content, and design a better structure, but first I had to answer a different question:

[Jekyll]: https://jekyllrb.com/
[melankorin]: https://melankorin.net/blog/2023/06/19/

## Who are you writing for?

I've shied away from this question for ages, because it feels a bit vain to imagine I have an "audience", and I didn't want a lack of readers to stifle my motivation.
Twelve years in, I've built a small audience, and if I want to take my writing more seriously, I have to think about who I'm writing for.

This site gets about 10,000 visitors a month.
That's small potatoes compared to some popular websites, but it's still a lot -- imagine that many people gathered in one place to hear you speak, and it's quite daunting.

Based on conversations and anecdata, I think I can split my readers into three buckets:

1.  **Me!**
    When I started this site, I was writing for myself -- writing was fun and I wanted to get better at it.
    I posted online because it gave me a vague sense of accountability, but I wasn't fussed about whether anybody was actually reading it.

    I still enjoy writing, and I've found other benefits as well.

    It's especially useful as a way to record my work, and capture [periods of hyperfixation][hyperfixation].
    I often have an idea, spend a week or so thinking about it in great detail, and then my brain moves on to something else.
    Writing a post gives me a sense of completion, and ensures I don't forget all that thinking.
    I refer back to old posts regularly.

2.  **Casual searchers.**
    A lot of people arrive on the site from Google, looking for answers to a specific problem.
    My posts do pretty well in search engines, because they have descriptive titles and they contain useful information.

    These people land on the site, read one post to get the info they need, then disappear.
    They want a quick and easy fix to their current problem, and they don't look at the rest of the site.

    This group is mostly software developers.

3.  **Dedicated readers.**
    These people aren't looking for specific information; they're looking for something fun or interesting to read.

    I think this is mostly people who know me from elsewhere -- friends, family, colleagues.
    They know who I am and want to read something written by me, because they like me and what I write.
    This is a smaller group, but I care about their opinions and experience more than that of casual searchers.

    There are software developers in this group, but they're not the overwhelming majority.

The site is going great for me, and I think it works pretty well for casual searchers -- but I'm unhappy about the experience for dedicated readers.
I think there's a problem with discoverability in my post archives.

I've spoken to people in the past who seemed genuinely interested, visited the site, and were turned off because they only saw posts with very specific titles that they didn't understand.
I'm sure I have articles they'd have found interesting, but they was too difficult for them to find.
I even find myself self-censoring; not mentioning the site to people because I'm worried they'll have an unsatisfying experience when they visit.

I want to do more of the sort of writing that appeals to dedicated readers, and I want it to be easier to find when I do.
This is the main issue that was on my mind as I was rethinking the content model.

[hyperfixation]: https://wellcomecollection.org/articles/ZRrH3RIAACIAALP5

## Let's split the party

I already half-knew that I have different styles of writing, depending on what I'm writing.

1.  If I'm writing a **practical how-to guide**, I try to be short and succinct, and I try to avoid colourful language or literary flair.
    I'm explaining how to solve a specific problem in a particular circumstance, and trying to provide useful information to other people with the same problem.
    I'm optimising for skim reading and quick access to key information.

2.  If I'm writing **anything else**, I try to write something in-depth and engaging that you want to read to the end.
    It might include broader topics, personal reflections or deeper insights, not just practical information.
    These posts take longer for me to write, and I need to work harder to keep you engaged -- I don’t have the easy hook of a promise to a pressing problem.
    But I find these posts more satisfying to write, and I’m more proud of them when they’re done.

Now I write that all out, it's obvious that these styles map to casual searchers and dedicated readers -- but I'd never thought of it that way.
I'd only ever been thinking of the next post, the next thing to write, and I'd never stepped back to consider the structure of the site as a whole.

Because I never spotted this distinction, I was trying to write all my posts as if they'd be read by casual searchers and dedicated readers alike -- even though that almost never happens.
Most of my posts resonate strongly with one group, and get ignored by the other.

I realised that having a single list of "posts" was wrong -- I needed to split the post type in my model.
This is what led to *Today I Learned (TIL)* and *Articles*:

{%
  picture
  filename="new_content_model.png"
  width="500"
%}

With this structure, I could also see how some of my pages fit into this model.
The homepage helps dedicated readers find interesting articles; the contact page is where they go afterward.
Now these pages have a purpose, and aren't just free-floating.

As well as

---

Splitting my posts allows the two types to diverge, and each type can be optimised for its strengths.

Splitting my posts allows the two types to diverge, and each type can be optimised for its strengths. TIL posts can be short, succinct, and I can ditch the lyrical prose – making it faster for casual searchers to find the information they want. Articles can be longer, more detailed, and contain more stuff that dedicated readers find interesting about my style.



---

These post types broadly map to casual searchers and dedicated readers

But because I have a single collection called "posts", I was trying to write every post as it fell into both categories

---

I’d been writing all my posts as if they’d be read by casual searchers and dedicated readers alike, even though that almost never happens. Most of my posts do well with one group, and get ignored by the other.



---

It might include broader topic, personal reflections or deeper insights than an immediate “how-to”. This sort of writing is meant to be appealing to a wide audience.

I'm only interested in

They explain one thing: how to solve a specific problem in a particular circumstance.
This makes them really useful if you have that exact problem, and fairly boring if you don't.

---

Once I'd thought about my audience, the limitations of my old content model became obvious.
I already knew that I had different styles of writing, depending on what I'm writing.



Posts for casual searchers tend to be short, succinct, neutral.
Posts fo

I'd been writing all my posts as if they'd be read by casual searchers and dedicated readers alike, even though that almost never happens.
Most of my posts do well with one group, and get ignored by the other.

I have different styles of writing depending on who I'm writing for.
If I'm writing for a

---

## Different posts for different audiences

Once I'd thought about my audience, the limitations of my old content model became clear.

I'd been writing my posts as if they'd be read by both casual searchers and dedicated readers, even though that almost never happens.
Most of my posts do well with one group, and get ignored by the other.
Trying to serve both groups is a fool's errand, and it makes the posts worse for everyone.

For example, when writing practical how-tos about specific problems, I'd include some extra information or commentary.
I was trying to add colour; to make the post more interesting to a dedicated reader.
But this isn't helping anyone -- a casual searcher will skip that paragraph because it's not about their immediate problem, and most dedicated readers will skip the entire post because it's about a problem they don't have.
They'll never see that extra info!



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

in hindsight this is all obvious
