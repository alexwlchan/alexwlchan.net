---
layout: post
title: Hard problems in social media archiving
summary: Preserving social media is easier said than done. What makes it so difficult for institutions to back up the Internet?
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

In [my previous post][social-media-scrapbook], I wrote about my personal scrapbook of social media posts -- a tiny, private archive where I can save conversations that I care about.
What happens when larger institutions try to preserve social media?

Cultural heritage institutions know the historical importance of social media, and everyone I've worked with understands the urgency -- including when I worked at the [Flickr Foundation][flickr-fdn].
Digital preservation is a well-established field that's developed over decades, but preserving social media presents some unique challenges.

[social-media-scrapbook]: /2025/social-media-scrapbook/
[flickr-fdn]: https://www.flickr.org/

{% table_of_contents %}


---

## What exists and what can be saved

### The scale of social media is overwhelming

Social media exists at a scale that's hard to comprehend: billions of posts, with millions more being added each day.

This makes it difficult for anyone to choose what to preserve, because each person only ever sees a tiny fragment of the whole.
Making a choice inevitably introduces selection bias, and I've spoken to many people who'd like to avoid that bias by "collecting everything" -- but that's far beyond the capacity of any institution.

Since they can't collect everything, institutions create rules -- collection policies that define what's in-scope.
These rules are meant to ensure consistency, fairness, and reduce individual bias, but they force archivists to draw boundaries in a medium that inherently resists them.

Social media isn't a sequence of isolated posts; it's a dense, interconnected graph.
A single post only makes sense in context -- the replies, the people, the topic du jour.
How much of this context do you gather?
How many hops out do you follow?
Do you save the whole thread, every reply, every linked account?
How do you prevent scope creep from sucking in everything?

My personal scrapbook is subjective and inconsistent, because the only audience is me.
My "collection policy" is pure vibes -- I save threads I think are interesting; I keep posts that I find moving; I prune replies that are embarrassing or unhelpful.

Institutions can't be that casual.
They need durable, defensible rules about where their collection starts and ends.
On social media -- where every post is context to a larger tangle of conversation -- drawing that boundary is a major challenge.

### Private and disappearing content

Social media archiving efforts often concentrate on publicly available, long-lasting content, which excludes other types of material -- even though they make up an ever-growing proportion of social media.
Two major categories stand out:

1.  Private social media -- direct messages, private accounts, closed groups, paywalled forums.
2.  Ephemeral features -- content that deliberately disappears or expires. 
    Think Snapchat, Instagram Stories, or one-time messages.

Collecting this material is difficult.
Technically, it's behind authentication walls or interfaces that most web archiving tools can't reach.
Ethically, archivists have to be careful not to violate social norms or user expectations -- many people would be surprised if their private or temporary posts were copied to a public, permanent archive.

It isn't impossible, and I've seen a handful of projects capture private and ephemeral media -- for example, researchers analysing Instagram Stories and their use in political campaigns.
These efforts rely on a patchwork of methods: accessing content through user logins, browser plugins, even taking screenshots.
They tend to be small, targeted, and short-lived.

My scrapbook has a small amount of private content, mostly conversations between me and locked accounts on Twitter.
I'm comfortable with that because I was part of those conversations, and it's a private archive.
I'm not sharing it with anybody else, so I don't think my friends would begrudge me keeping a copy.
I haven't saved any ephemeral content.

Private and ephemeral posts have a different dynamic from public timelines.
People can be more personal, vulnerable, and candid when they know their posts can't be seen by anyone, forever.
Maybe those moments won't appear in social media archives -- but if so, we should acknowledge that limitation, and what stories it leaves out.

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

## Rules, resistance, and responsibility

### What if platforms resist preservation?

In the early 2000s, many platforms were far more supportive of digital preservation.
Public APIs were common, scraping was largely tolerated, and some companies even collaborated with heritage institutions.

Twitter is the poster child.
Their public API allowed a flourishing ecosystem of third-party clients and research projects.
Researchers could easily assemble datasets, and the Library of Congress even attempted to preserve [every public tweet][loc-twitter-project] between 2006 and 2017.
The project stalled and remains largely inaccessible today -- but it would never even get started in 2025.

