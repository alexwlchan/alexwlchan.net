---
layout: post
title: Hard problems in social media archiving
summary: 
tags:
  - digital preservation
  - social media
index:
  feature: true
colors:
  index_light: "#5366ac"
  index_dark:  "#607db9"
---
<!-- Social media card image: martin-fisher-5577331_1920.jpg -->

In my [previous post][social-media-scrapbook], I wrote about my new scrapbook of social media -- a place where I can save social media posts that are important to me.
This is a strictly personal archive, which will only ever be updated or accessed by me.
What about larger archives?

Heritage institutions are very interested in archiving social media, given its ever-growing impact on our lives, but it's a nascent field.
I worked in cultural heritage for eight years, including nearly two years at the [Flickr Foundation][flickr-fdn], and I talked to a lot of people about preserving social media.
Everybody I spoke to understood its importance, but the process and tools are still relatively young.
A lot of institutions have a good digital preservation strategy, but comparatively few have a mature approach for preserving social media.

In this post, I'm going to talk about why this is a difficult problem, and how I've approached it in my personal archive.

[social-media-scrapbook]: /2025/social-media-scrapbook/
[flickr-fdn]: https://www.flickr.org/



{% table_of_contents %}



## The Flood: how do you decide what to save?

How do you choose what parts of social media to save?
Do you filter by topic, or by author, or by geographic location? 
What's most important?
Who decides? 

These questions of curation are tricky, and I understand why many people would would prefer to collect everything -- it reduces bias in the selection process. 
The problem is social media operates at a scale where collecting everything is simply impossible. 
Social media is orders of magnitude bigger than even the most well-resourced institution can store.
(YouTube alone gets [over 20 million new videos a day][youtube-scale], which would blow the storage budget for most institutions.)

There's a big tension between "collect everything" and "collect sustainably".

One approach is to treat social media as a graph and try to collect connected subsets of that graph. For example, if you save one post in a conversation, Save the other posts in the conversation so you have all the context in one place. 
This is a limitation of more traditional web archiving tools which typically save a page at a time. They aren't aware of the networked context of social media, and may only save part of a conversation.

In my personal archive, I'm only collecting posts that are important to me, and so the scale is inevitably capped by the rate at which I can consume social media.
I can also choose whether or not to include something based entirely on vibes and personal preference, whereas institutions like to have a set of well-defined rules for what is in scope for their collections.
I can be more loosey-goosey with what I collect. 

(Social graph context?)

[youtube-scale]: https://blog.youtube/press/#:~:text=On average, there are over 20 million videos uploaded daily to YouTube.

> and boundary of what gets collected
>
> Social media posts exist in a network context. Most posts are not isolated entities, but part of a large tapestry conversation. Makes it difficult to understand and interpret later
> If you only preserve one posted at a time, they can be hard to understand.
> 
> Because I am choosing what to collect by hand, I can decide which posts I think I'll worth keeping. I might keep a single tweet, or a whole thread, awesome tweets from the middle of the thread and a few replies.
>
> Because this is a personal archive, I only need contact to myself. I was involved in many of the conversations I'm saving, and I don't remember some of the context. I knew who is involved, and what their expertise is there's context I don't save, because I know it outside the archive.
>
> This is a problem with traditional when having tools like the Wayback machine, which typically focus on saving single pages. Although the machine to save as much as possible, individual posts are individual captures, and it's not always easier possible to zoom out and see the rest of the context.
>
> The risk of saying context is important and worth saying is that it becomes an argument for everything. On some level, everything is context, but trying to preserve an entire social media site is not useful nor practical.
>
> Because this isn't archive only for me, I can decide where to draw that boundary. I can decide based on vibes and personal preference, which likes the required by professional institutions. I can also choose editorialise.
>
> For example, if somebody posted a tweet and then an immediate follow-up with a typo correction, I just save the original tweet and fold in the typo fix. I don't care about preserving the fact that there were two separate tweets. Or if a conversation includes something that I wrote which I now find embarrassing and cringeworthy, I can just admit it.

