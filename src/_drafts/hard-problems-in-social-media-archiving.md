---
layout: post
title: Hard problems in social media archiving
summary: Preserving social media is easier said than done. What makes it so diffcult for institutions to back up the Internet?
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

## Deciding what to preserve

### The scale of social media is overwhelming

Social media exists at a scale that's hard to comprehend: billions of posts, with millions more being added each day.
Any person's view of social media is a tiny sliver of the whole.

This makes it difficult for anybody to select a subset of social media to preserve, because the vast majority of it is invisible to them.
Making a choice introduces selection bias, and I've talked to many people who want to avoid that bias by "collecting everything" -- but that's far beyond the capacity of any institution.

Since they can't collect everything, institutions create rules -- collection policies that define what's in-scope.
These rules are meant to ensure consistency and reduce individual bias, but they force archivists to draw boundaries in a medium that inherently resists them.

Social media isn't a sequence of isolated pages; it's a dense, interconnected graph.
A single post only makes sense in context -- the replies, the people, the topic du jour.
How much of this context do you gather?
How many hops out do you follow?
Do you save the whole thread, every reply, every linked account?
How do you prevent scope creep from sucking in everything?

My personal scrapbook is subject and inconsistent, because the only audience is me.
My "collection policy" is pure vibes -- I save threads I think are interesting; I keep posts that I find moving; I prune replies that are embarrassing or unhelpful.

Institutions can't be that casual.
They need durable, defensible rules about where their collection starts and ends.
On social media -- where every post is context to a larger tangle of conversation -- drawing that boundary is the hardest part.

### Private and disappearing content

Most social media archiving efforts focus on publicly available, long-lasting content.
This excludes other types of material which make up an ever-growing proportion of social media.

Two major categories stand out:

1.  Private social media -- direct messages, private accounts, closed groups, paywalled forums.
2.  Ephemeral features -- content that deliberately disappears or expires -- think Snapchat, Instagram Stories, or one-time messages.

Collecting this material is difficult.
Technically, much of it is behind authentication walls or interfaces that most web archiving tools can't reach.
Ethically, archivists have to be careful not to violate social norms or user expectations -- many people would be surprised if their private or temporary posts were copied to a public, permanent archive.

It isn't impossible, and I've seen a handful of projects capture private and ephemeral media -- for example, researchers analysing Instagram Stories and their use in political campaigns.
These efforts rely on a patchwork of methods: accessing content through user logins, browser plugins, even taking screenshots.
They tend to be small, targeted, and short-lived.

My scrapbook has a small amount of private content, mostly conversations between me and locked accounts on Twitter.
I'm comfortable with that because I was part of those conversations, and my archive is entirely private.
(For more on the ethics, see "Rules and responsibilities" below.)
I haven't saved any ephemeral content.

Private and ephemeral posts have a different dynamic from public timelines.
People can be more personal, vulnerable, and candid when they know their posts can't be seen by anyone, forever.
Maybe those moments won't appear in institutional social media archives -- but if so, we should acknowledge that limitation, and what stories it leaves out.

### Implicit knowledge, cultural context, and memes

Social media relies on shared knowledge: current events, in-jokes, and memes.
Without this context, the meaning of a post can fade -- or an entirely new meaning can take its place.

It's impossible to preserve all this background information.
People rarely link to the thing they're referring to; they rely on their audience to already know.
A key part of any creative work is deciding how much to explain and how much to leave implied.
Sometimes it's a tiny in-joke for a handful of fans, other times it's essential to understanding the point.

This isn't a new problem -- all human communication requires context -- but social media [takes it to eleven][wiki-spinal-tap].
The pace and brevity are a fertile breeding ground for memes whose origins disappear almost immediately.
Log off for a day, and you'll miss the moment that makes a whole thread make sense.
Imagine how much harder it is to understand if you arrive years -- or decades -- later.

Institutions try to fill in the gap with catalogue descriptions, but that's only possible if somebody understands the references well enough to describe them.
With social media's scale and speed, it's impossible for anybody to know all the jokes, memes, and ideas that might affect a post.

In my personal scrapbook, I rely on my memory to provide that context.
I don't write longer explanations, and I don't know how much I'll remember.
What seemed obvious in 2020 may be baffling in 2030.
Only one way to find out!

[wiki-spinal-tap]: https://en.wikipedia.org/wiki/Up_to_eleven

### The experience of social media

We've looked at the content itself — the posts, the words, the images.
But social media isn't just what’s posted; it’s how we *experience* it.
The interface, interaction design, and the algorithms that shape our feeds are rarely captured in archives.

Consider TikTok and the rise of vertical-swipe video.
Because the next video is just a swipe away, creators structure their content to hook you immediately, and keep your attention throughout.
If you only capture the video file, and not the mechanics of the swipe experience, you miss something about how it was consumed.