Today, most platforms resist being preserved, archived, or downloaded en masse.
APIs are restricted or paywalled, rate limits are strict, and scraping is aggressively blocked.
The rise of generative AI has accelerated this trend, as companies realise their data is valuable for model training.
Why give it away for free when you can ask for money?

Reddit is the most recent example.
They [blocked the Internet Archive][reddit-blocks-ia] after AI companies used it to access posts without paying, even as companies like Google pay Reddit [millions for access][reddit-google-deal].

Attempts to preserve content programmatically are increasingly limited, which makes it difficult to archive at scale.
In my scrapbook, I replace APIs with entering data by hand, but that only works if you're saving a small amount of data.

[loc-twitter-project]: https://www.npr.org/sections/thetwo-way/2017/12/26/573609499/library-of-congress-will-no-longer-archive-every-tweet
[reddit-blocks-ia]: https://www.theverge.com/news/757538/reddit-internet-archive-wayback-machine-block-limit
[reddit-google-deal]: https://www.theverge.com/2024/2/22/24080165/google-reddit-ai-training-data

### Do people want to be preserved?

A lot of web archiving has historically ignored consent.
If something is on the public web, many archives consider it eligible for capture -- but preserving a post means it's preserved *forever*.
Embarrassing thought or personal pictures can't be deleted once they've been archived.

Not everyone would agree to their posts being permanently preserved, even if they use services like the Wayback Machine.
We see this in the popularity of private accounts, closed forums, and ephemeral posts -- people want control over how and when their posts are seen.
Generative AI and the use of social media for model training has made people even more sensitive about their data.

The general public often ignores copyright and privacy -- how many people use images they found online with [no regard for the creator][anonymised-art]? -- but institutions hold themselves to a higher standard.

A strict ethical stance would require explicit consent from every creator.
Institutions often use donor agreements, where you allow them to keep your material and sign away the right to remove it afterwards -- but that solution is imperfect.
Donor agreements are hard to scale to social media, where a single conversation may involve dozens of people.

Requiring consent from everybody involved would exclude orphaned accounts, abandoned platforms, and users who have died or lost their password.
And web archives already preserve content from companies, politicians, and public figures, helping keep them accountable -- but these figures would rarely consent to archiving they don't control.
If we took an absolute approach to consent, we'd lose huge amounts of historically valuable material.

One interesting approach is Bluesky's proposal [User Intents for Data Reuse][bsky-proposal], letting users declare how they want their posts to be reused, such as for AI training or archiving.
Technology alone is not the solution -- you also need enforcement -- but this feels like a step in the right direction.

I like the idea of a balanced approach -- collecting material from public figures is fair game; anything from private citizens needs explicit consent.
That's easier said than done, and it's tricky to codify that as a well-defined rule -- but to me, "anything publicly available" feels increasingly insufficient as an ethical guideline.

In my personal scrapbook, I don't have a formal consent process -- something I feel comfortable with because my archive is small, private, and only my own reference.
My guiding rule is "don't be a creep".
I don't save anything I think the original author would be uncomfortable knowing I kept.

[bsky-proposal]: https://github.com/bluesky-social/proposals/blob/main/0008-user-intents/README.md
[anonymised-art]: /2025/anonymised-art/

### Laws and legislation

Consent is a preference, but legislation is a hard boundary.
Digital collections are affected by a patchwork of laws -- copyright, privacy, data protection rules like the [right to erasure][ico-right-to-erasure], and even content-related restrictions.