> Institutions often struggle with:
> * how many hops out in a conversation?
> * do you preserve the whole thread or just the post?
> * do you preserve all replies or only “relevant” ones?
> * do you preserve linked posts? linked accounts?
> * how do you contain scope creep?
> Your “vibes-based boundary” is the personal solution.
> Institutions need a rule — and making one is incredibly hard.

## The Fog: how do you search what you've saved?

Accumulating a large social media archive is no good if you can't find anything in it later.

A common approach to social media archiving is web archiving, where you save the web page for each post.
Putting aside the inefficiency of capturing an entire web page for a single post, which which may be only a few hundred characters, this approach can make it difficult to search across the archive.
You can look up a single post if you know its URL, but you can't find all the posts about a particular topic or by a particular author. 
The Internet Archive has saved millions of tweets, but try finding saved tweets about cats.

With physical objects or smaller digital archives, this problem is solved by cataloguing.
Archivists write a description of the contents of an item and then researchers can search the catalogue to find items they might be interested in.
This approach doesn't scale to social media posts, where you can save a thousand posts in the time it takes a human cataloguer to write a single description. 

In my personal archive, I'm adding keyword tags to every conversation I save. 
This is a good balance of description and time taken for me -- but this is harder to pull off in an institutional context. Among other things, I don't need to coordinate the meaning or usage of my tags with anybody else. 
And my archive is already narrowed to my fairly specific set of interests, so my tags are filtering in a very small pool. 
It's unlikely an institution would have such a niche dataset.
(Is niche the right word?)

> so much stuff!
> problem of storage, and also discoverability

## The Self: who's really talking?

> Identity on social media is:
> * mutable (people change handles)
> * fragile (names are reused after account deletion)
> * cross-platform (one human, many accounts)
> * ambiguous (“which JohnSmith42 is this?”)
> Institutions often need to:
> * track identity over time
> * distinguish between accounts with the same username
> * express uncertainty (e.g., “likely same user”)
> * deal with impersonation or parody accounts
> * record external context (“this is an official account”)
> This is barely mentioned in your draft but is one of the hardest challenges for researchers using archival social-media datasets.
> Your personal archive sidesteps this because you know who you’re looking at.

## The Walled Garden: what if a platform resists being preserved?

