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

Although I've been pondering this for a while, the impetus for these recent changes was a thoughtful article by Kori about [designing a personal website][melankorin].
It talks about the structure of your content, not the visual design -- what do you want to include, how to organise it, how do you make it discoverable.

I've come across these ideas before, but never in the context of  a personal site.
I'm used to seeing content modelling applied to much larger websites that have multiple contributors.

My old content model was pretty typical for blog-style websites: a chronological list of posts, plus a collection of static pages for everything else.
I'd never really thought about this; I just used the default setup from [Jekyll], the software I use to build this site.

{%
  picture
  filename="existing_model.png"
  width="500"
  alt="Hand-drawn sketch of a diagram with two boxes: 'posts' and 'pages'"
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
  alt="Hand-drawn diagram with several more boxes: two labelled 'articles' and 'TILs' which are bracketed together as 'posts', plus a box called 'homepage' that points to 'articles', and another called 'contacts' pointed to by 'posts'."
%}

As well as splitting the two types conceptually, I also wanted to split the way you get to them.
I've created separate index pages and RSS feeds for the two types, and now the homepage only shows you recent articles.
TIL posts are slightly harder to find on this site, because I know most people are finding them through Google instead.

With this structure, I could also see how some of my pages fit into this model.
The homepage helps dedicated readers find interesting articles; the contact page is where they go afterward.
Now these pages have a purpose, and aren't just free-floating.

This distinction seems obvious in hindsight, but it took me a long time to see it.

At the beginning of this year, I quietly created the new section and started writing my TIL posts there.
Although this split sounds good in theory, I wanted to get some practice with this setup before sharing it more widely.

## How's it going?

I'm really pleased with how this has gone.
Splitting my posts has allowed the two types to diverge, and I can really lean into the strengths of each style.

I'm writing more Today I Learned posts than I did in the past (so far I've written one every other day).
This is because I've lowered my threshold for posting, and I'd rather write a TIL that's short and simple than nothing at all.
I'm treating it as a sort of public notebook.

Here are some reflections:

*   A common structure is "here’s what I tried, here’s what happened, and here's what I learnt".
    This is pretty easy for me to write, so I can write more quickly.

*   I've realised that in the past, I'd be hesitant to write a TIL-style post if it would push an article with broad appeal off the list of recent posts off the homepage.
    Now TIL posts don't appear on the homepage, that hesitation is gone.

*   I don't think this split has cannibalised my articles at all.
    Looking over the list of TILs I've posted, I doubt any of them would have been written as longer articles if I hadn't made this split -- they just wouldn't have been written at all.

*   I'm really leaning into TIL posts as a place to put reference links.
    When I'm researching a problem, I open lots of browser tabs and dig through them to find the information I want.
    Later I may want to re-read one of those tabs, but it can be pretty difficult to re-find websites.
    By linking to the useful tabs from my TIL posts, it's easier to find them again.

I haven't posted as many articles in that time, but that's okay -- I can't write long pieces at the same rate as short TIL posts.
I do have several new articles in draft, and they're much longer and more detailed than articles I've written in the past.
Inevitably that means they take longer to write, to edit, and to finish, but I think they'll be better for it.
I'm taking a swing at some hard topics I've avoided in the past, and I'm enjoying the challenge.

## What's next?

I'm going to keep writing, obviously.

I want to keep thinking about the content model.
This new version is a step in the right direction, but there's more to do.
I want to think more about how I use tags to organise posts.
(For example, right now you can see all the articles or all the TILs that use a particular tag, but not both.
Does that matter?)
I also want to keep breaking down the amorphous blob called "pages", and be more intentional about that content.

I don't want to pretend that splitting out TILs into their own section is a miracle cure, but it has solved a bunch of my low-grade frustrations.
If somebody new visits my homepage, they see a selection of writing that I'm proud of, and I feel they can probably find something they want to read.
They won't be confused or put off by posts with specific and jargon-y titles.

For the first time in ages, I'm not embarrassed to tell people the site exists.

