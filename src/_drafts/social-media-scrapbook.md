---
layout: post
title: The Internet forgets, but I don't want to
summary: I don't trust platforms to preserve my memories, so I built my own scrapbook of social media. 
tags:
  - digital preservation
  - social media
  - static sites
index:
  feature: true
colors:
  index_light: "#293d56"
  index_dark:  "#41a5ed"
---
{% table_of_contents %}

I grew up alongside social media, as it was changing from nerd curiosity to mainstream culture.
I joined Twitter and Tumblr in the early 2010s, and I stayed there for over a decade.
Those spaces shaped my adult life: I met friends and partners, found a career in cultural heritage, and discovered my queer identity.

That impact will last a long time.
The posts themselves?
Not so much.

Social media is fragile, and it can disappear quickly.
Sites get [sold][musk-buys-twitter], [shut down][cohost-closes] or [blocked][bbc-imgur].
People close their accounts or flee the Internet.
Posts get [deleted][deleted-my-tweets], [censored][lj-strikethrough] or [lost][bbc-myspace] by platforms that don't care about permanence.
We live in an era of abundant technology and digital storage, but the everyday record of our lives is disappearing before our eyes.

I want to remember social media, and not just as a vague memory.
I want to remember exactly what I read, what I saw, what I wrote.
If I was born 50 years ago, I'd have a scrapbook full of letters and postcards -- physical traces of the people who mattered to me.
(I'm lucky enough to have a few of those even today, but they're the exception, not the rule.)

I don't trust the Internet to remember for me, so I've built my own scrapbook of social media.
It's a place where I can save the posts that shaped me, delighted me, or just stuck in my mind.

<figure>
  {%
    picture
    filename="social-media-scrapbook.png"
    width="750"
    class="screenshot"
  %}
  <figcaption>
    Each conversation appears as a little card, almost like a clipping from a magazine or newspaper.
    Most of my conversations are from Twitter, but I also have sites like Tumblr, YouTube, and Bluesky.
  </figcaption>
</figure>

It's a static site where I can save conversations from different services, enjoy them in my web browser, and search them using my own tags.
It already feels more permanent than many social media sites.
This post is the first in a three-part series about how I built this scrapbook, and what I learned along the way.

[bbc-imgur]: https://www.bbc.co.uk/news/articles/c4gzxv5gy3qo
[bbc-myspace]: https://www.bbc.co.uk/news/technology-47610936
[lj-strikethrough]: https://www.theverge.com/2018/12/6/18127869/tumblr-livejournal-porn-ban-strikethrough
[cohost-closes]: https://web.archive.org/web/20240909195207/https://cohost.org/staff/post/7611443-cohost-to-shut-down
[musk-buys-twitter]: https://arstechnica.com/tech-policy/2022/10/elon-musk-completes-twitter-purchase-immediately-fires-ceo-and-other-execs/
[deleted-my-tweets]: /2024/i-deleted-all-my-tweets/

---

## The long road to a lasting archive

Long before I knew the phrase "digital preservation", I knew I wanted to keep my social media.
I wrote little scripts to capture my conversations and stash them away on storage I controlled.

Those scripts worked, technically, but the end result was a mess.
I focusing on saving data, while organisation and presentation were an afterthought.
I was left with folders full of JSON and XML files -- archives I couldn't actually use, let along search or revisit with any joy.

I've tried to solve this problem more times than I can count.
I have screenshots of at least a dozen different attempts, and there are probably just as many I've forgotten.

For the first time, though, I think I have a sustainable solution.
I can store conversations, and find it later, and the tech stack is simple enough that it's unlikely to break any time soon.
Saying something will last is always hubristic, especially when software is involved, but I have a good feeling about this attempt.

Looking back, I realise my previous attempts failed because I focused too much on my tools.
I kept thinking that if I just picked the right language, or found a better framework, or wrote cleaner code, I'd finally land on a permanent solution.
The software does matter -- and a static site will certainly outlive my hacky Python web apps -- but other things are more important.

What I really needed was a good data model.
Every earlier version started with a small schema that could hold simple conversations, which worked until I tried to save something more complicated.
Whenever that happened, I'd try to make a quick fix, thinking about the specific issue rather than the data model as a whole.
Too many one-off changes and everything becomes a tangled mess, which is usually when I'd start the next rewrite.

This time, I thought more carefully about the shape of the data.
What's worth storing, and what's the best way to store it?
I built better tools for cleaning, validating, and refining my data.
More than any language or framework choice, I think this is what will finally give this project some sticking power.

[xkcd-927]: https://xkcd.com/927/

---

## How it works

I'm not planning to share code, because it's difficult to extricate from my saved data, but I do want to share some broad ideas.