Screenshots and screen recordings can preserve a static snapshot, but they can't capture the dynamism of scrolling, swiping, or live interactions.

Even more elusive is the "algorithm", the black box that decide what posts appear in our timeline, when, and to whom.
These algorithms shape culture itself -- amplifying some voices, suppressing others, deciding which ideas can spread -- but their inner workings are deliberately opaque and impossible to archive.

We can preserve the content of social media, but not the experience.
Without the interface and the algorithmic context, the way we encountered and engaged with posts is lost to history.

---

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

You discuss timelines but not the systems behind them.
Algorithms determine:
what you see
when you see it
what gets buried
what trends
Preserving posts isn’t the same as preserving the algorithmic environment.

---

## Rules and responsibility

## Maintaining what you have

1. the flood
    2. the subtext: what’s written between the lines?
      -> most important links are often implicit, not explicit
    3. the veil: veil
    4. the ephemera

the fog
the ethics -> the law -> the self

walled garden -> the feed -> the fog -> the ledger -> the rot/long haul




---


Start with volume — the overwhelming scale of the social-media universe.
This sets the stage: before anything else, you must choose what’s even eligible.
2. The Veil: what about posts that aren't public?
Once you know what exists, confront what you can’t see (privacy, DMs, private groups, paywalls).
This pairs naturally with the flood: the visible sliver versus the hidden whole.
3. The Ephemera: what about disappearing or time-limited content?
A second category of “stuff you can’t rely on seeing,” but for temporal rather than access reasons.
This gives you the two kinds of “unseen” content back to back.
4. The Walled Garden: what if platforms resist preservation?
Moves from content-based visibility to platform-based accessibility.
You now know what exists and what’s visible—this covers what’s technically capturable.
5. The Feed: do you preserve the experience?
Once capture becomes possible, the next question is:
What is the representation?
Algorithmic timelines, UI, interaction.
6. The Fog: how do you find what you've saved?
After capture and representation, move to discovery.
This mirrors archival workflow: ingest → describe → retrieve.
7. The Ethics: do people want to be preserved?
Now shift from technical questions to human ones.
Ethics comes naturally after “fog” because discovery raises questions of exposure and consent.
8. The Law: how does policy shape preservation?
Follow ethics with legal constraints—what you must do regardless of what you want or can do.
9. The Self: who's the person behind the profile?
Identity fits well after ethics + law:
consent depends on identity
context and reliability depend on knowing the speaker
legal obligations can depend on who the subject is
10. The Ledger: can you prove a post is what it claims to be?
Once you know who wrote something, the next issue is whether it’s authentic.
This is a natural deepening of the identity-and-context problem.
11. The Rot: how do you prevent digital decay in your archive?
Now shift from capture/ethics/identity into preservation stability.
Formats, rendering, infrastructure.
12. The Long Haul: how do you keep the archive going?
End with stewardship—budget, staffing, maintenance.
This is the natural closing chapter: the long-term responsibility that outlives all previous decisions.


---



## The Walled Garden: what if platforms resist preservation?

In the early 2000s, many platforms had public APIs.
Twitter is the poster child of this approach -- their API allows a flourishing ecosystem of third-party clients and research projects.

That time is over.
Companies take a dim view of their content being downloaded en masse -- they don't have public APIs, and they aggressively block attempts to scrape or crawl their content.
This has intensified in the era of AI, as companies try to monetise their data for model training.
Preservation tools have been caught in the same net.

This makes institutional archiving difficult.

It's less of an issue in my scrapbook, where I can just enter data by hand.
I prefer to use APIs to save content, but I don't require it -- If I can see a post, I can save it.
But this only works because I'm working at a small scale, and I can accept the small risk of human error in my date entry.
That's a harder sell for institutions.

## The Fog: how do you find what you've saved?

An archive is useless if you can't find what you've saved.
This is often a problem in social media archives: we can save posts at incredible speeds, but we can't search them in any meaningful way.

The default solution is web archiving -- saving each post as a web page, like the Wayback Machine.
This approach scales beautifully for capture, but terribly for discovery.
You can retrieve a post if you know a URL, but not “everything about X” or “posts written by Y”.

Traditional archives solve this with cataloguing: humans write descriptions, and researchers use those to find what they need.
But that model collapses at social media scale: machines can save thousands of posts in the time it takes a human to describe just one.

In my personal scrapbook, I add keyword tags to every conversation.
They're fast, informal, and effective.
If I want something specific, I can filter by tag and find it instantly.
Since I'm the only person who uses these tags, I can define them in a way I like and change them when I decide.
If I was in an institutional context, I'd use a controlled vocabulary like [wiki-LCSH] or [MeSH][wiki-MeSH].