I heard of one archive which had legal trouble after digitising a century-old book.
They discovered the book had photographs which modern laws classify as [child sexual abuse material (CSAM)][csam-law], and the digital files were swiftly deleted.
(I know the physical book was then scrutinised through the same lens, but I don't recall the outcome.)

Institutions must ensure their collections comply with all relevant laws, even if those obligations conflict with the goals of long-term preservation.
Social media archiving faces the same pressure -- often more intensely, because the material is user-generated and fast-moving.

[ico-right-to-erasure]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/
[dmca]: https://en.wikipedia.org/wiki/Dmca
[csam-law]: https://en.wikipedia.org/wiki/Child_pornography

---

## Understanding what you've saved

### How do you search in your collection?

An archive is useless if you can't find what you've saved.
This is often a problem in social media archives: we can save posts at incredible speeds, but we can't search them in any meaningful way.

A common solution in web archiving is to save page-by-page, one page per post, like the Wayback Machine.
This approach scales beautifully for capture, but terribly for discovery.
You can retrieve a post if you know a URL, but you can't find “everything about X” or “posts written by Y”.

Traditional archives solve this with cataloguing: humans write descriptions, and researchers use those to find what they need.
But that model collapses at social media scale: machines can save thousands of posts in the time it takes a human to describe just one.

In my personal scrapbook, I add keyword tags to every conversation.
They're fast, informal, and effective.
If I want something specific, I can filter by tag and find it instantly.
Since I'm the only person who uses these tags, I can define them in a way I like and change them when I decide.
If I was in an institutional context, I'd use a controlled vocabulary like [LCSH][wiki-LCSH] or [MeSH][wiki-MeSH].

These light-touch keywords feel like a realistic middle ground: human-scale data that's quick to apply, but rich enough to cut through the fog.

[wiki-LCSH]: https://en.wikipedia.org/wiki/Library_of_Congress_Subject_Headings
[wiki-MeSH]: https://en.wikipedia.org/wiki/Medical_Subject_Headings

### Who's the person behind the profile?

Identity on social media is a hard problem.
Many accounts are anonymous or pseudonymous, and most people have accounts scattered across multiple platforms.
This makes it tricky to track somebody's presence on social media, because there's rarely a mapping between a person's legal identity and the accounts they use online.
Often, this anonymity is intentional.

This ambiguity creates a big headache for support teams.
When somebody asks for help regaining access to an account because they've lost the password or been hacked, how can the platform be sure they're the real owner?

Institutions and researchers care about identity because it provides context and authority: *who wrote this, and how much can we trust their words?*
Social media makes this hard, because many usernames don't tell you anything about the person behind them.
Although institutions have tools to connect people across records, it's hard if you don't know who the person is!

My personal scrapbook sidesteps this complexity.
Nearly all of the conversations it contains are with friends I know well, so I can easily connect their identities across different services.

### Implicit knowledge, cultural context, and memes

Social media relies on shared knowledge: current events, in-jokes, and memes.
Without this context, the meaning of a post can fade -- or an entirely new meaning can take its place.

It's impossible to preserve all this background information.
People rarely link to the thing they're referring to; they rely on their audience to already know.
A key part of any creative work is deciding how much to explain and how much to leave implied.
Sometimes it's a tiny in-joke for a handful of fans, other times it's essential to understanding the point.

This isn't a new problem -- all human communication requires context -- but social media [takes it to eleven][wiki-spinal-tap].
The pace and brevity are a fertile breeding ground for memes whose origins disappear almost immediately.
Log off for a day, and you'll return to posts that make no sense at all.
You missed the moment that sparked the meme.
Imagine how much harder it is to understand if you arrive years -- or decades -- later.

You can try to fill in the gap with catalogue descriptions, but that's only possible if somebody understands the references well enough to describe them.
With social media's scale and speed, it's impossible for anybody to know all the jokes, memes, and ideas that might affect a post.

In my personal scrapbook, I rely on my memory to provide that context.
I don't write longer explanations, and I don't know how much I'll remember.
What seemed obvious in 2020 may be baffling in 2030.
Only one way to find out!

[wiki-spinal-tap]: https://en.wikipedia.org/wiki/Up_to_eleven

---

## We won't save everything, but we can save something

Perhaps we can't preserve social media perfectly, but that doesn't mean we shouldn't try.
Every archive ever assembled is incomplete, but they still have immense value. 
Capturing public posts, threads, or conversations -- even if we lose some of the context or ephemeral content -- helps preserve a record of cultural history that could otherwise be lost. 

What excites me is the small, ad-hoc projects happening everywhere.
I see lots of people building tools to save tiny corners of the web -- posts from a single account, fanworks from a tight-knit community, or shared advice from a community wiki.
Whenever a platform disappears or looks shaky, there's a renewed interest to minimise the loss.

Grassroots efforts can reach areas that larger institutions can't, and institutional archives provide scale, stability, and long-term preservation.
Both are vital to capturing social media's history.

Social media archiving will never be perfect, but it's possible.
I think there's a lot of potential, and I'm excited to see how institutions rise to the challenge.