### A static site, viewed in the browser

Static sites give me a lightweight, flexible way to store and present my data, in a format that's widely supported and likely to remain usable for a long time.
I store metadata in a machine-readable JSON/JavaScript file, and view it as a website that I can open in the browser.

This is a topic I've [written about at length][static-sites], including a [detailed explanation][static-sites-code] of my code.

[static-sites]: /2024/static-websites/
[static-sites-code]: /2025/mildly-dynamic-websites/

### Conversations as the unit of storage

Many posts don't stand alone, but are part of a longer conversation.
You need that conversation and context to understand the post, or it doesn't make sense later.
Reading a tweet where I said "that's a great idea!" is pointless unless you know what I was replying to!

This is a particular problem with the exports, which typically only contain my posts, but not anybody else's.

Within my scrapbook, the unit of storage is a *conversation* -- a set of one or more posts that form a single thread.
If I save one post in a conversation, I save them all, so I preserve that context.
This is different to many other social media archives, which save one post at a time, and may only capture part of a conversation.

Working on this project, I finally understand why so many handwritten letters start by recapping the previous letter.
Especially in the past, the person you're writing to is unlikely to have a copy of the last letter they sent to you, so you need to remind them of what you're replying to.

### A different data model and renderer for each site

A big mistake I made with my data model in the past was trying to shoehorn data from different sites into the same schema.
This can go one of two ways: either you end up with an overly reductive model that over-simpfifies your data, or you get an overly generic model with lots of fields, only a few of which are used in each item.

But different sites are different.
Twitter and other microblogging services are short fragments of text in a long thread, sometimes with media attached.
Tumblr posts are heavier, with more media and HTML formatting.
On Flickr the photo is the star, with some ancillary metadata to add extra context.
It's tricky to create a data model that can store a tweet and a Tumblr post and a Flickr picture and the dozen other sites I want to support.

For this project, I've created a different data model for each site I want to save.
I've tried to keep it fairly simple, small enough that I can fill in all the fields by hand without it being arduous.
That means I can store precisely the data I want to keep about each site, and not have to decide how to shove site-specific data in a generic field, or leave the model with a bunch of unfilled fields.
I store all the data as JSON, which is easy to edit by hand.

Here's a snippet from one conversation I've saved: a thread from Twitter, where I saved one of my tweets and the replies.
There's a bit of generic metadata at the top (`meta`), then the `body` array contains the tweets in the thread.
The `meta` is the same for every conversation; the contents of `body` varies by site.

```json
{
  "site": "twitter",
  "id": "1574527222374977559",
  "meta": {
    "tags": ["trans joy", "gender euphoria"],
    "date_saved": "2025-10-31T07:31:01Z",
    "url": "https://www.twitter.com/alexwlchan/status/1574527222374977559"
  },
  "body": [
    {
      "id": "1574527222374977559",
      "author": "alexwlchan",
      "text": "prepping for bed, I glanced in a mirror\n\nand i was struck by an overwhelming sense of feeling beautiful\n\njust from the angle of my face and the way my hair fell around over it\n\ni hope i never stop appreciating the sense of body confidence and comfort i got from Transition 🥰",
      "date_posted": "2022-09-26T22:31:57Z"
    },
    {
      "id": "1574527342470483970",
      "author": "oldenoughtosay",
      "text": "@alexwlchan you ARE beautiful!!",
      "date_posted": "2022-09-26T22:32:26Z",
      "entities": {
          "hashtags": [],
          "media": [],
          "urls": [],
          "user_mentions": ["alexwlchan"]
        },
        "in_reply_to": {
          "id": "1574527222374977559",
          "user": "alexwlchan"
        }
      }
    }
  ]
}
```

One advantage of spending over a decade thinking about this is that I know exactly what fields I care about and what I don't.
For example, many social media websites provide metrics -- how many times was a post viewed, or starred, or retweeted.
I don't keep any of of those because those metrics aren't something I'm interested in.
I remember posts because they were fun, thoughtful, or interesting, not because they had a particularly notable metric.

I try to reuse data structures where appropriate -- for example, the `meta` block is common to every site, and I use the same data structure for all the microblogging services I save (Twitter, Mastodon, Bluesky, Threads) -- and I have a common data structure for media files like images and videos -- but each site has a slightly different structure.

Each data model is accompanied by a rendering function, which reads this data and returns a snippet of HTML that can appear in one of the "cards" in my web browser.
I have a long switch statement that just picks the right rendering function, something like:

{% code lang="javascript" names="0:renderConversation 1:props 4:renderFlickrPicture 6:renderTwitterThread 8:renderYouTubeVideo" %}
function renderConversation(props) {
    switch(props.site) {
        case 'flickr':
            return renderFlickrPicture(props);
        case 'twitter':
            return renderTwitterThread(props);
        case 'youtube':
            return renderYouTubeVideo(props);
        …
    }
}
{% endcode %}