These light-touch keywords feel like a realistic middle ground: human-scale data that's quick to apply, but rich enough to cut through the fog.
This might be the approach that institutions need.

[wiki-LCSH]: https://en.wikipedia.org/wiki/Library_of_Congress_Subject_Headings
[wiki-MeSH]: https://en.wikipedia.org/wiki/Medical_Subject_Headings



## The Ethics: do people want to be preserved?

Web archiving has long ignored consent.
If something is on the public web, most archives consider it eligible for capture -- but preserving a post means it's preserved *forever*.
If somebody posts an embarrassing thought or a personal picture, and it gets sucked into a web archive, it's much harder to remove it from the Internet.

If you asked, I don't think everyone would agree to their posts being preserved forever (even if they're fans of services like the Wayback Machine).
Some would, but others would prefer to retain control over how and when their posts can be seen.
We can see this in the popularity of features like private accounts, closed forums, and disappearing posts.
The era of generative AI and the use of social media for model training has made people even more sensitive to how their data is used.

The general public's attitude to copyright and privacy is pretty laissez-faire.
Many people are happy to download pictures from the Internet, with no regard for the original creator -- but it feels different when it's your data on the line.

A strict ethical stance would require explicit consent from every creator.
Institutions typically govern this with some a donor agreement, where you allow the institution to keep a copy of your material, and sign away the right to remove it afterwards.
This is squeaky clean, but it's hard to scale, and it would exclude orphaned accounts, abandoned platforms, and users who have died or lost their password.
We'd lose huge amounts of historically valuable material.

Web archives have already proved their worth in the preservation of material from companies, politicians, and public figures.
Keeping a permanent record of their statements helps keep them accountable, but they'd never consent to being collected by an archive they don't control.

One idea I'm following is Bluesky's proposal [User Intents for Data Reuse][bsky-proposal], which would allow users to declare how they want their posts to be reused.
For example, you could say whether your posts can be used for generative AI model training, or preserved by a web archive.
Technology alone is not the solution -- you also need an enforcement mechanism so that everyone respects these settings -- but I like the idea of having more granular, per-user preferences.

I feel like the correct approach is something in the middle -- collecting material from public figures is fair game, from private citizens needs explicit consent.
Of course, that's easier said than done, and it would be tricky for institutions to write rules that draw that line.
But the attitude that anything publicly available is okay to archive feels increasingly insensitive and untenable.

In my scrapbook, I'm also ignoring consent.
I feel okay about this because it's private, never shared, and limited to posts I could see at the time.
I feel like it's fine for me to have these posts, but not to share them. 
My guiding rule is "don't be a creep" -- don't save something if it would creep out the original author to know I kept a copy.

[bsky-proposal]: https://github.com/bluesky-social/proposals/blob/main/0008-user-intents/README.md

## The Law: how does policy shape preservation?

Consent is a preference, but legislation is a hard boundary.
Digital collections are affected by a patchwork of laws -- copyright, privacy, data protection rules like the [right to erasure][ico-right-to-erasure], and even content-related restrictions.

In one example, I heard of an archive which had legal trouble after digitising a century-old book that contained photographs now classified as [child sexual abuse material (CSAM)][csam-law].
The digital files were swiftly deleted to comply with the law.
(I'm not sure what happened to the physical copy.)

Institutions must ensure their collections comply with all relevant laws, even if those obligations conflict with the goals of long-term preservation.
Social media archiving faces the same pressure -- often more intensely, because the material is user-generated and fast-moving.

By constrast, my personal scrapbook is entirely private and offline, so it avoids most of these institutional and regulatory constraints.

[ico-right-to-erasure]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/
[dmca]: https://en.wikipedia.org/wiki/Dmca
[csam-law]: https://en.wikipedia.org/wiki/Child_pornography

## The Self: who's the person behind the profile?

Identity on social media is a hard problem.
Many accounts are anonymous or pseudonymous, and most people have accounts scattered across multiple platforms.
This makes it tricky to track somebody's presence on social media, because there's rarely a mapping between a person's legal identity and the accounts they use online.
Often, this anonymity is intentional.

This ambiguity creates a big headache for support teams.
When somebody asks for help regaining access to an account because they've lost the password or been hacked, how can the platform be sure they're the real owner?

Institutions and researchers care about identity because it provides context and authority: *who wrote this, and how much can we trust their words?*
Social media makes this hard, because many usernames don't tell you anything about the person behind them.

My personal scrapbook sidesteps this complexity.
Nearly all of the conversations it contains are with friends I know well, so I can easily connect their identities across different services.

> I can even collapse typo-correction follow-ups into a single cleaned-up note.

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