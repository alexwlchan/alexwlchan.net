---
layout: post
title: Hard problems in social media archiving
summary: Preserving social media is easier said than done. Why is it so diffcult for institutions face when they want to back up the Internet?
tags:
  - digital preservation
  - social media
index:
  feature: true
colors:
  css_light: "#5366ac"
  css_dark:  "#607db9"
---
<!-- Social media card image: martin-fisher-5577331_1920.jpg -->

In my [previous post][social-media-scrapbook], I wrote about my scrapbook of social media posts -- a tiny, private archive where I can save conversations that I care about.
What happens when larger institutions try to preserve social media?

Cultural heritage institutions know the historical importance of social media, and everyone I've worked with understands the urgency -- including when I worked at the [Flickr Foundation][flickr-fdn].
But preserving social media is difficult, and it's not a well-developed area of practice.
The enthusiasm is there, but the processes and tools are still relatively young.
Many institutions have a mature strategy for digital preservation, but few have a strategy for social media.

In this post, I'm going to explain why preserving social media is so hard, and how I've approached it in my scrapbook.

[social-media-scrapbook]: /2025/social-media-scrapbook/
[flickr-fdn]: https://www.flickr.org/

{% table_of_contents %}

---

## The Flood: how do you decide what to save?

The sheer size of social media is the first problem.
It exists at a scale that's hard to comprehend: billions of posts, with millions more being added each day.
Any person's view of social media is a tiny sliver of the whole.

This makes it difficult for anybody to select a subset of social media to preserve, because the vast majority of it is invisible to them.
Making a choice introduces selection bias, and I've talked to many people who want to avoid that bias by "collecting everything".
But that's impossible -- collecting everything is beyond the technical or financial scope of any heritage institution.

Since they can't collect everything, institutions create rules -- collection policies that define what's in-scope.
These rules are meant to ensure consistency and reduce individual bias, but they force archivists to draw boundaries in a medium that inherently resists boundaries.

Social media isn't a sequence of isolated pages; it's a dense, interconnected graph.
A single post only makes sense in context -- the replies, the people, the topic du jour.
How much of this context do you gather?
How many hops out do you follow?
Do you save the whole thread, every reply, every linked account?
How do you prevent scope creep from sucking in everything?

In my personal scrapbook, I'm only interested in saving the sliver of social media that I see, and only a subset of that.
I save threads I think are interesting; I keep posts that I find moving; I prune replies that are embarrassing or unhelpful.
My "collection policy" is pure vibes.
My archive is subjective and inconsistent, because the only audience is me.

Institutions can't be that casual.
They need durable, defensible rules about where their collection starts and ends.
And on social media -- where every post is context to a larger tangle of conversation -- drawing that boundary is the hardest part.

## The Fog: how do you search what you've saved?

We collect things so we can look at them later.
This means we need organisation, some way to reach into our collection and find specific items.
This can be a problem in social media archives, there the collections are too large and sparsely-described to be easily searchable.

A common approach to preserving social media is web archiving, where you save a copy of the web page for each post.
The largest example of this is the Wayback Machine.
This approach is easy to automate, but the archive is inefficient and difficult to earch.
You can find a single post if you know its URL, but it's hard to search for posts about a particular topic or by a particular author.

With physical objects or smaller digital archives, we solve this problem with cataloguing.
Archivists write a description of an item, and researchers can search the catalogue descriptions to find items they might be interested in.
This doesn't scale to social media posts, where a machine can save a thousand posts in the time it takes an archivist to write a single free-text description.

In my scrapbook, I'm adding keyword tags to every conversation.
It's a good balance of description and time -- I can add tags quickly, and it makes it easier for me to find stuff later.
These tags are loosier than a controlled vocabulary like [LCSH] or [MeSH] -- only I have to understand what the tags mean, and I don't need to agree on definitions with anybody else.
This feels like an approach that could work in institutions.

> I can even collapse typo-correction follow-ups into a single cleaned-up note.
> Traditional web-archiving tools, designed around page-by-page capture, often miss this surrounding networked context.

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
Twitter is the poster child of this approach -- their API allowed a flourishing ecosystem of third-party clients, and it was easy enough to use that many researchers used it to collect large amounts of Twitter data for preservation and other research. 
(The accessibility of Twitter's API is one reason we have such extensive Twitter archives.)

This is largely a relic of the past.
Social media platforms are no longer keen on their content being downloaded en masse -- they don't have public APIs, and they aggressively block attempts to scrape or crawl this content. 
This has intensified as companies try to stop large language models being trained on their data, and preservation tools get blocked at the same time.
(Especially as there are instances of AI companies using web archives to [circumvent blocks on their scrapers][ia-blocked-by-reddit].)

The lack of programmatic access makes it hard for institutions to collect social media at scale. 

In my scrapbook, I can just type.
I have a small and simple data model that I can fill in by hand. 
Although I've written scripts to automate the process for websites that have APIs, it's not essential. 
If I can see a post in my web browser or in an app, I can see enough to fill in the data to save it. 

This works for me because I'm only saving a small number of posts, and I'll accept the small possibility of human error during manual data entry.
The lack of scale and risk of mistakes means this is probably less appealing to institutions.

[ia-blocked-by-reddit]: https://www.theverge.com/news/757538/reddit-internet-archive-wayback-machine-block-limit

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