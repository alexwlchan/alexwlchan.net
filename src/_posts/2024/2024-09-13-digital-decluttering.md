---
layout: post
date: 2024-09-13 17:38:59 +0000
title: Digital decluttering
summary: I'm resisting my temptation towards digital hoarding and "save everything", and trying to be more selective about the data I'm keeping.
tags:
  - personal
  - digital preservation
colors:
  css_dark:  "#8ec0e6"
  css_light: "#3351a3"
is_featured: true
---
{% comment %}
  Cover image from https://www.pexels.com/photo/gray-and-yellow-gravel-stones-997704/
{% endcomment %}

I spent a lot of my formative Internet years in online fandom.
I read novel-length stories about *Doctor Who* characters; I swooned over fan art of the *Lizzie Bennet Diaries*; I pored over in-depth analyses of each episode of *Carmilla*.

Most of that is gone now.

Links rot quickly, and much of that early-2010s fan culture has vanished from the Internet.
Accounts get deleted, websites go down, domain names expire.
Every fan learns that if there's something you love, you can't rely on the Internet to keep it safe.
You have to save your own copy.

So I started saving, and I kept saving.
Digital storage was cheap and abundant, and I could afford to keep local copies of *everything*.
I didn't have to be picky with what I was saving.

I kept every photo I'd taken, every tweet I'd written, every link I'd read.
If you look at my early posts or my old GitHub repos, you'll see my excitement at code that could scrape down data and squirrel it away on my hard drive.
I always thought "what if I want to go back to this someday?"

In hindsight, I was being excessive.
I could throw away 95% of this data and I'd be fine.
There are some things that I'm glad I saved, but there's an awful lot of other stuff that I don't actually care about.
I've never gone back to it, and I know I'm not going to look at it again.

I was also disorganised.
I was more interested in making sure I had a copy of each file *somewhere*, and less so whether I could actually find it.
My files were stored in a messy collection of folders, and it was difficult to find that 5% I actually care about.

I want to simplify, and store less data.

As I save new stuff today, I'm trying to be more intentional and selective.
I ask myself "when will you want to look at this again?"
If I can't imagine a scenario in which I'd be glad to have saved this particular thing, I don't save it.
I've been collecting for fifteen years, and I know what I go back to.
Heartfelt stories and in-depth essays? Yes.
Current affairs and political news? Not so much.

If I decide to save something, I make sure to write a brief description and notes on why I thought it was worth saving, and to organise it properly so I can find it later.
I'm saving less stuff, but it's all the stuff I really love, and I can find it when I want to.

I've been retroactively applying similar rules to old stuff -- what have I thought about since I saved it, and what have I completely forgotten?
I've been going through all my old data, deleting what I don't want and organising what I do.
It's a slow and arduous process, because there's no easy way to automate it -- ultimately, I have to look at every item and decide if it's worth keeping.

Storage is only cheap at the point of purchase – the costs are felt elsewhere.
The material used to make hard drives; the electricity and water to power the cloud data centres; the cognitive load of owning so much stuff.
I don't think it's sustainable for me to have such a fast-growing pile of data.
I'm feeling the questionable choices made by my younger self.

Modern storage has made it possible for me to keep everything, but that doesn't mean I should.
"As much as I can get" isn't a collecting strategy; it's hoarding.

---

## Three examples of digital clutter

It took me years to accumulate my data, so I'm not going to clear it in a day.
I've already spent months chipping away at it, and there's plenty still to go.

Let's look at a few examples of what I've been tidying.

### 1. My photo library

I used to keep every photo I took.
I was snapping away on my phone, and uploading everything to iCloud Photo Library and my local hard drive.

Some of those photos record precious memories, and I'm so glad that I have them.
But a lot of them are complete junk -- blurry shots, duplicate pictures, long-passed reminders of something I had to do.
(I had *so* many photos of books I wanted to read.)

The bad photos were drowning out the good ones, so I've been deleting them.
I wrote a [small Mac app][blink] to go through every photo in my camera roll, and help me choose what to keep.

Photos of places and objects were easy to review.
If I didn't recognise the subject, I deleted it.
I binned a lot of generic landscapes and builings that I've forgotten in the intervening years.