As well as a data model for each site, I have a "generic media" data model where I can save images downloaded from arbitrary URLs.
Previously this generic model was my only data model, and everything was based around images -- now it's just a small subset.

### Keyword tagging on every conversation

I tag everything with keywords as I save it.
If I'm looking for a conversation later, I remember what tags I would have used, and filter for those.
These tags make it much easier for me to find old posts, and allows me to add my own interpretation.

This is much easier than doing full text search, because I can look for a consistent set of terms.
Social media posts don't always mention their topic in a consistent, easy-to-search for phrase -- either because it just didn't fit into the wording, or because they're deliberately keeping it as subtext.
For example, not all cat pictures [include the word "cat"][tw-miette], but I tag them all with "cats" so I can find them later.

I use [fuzzy string matching][fuzzy-tags] to find and fix mistyped tags.

[tw-miette]: https://x.com/supergirl_sass/status/1392589896116699137
[fuzzy-tags]: /2020/using-fuzzy-string-matching-to-find-duplicate-tags/

### Metadata in JSON/JavaScript, interpreted as a graph

Here's a quick sketch of how my data is laid out on disk:

```
scrapbook/
 ├─ avatars/
 ├─ media/
 │   ├─ a/
 │   └─ b/
 │      └─ bananas.jpg
 ├─ posts.js
 └─ users.js
```

All of my post data is in `posts.js`, which contains objects like the Twitter example above.
Each conversation is completely self-contained -- posts can refer to each other within a single conversation, but there's no link to posts in other conversations.
e.g. a tweet can refer to a previous tweet in a thread, but not to tweets in other conversations.
This keeps the logic simpler.

Through the `author` field, this points to entries in `users.js`.
My user model is pretty light -- the path of an avatar image in `avatars/`, and maybe a display name if the site supports it.

Currently users are split by site -- I have no way to record that `@alexwlchan` on Twitter and `@alex@alexwlchan.net` on Mastodon are the same person, for example.
That'd be a nice future upgrade.

Posts can also refer to media files, which I store in the `media/` and organise by the first letter of their filename -- this keeps the number of files in each subdirectory more manageable.

This metadata forms a little graph:

```
flowchart LR
    P[posts.js] --> U[users.js]
    P --> M[media files]
    U --> A[avatar files]
```

And I have tests that check the graph is consistent -- every user referred to in `posts.js` has an entry in `users.js`, every media file described in `posts.js` is saved on disk, and every avatar file described in `users.js` is saved to disk.

### A large suite of tests

I have a test suite written in Python and [pytest][pytest] that checks the consistency and correctness of my metadata.
This includes things like:

*   My metadata files match the data model I've defined
*   Every media file described in the metadata is saved on disk, and every media file saved on disk is described in the metadata.
*   I have a profile image for the author of every post that I've saved
*   Every timestamp uses [a consistent format][test-timestamp]
*   None of my videos are [encoded in AV1][test-av1] (which can't play on my iPhone)

I'm editing a lot of metadata by hand, and these tests give me a safety net against issues in my data.
They're quick to run, so I run them every time I make a change, which means I catch errors early.

[pytest]: https://docs.pytest.org/en/stable/
[test-av1]: /2025/detecting-av1-videos/
[test-timestamp]: /2025/messy-dates-in-json/

---

## Inspirations and ideas

When I look at this project, I can see all the places where the ideas came from.
These are the influences that helped me get to the current design.

### Static website in Twitter archive

Pretty much every social media website gives you a way to download your data, but some downloads are better than others.
On some sites it's obviously offered reluctantly -- a zip archive full of JSON files, with minimal documentation or explanation.
Enough to comply with data export laws, but nothing more than that.

Twitter's archive was much better than that.
When you've downloaded your archive, the first thing you saw was an HTML file called `Your archive.html`.
Opening this would launch a static website where you could browse your data, including full-text search for your tweets:

<style>
  #twitter_archive {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: var(--grid-gap);
  }

  #twitter_archive a:nth-child(1) img {
    border-top-right-radius:    0;
    border-bottom-right-radius: 0;
  },

  #twitter_archive a:nth-child(2) img {
    border-top-left-radius:    0;
    border-bottom-left-radius: 0;
  }
  
  #twitter_archive figcaption {
    grid-column: 1 / span 2;
  }
</style>