In the early 2000s, many social media sites had publicly accessible APIs for getting their content. 
Twitter is the poster child for this access. their API allowed a flourishing ecosystem of third party clients. And the API was easy enough to use that many researchers used it to collect large amounts of Twitter data for preservation and other research. 
(The accessibility of Twitter's API is one of the reasons until we have such extensive Twitter archives.)

This is largely a relic of the past.
Social media platforms are no longer keen on their content being downloaded en masse -- they don't have public APIs, and they aggressively block attempts to scrape or crawl this content. 
These efforts have been exacerbated by companies trying to stop large language models being trained on their data, and preservation tools have been blocked as well.
(And there are instances of AI companies using web archives to [circumvent blocks on their scrapers][ia-blocked-by-reddit].)

The lack of programmatic access makes it much harder for institutions to collect social media at any sort of scale. 
Especially if you want to collect a wide variety of fields, you need to be able to use an API or automated tools. 

In my personal archive, I have a small and simple data model that I can fit in by hand. 
Although I've written scripts to automate the process for websites that have APIs, it's not essential. 
If I can see a post in my web browser or in an app, I can see enough to fill in the data to save it in my scrapbook. 

[ia-blocked-by-reddit]: https://www.theverge.com/news/757538/reddit-internet-archive-wayback-machine-block-limit

> - Why institutional-scale solutions are blocked by rate limits, disappearing APIs, paywalls, and hostile platforms.
> - You can just… type.

## The Ethics: do people want to be preserved?

Many web archives have largely ignored issues of consent.
If something is available on the public internet, it's fair game to be scraped and downloaded into an archive, whether or not the original author wants their content to be preserved. 
Once preserved, this deprives the original author the ability to delete their posts from the internet. 
If somebody posts an embarrassing thought, or a personal picture, and it gets sucked into a web archive, it's much harder for them to remove it from the internet. 

This problem has been bubbling under the surface for years. But people have a renewed interest in how their data is used thanks to generative AI. 
Now that people are aware their data is being sucked up to train large language models, tools, they're much more careful and cautious about where their data is copied. I think we could see a big retreat from open access, Creative Commons, and public by default.

If you take a hard-line ethical stance, you should only collect material where authors have explicitly agreed to have their material collected. Institutions typically govern this with some sort of collection agreement where you allow the institution to keep a copy of your material and sign away the right to remove it afterwards.
This is squeaky clean, but it's hard to scale. 

It also comes with preservation risks. What about people who can no longer consent? There are social media websites that have been around for decades, with lots of users who have abandoned the site, lost their password, or have just died. made. If you need their explicit consent to save their material, and you have no way of contacting them or their next of kin, then their posts will never be preserved. 

How do people feel about their social media posts being preserved? Many people seem to be broadly supportive of web archives and the Internet Archive and web archives in general but what if it's their posts on the line? do they feel the same?

Anecdotally, I see a lot more people trying to protect their social media posts. Hiding their posts from public view, you, restricting them to private friends, using disappearing media like one-time messages or expiring stories.
There is an intent here:I want you to see this, but I don't want you to have a copy of it forever. 

One project I'm following with interest is BlueSky's user intents, where they plan to ask users how they feel about their posts being reused for a variety of purposes, including training machining learning models and digital preservation. It's only a draft, but if accepted I'd really like to see what sort of response it gets. 

In my personal archive, I'm largely ignoring issues of privacy and consent. 
This is only an archive for my personal views which I'm never going to share with anybody else. There's no risk of me sharing something beyond its original intended audience. I can only save a post if it was visible to me once, and I'm not going to make it visible to anybody else. 

I feel like it's fine for me to have these posts, but not to share them. 

When I'm deciding what to save, I consider how somebody might feel if they knew I'd saved a copy of their posts. 
Would I feel comfortable telling them? them. For example, I think it's fine for me to save a conversation I was a part of or or posts about a topic I'm interested in, but it would be creepy if I downloaded every post somebody had made, including posts from conversations that didn't include me. 

> - You’re exempt from institutional ethics problems.
> - “This archive is for me, not for the world.”
>
> * Ignore issues of privacy/consent
> 	* This is only an archive for personal use, never going to share
> 	* So less issue with me sharing stuff beyond intended bubble
> 	* Analogue: me tcopying something into a diary
>
> creepy factor
> 
> Another big issue for social media preservation is consent.
> 
> I’m sure many of you will be familiar with the CARE and FAIR principles for Data Integrity
> Asking for consent is our way of encoding those in software
> 
> In particular “authority to control”
> A lot of people have found their data sucked up into systems, and then they have no way of controlling it
> For example
> 
> And consent is hard, it comes at a price; what about people who can no longer consent?
> Flickr is over 20 years old – there are lots of users who’ve abandoned the site, lost their password, or have just died
> If we need their consent to put their photos in a DL, then their photos can never go in a DL!!!
> Which undermines our ability to preserve them!
> 
> This is a fast-moving topic
> GenAI has sucked up all our stuff, people wondering how they feel about its
> I think we’re seeing a real retreat from open access, Creative Commons licenses, public by default
> 
> Many people now protect their social media posts for example only making them available to logged in users, unknown friends. Can that post be reserved? What if a poster was initially public, but later made private or deleted? (Established rules for this in a creative comments context, but social media websites rarely have such explicit licensing. That's a tricky question for big institutions.
> 
> I can mostly ignore this, because my only criteria is that a post was visible to me at some point. I never going to share my archive with anybody else, so I'm never going to share a post with somebody who the original author didn't want to see it. Of course, a post author might sense of decided they no longer want me to see it, but that's harder to force.
> 
> I feel like my archive is a kin to a folder of screenshots of social media.
> 
> It's fine for me to have these posts, but it's not okay to share them.
> 
> cf disappearing social media

## The Law: how does policy shape preservation?

> Institutions run into:
> * GDPR and the “right to erasure”
> * CCPA, COPPA, and privacy laws
> * national restrictions (e.g., German hate-speech rules)
> * takedown requests and DMCA
> * subpoenas (archives can be compelled to produce data)
> * conflicts between “preserve” vs “delete on request”
> This is generally a big part of institutional practice, especially for social-media harvesting, and you're not covering it yet. It’s distinct from “consent” — it’s about law, not preference.
> You might want to at least nod to it.

## The Feed: do you preserve the experience?

> Alex writes frequently about presentation, formats, rendering, and UX.
> In institutional preservation, capturing what the user actually saw is an unsolved challenge:
> * Infinite scroll vs. paginated captures
> * Algorithmic timelines (which are not reproducible)
> * Hidden replies, blocks, algorithmic ranking, “For You” tabs
> * Ephemeral UI elements (live counts, badges, tooltips, quote-tweet previews)
> * “Dark mode,” “light mode,” custom themes
> Institutions can capture objects, but often not the experience, which means they may misrepresent how information was encountered at the time.
> Alex’s scrapbook gets around this by designing its own stable representation.
> Institutions don’t have that luxury.
> Where it fits: as a subsection under “the rot” (format + interaction preservation), or as an additional major section (“The illusion of reproducibility”).

## The Ledger: can you prove a post is what it claims to be?

> 1. The problem of verifying authenticity (provenance, integrity, and trust)
> Alex often writes about correctness, audits, test suites, and the “chain of custody” for data.
> For institutional social-media archives, this is a huge missing challenge:
> * How do you know a captured post is authentic?
> * How do you show a researcher that a capture is complete and unaltered?
> * How do you prove that a screenshot hasn’t been edited?
> * What do you do when platforms retroactively edit, delete, or “shadow-update” content?
> This matters for scholarship, journalism, and legal evidence, and it ties directly to alex’s interest in metadata validation and test suites.
> It’s not mentioned in your draft, but institutions care about it a lot.


## The Rot: how do you prevent digital decay in your archive?

One of the perpetual problems in digital preservation is deciding what file formats to use. 
Do you save files in the original format (which preserves the most authentic copy of the file but might be harder to read), or convert them to a newer file format (which might lose some nuance of the original but be more widely readable)?
If you do a conversion, what do you convert to?

Once you have a file stored, how do you present it?
How do you allow somebody to view it, like they might view an old book in a reading room?

There is no "native" file format for social media.
On the backend, posts are stored in massive databases that (1) you aren't going to be allowed to archive and (2) require a lot of operational knowledge to use and understand, even if you did have a copy.

If you have a collection of, say, PDF files, you can just provide those for download. 
What do you do for social media?

You could use something like web archiving, but storing copies of web pages is inefficient and makes it difficult to do cross collection searching.
You could build your own database and viewer application, but that's more complicated than a simple file repository.

In my personal archive, I'm storing metadata in a JavaScript/JSON file, and rendering it as a static website.
That approach is likely to last a long time, because it's built on standard web technology, but it's not an approach that scales.
I have ~4000 conversations and a 7MB metadata file.
If I wanted to store 10&times; or 100&times; as many conversations, I'd need to rejig how I'm storing metadata.

## The Long Haul: how do you keep the archive going?

> Alex often emphasises maintainability, small/simple tooling, avoiding operational complexity, and the cost of running software over time.
> Institutional archives face:
> * Ongoing cost of storage (especially for high-volume social content)
> * Ongoing cost of re-processing when formats or standards change
> * Bit-rot, checksum verification, migrations
> * Maintaining crawlers, scrapers, tools that continuously break
> * Staffing needs (ops, archivists, engineers)
This is not the same as “scale” or “format decay” — it’s about the institutional obligation to keep the archive alive for decades, with limited budgets and staff turnover.
Alex’s personal archive avoids this because it is small, tested, and doesn’t require infrastructure.