The photos of people were harder.
I could see special moments, how much I've grown, and how much happier I became after I transitioned.
But I was also embarrassed by the cringe things I did as a teenager, and reminded of the mistakes I've made as an adult.
There are dear friends in those photos I haven't spoken to in years.
We didn't fall out; our lives just drifted apart and we fell out of touch.
It hurt to see all the good people who are no longer in my life.

It took eleven months to go through everything, and I've trimmed my library from 32,000 photos to 25,000.
That still feels like a big number -- more than 2 photos for every day I've been alive -- but it's an improvement.

I'm thinking about ways to be even more selective, and how to highlight the photos I actually care about -- like putting them on my walls, or making some printed albums.
I want to do more here.

[blink]: /2023/blink/

### 2. My podcast collection

I used to keep every podcast episode I listened to.

I can trace this behaviour to a specific podcast called *IRL Talk*, which I listened to around 2012.
It came at a formative moment in my life, and it's associated with some fond memories -- but it disappeared from the Internet after one of the hosts passed away.
I was sad when I couldn't listen to it any more, and delighted when somebody uploaded the entire run [to the Internet Archive][irltalk].

To avoid ever losing a podcast again, I wrote a Python script that would download every episode I played.
I could get a complete list of those episodes from my podcast app, and it was easy to parse that list and shove the files in a folder.

But I never actually looked in the folder.
A lot of podcasts I subscribe to are very timely, like tech news and politics -- interesting in the moment, but I rarely listen more than once.
I had thousands of MP3 files, but there weren't many I wanted to listen to again.
When I did want to go back to an episode, it was easier to find it again on the web than look in my local archive.

I threw the folder away, and built a new archive which is much more selective.
It only contains a hundred or so episodes, and it's just my favourites -- the timeless episodes I've already listened to multiple times.
These are the files I know I'll want to go back to in future.

[irltalk]: https://archive.org/details/irl-talk-podcast

### 3. My bookmark archive

I've saved a lot of links, but I'm not going to read all of them again.
News articles; outdated reference material; fics I don't want to re-read -- I saved them because it was so easy to create bookmarks, but I've never gone back to them.

I'm going through my bookmarks, reducing it to a more focused collection.
What's the stuff I actually want to remember?
Like podcasts, I'm mostly keeping stuff I've already looked back on.
I'm saving evergreen writing that doesn't go out of date, and web pages which have lodged themselves in my memory.

As I go, I've been improving the metadata of bookmarks I decide to keep.
I'm adding proper descriptions and summaries, so I know what a link contains and why it's worth keeping.
This is a useful litmus test -- if I don't care enough to write this small amount of metadata, it's probably not that important.

I'm also checking my backups.
Between my own scripts and [Pinboard's archiving service][archiving], I should have an offline copy of each bookmark, in case the original goes down.
In practice, about a third of those backups are unusable -- what's saved is broken pages, 404 errors, paywalls and login screens.
This is the risk of bulk, automated scraping of the web -- nobody is checking whether the scraped page is actually useful.
I've been checking each offline copy, and replacing it if it's broken.
It'll take longer, but eventually I'll know that all of those files are useful backups, and not dead weight.

These two steps add more friction to the process, but I think that's a good thing.
It's slowing me down, and making me more thoughtful about what I save -- will I really want to read this link later, or am I just saving it for the sake of saving it?

[archiving]: https://pinboard.in/faq/#archiving

---

I've significantly shrunk my digital footprint.
My data used to be split across my internal disk and multiple external hard drives, and now it fits on my internal disk -- much simpler.
And the data I'm keeping is better organised, so I can actually find stuff I care about.

I have to be a bit careful.
Refining data is a boundless task -- there's always more you could do.
I don't want to let my [hyperfocus] take over and make this the only thing I do.
I've been doing it slowly, only taking a few minutes at a time.

This digital decluttering is part of a broader goal to be more intentional about how I use technology, and I've found it useful to introduce some constraints.
I'm not buying the most powerful computer, or the fastest Internet connection, or the biggest disk -- I'm adding deliberate limits, and that helps me stay focused on what's really important.

[hyperfocus]: https://wellcomecollection.org/articles/ZRrH3RIAACIAALP5