<figure id="twitter_archive">
  {%
    picture
    filename="twitter_archive1.png"
    width="375"
    class="screenshot"
    link_to_original
  %}
  {%
    picture
    filename="twitter_archive2.png"
    width="375"
    class="screenshot"
    link_to_original
  %}
  <figcaption>
    Fun fact: although Elon Musk has <a href="https://www.theverge.com/2023/7/23/23804629/twitters-rebrand-to-x-may-actually-be-happening-soon">rebranded Twitter as X</a>, you still get the Twitter name and iconography in newly-downloaded archives. 
  </figcaption>
</figure>

This approach was a big inspiration for me, and put me on the path of [using static websites for tiny archives][static-sites].
It's a remarkably robust piece of engineering, and I wouldn't be surprised if these archives are among the longest lasting pieces of Twitter. 

The Twitter archive isn't exactly what I want, because it only has my tweets.
My best memories of Twitter are long-running back-and-forth conversations with my friends, and my personal archive only contains my side of the conversation. 
In my scrapbook, I can capture both people's contributions.

### Data Lifeboat at the Flickr Foundation

I worked for the [Flickr Foundation][flickr-foundation] for nearly two years, including the [Data Lifeboat][flickr-dl] project, which focused on archiving slivers of Flickr.
I joined because of my interest in archiving social media, and the ideas flowed in both directions: personal experiments informed my work, and vice versa.

Data Lifeboat collects more metadata than my scrapbook and aims to be usable by anyone, whereas my scrapbook collects data from a much wider collection of services and only needs to be usable by me.
But the underlying principle is the same: preserve social media in a lasting format.

One of my favourite parts of that work was pushing the concept of a [static website for tiny archives][static-sites] further than I ever have before.
Each Data Lifeboat package includes a viewer app, which is a static website built in vanilla JavaScript, and it's the most complex such viewer I've built to date.
I even wrote a test suite using [Playwright][playwright], because it grew past what I could test by hand.

That experience has made me more ambitious about what I can do with static, self-contained sites.

[flickr-foundation]: https://www.flickr.org
[flickr-dl]: https://www.flickr.org/programs/content-mobility/data-lifeboat/
[static-sites]: /2024/static-websites/
[playwright]: https://playwright.dev/

### My bookmarks

Earlier this year I wrote about [my bookmarks collection][bookmarks], which I also store in a static site.
The scrapbook is very similar: same underlying idea, different data.

My bookmarks are mostly long-form prose and video -- reference material with private notes.
The scrapbook is more short-form content, often with visual media, often with conversations I was a part of.
Both give me searchable, durable copies of things I don't want to lose.

I built my own bookmarks site because I didn't trust a bookmarking service to last; I built my social media scrapbook because I don't trust social media platforms to stick around.
They're two different manifestations of the same idea.

[bookmarks]: /2025/bookmarks-static-site/

### Tapestry, by the Iconfactory

[Tapestry][tapestry] is an iPhone app that combines posts from multiple platforms -- social media, RSS feeds, blogs -- into a single unified timeline.
The app pulls in content using site-specific ["connectors"][tapestry-connectors], written with basic web technologies like JavaScript and JSON.

{%
  picture
  filename="tapestry.png"
  width="375"
  class="screenshot"
%}

Although I don't use Tapestry myself, I was really struck by the idea of connectors.
The idea that each site gets its own bit of logic is what pushed me towards having a separate data model per service, rather than writing a giant structure that tries to include everything.
That decision has made my scrapbook more robust, and it's become much easier to add new sites.

[tapestry]: https://usetapestry.com/
[tapestry-connectors]: https://usetapestry.com/connectors/
[talk-show-418]: https://daringfireball.net/thetalkshow/2025/03/08/ep-418

### Social media embeds on this site

When I embed social media posts in my posts, I don't use the native embeds offered by platforms, which pull in megabytes of of JavaScript and tracking.
Instead, I use [lightweight HTML snippets][good-embedded-toots] styled with my own CSS, an idea I first saw from Dr Drang [over thirteen years ago][good-embedded-tweets].

The visual appearance of these snippets isn't a perfect match for the original site, but they're close enough to be usable.
The CSS and HTML templates were a good starting point for my scrapbook.

[good-embedded-toots]: /2025/good-embedded-toots/
[good-embedded-tweets]: https://leancrew.com/all-this/2012/07/good-embedded-tweets/

---

## You can make your own scrapbook, too

If there’s something online you don’t want to lose, save your own copy.
Start with whatever's easiest -- a screenshot, a text file, a printout.
It doesn’t have to be perfect; it just has to exist somewhere you control.

Your archive won't look like mine, and that's okay.
Build something that fits the way *you* remember: a folder, a notebook, a journal, anything that helps you keep the moments that matter.
Use this post as inspiration, not a rigid template.

The Internet forgets, but it doesn't have to take your memories with it.
