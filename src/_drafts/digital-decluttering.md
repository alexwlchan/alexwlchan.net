---
layout: post
title: Digital decluttering
summary:
tags:
  - personal
  - digital-preservation
---
<!-- 1744 words -->

I spent a lot of my formative Internet years in online fandom.
I read novel-length stories about *Doctor Who* characters; I swooned over fan art of the *Lizzie Bennet Diaries*; I pored over in-depth analyses of each episode of *Carmilla*.

Most of that is gone now.

Links rot at an extraordinary rate, and much of that early-2010s fan culture has vanished from the Internet.
Accounts get deleted, websites go down, domain names lapse.
Every fan learns that if there's something you love, you can't rely on the Internet to keep it safe.
You have to save your own copy.

So I started saving, and I kept saving.
Digital storage was cheap and abundant, and I could afford to keep local copies of *everything*.
I didn't have to be picky with what I was saving.

I kept every photo I'd ever taken, every tweet I'd written, every link I'd read.
If you look at early posts on this site or my old GitHub repos, you'll see my excitement at code that could scrape down data and squirrel it away on my hard drive.
I always thought "what if I want to go back to this someday?"

This was excessive.
I could throw away 95% of this data and I'd be fine.
There are some things that I'm glad I saved, but there's an awful lot of other stuff that I don't actually care about.
I've never gone back to it, and I know I'm never going to look at it again.

It was also disorganised.
I was more interested in making sure I had a file, and not in whether I could find the file later.
These files were stored in a messy collection of folders, and it's difficult to find that 5% I actually care about.

I'm trying to simplify, and reduce the amount of data I keep.

As I save new stuff today, I'm trying to be more intentional about what I keep.
Before I save something, I ask myself "when will you want to look at this again?"
If I can't imagine a scenario in which I'd be glad to have saved this particular thing, I don't save it.
I've been collecting for fifteen years, and I know what sort of stuff I go back to.
Heartfelt stories and in-depth essays? Yes.
Current affairs and political news? Not so much.

If I decide to save something, I make sure to add a brief description and notes on why I thought it was worth saving, and organise it properly so I can find it later.
I'm saving less stuff, but it's all the stuff I really love.

I've been retroactively applying similar rules to old stuff -- what have I thought about since I saved it?
I've been gradually going through all my old data, deleting what I don't want and organising what I do.
It's a slow and arduous process, because there's no easy way to automate this -- ultimately, I have to look at every item and decide if it's worth keeping.

Storage is only cheap at the point of purchase – the costs are felt elsewhere.
The material used to make hard drives; the electricity and water to power the cloud data centres; the cognitive load of owning so much stuff.
I don't think it's sustainable for me to have such a fast-growing pile of data.
I'm feeling the effects of unsustainable choices made by my younger self.

Modern storage has made it possible for me to keep everything, but that doesn't mean I should.
"As much as I can save" isn't a collecting strategy; it's hoarding.

---

## Three examples of digital clutter

It took me years to accumulate my data, so I'm not going to clear it in a day.
I've spent months chipping away at it, reviewing a few items at a time, and there's plenty more to go.

Let's look at a few examples of what I'm been deleting.

### 1. My photo library

I used to keep every photo I'd ever taken.
I was snapping away on my smartphone, and uploading everything to iCloud Photo Library and my local hard drive.

Some of those photos record precious memories, and I'm so glad that I have them.
But a lot of them are complete junk -- blurry shots, duplicate pictures, long-passed reminders of something I had to do.
(I had *so* many photos of books I wanted to read.)

The bad photos were drowning out the good ones, so I've been deleting them.
I wrote a [small Mac app][blink] to go through every photo in my camera roll, and decide what to keep.

The photos of places and objects were easy to review.
If I didn't recognise the subject, I deleted it.
I got rid of a lot of generic landscapes and builings that I've just forgotten in the intervening years.

The photos of people were harder.
I was reminded of fond memories; I could see how much I've grown; I can see how much happier I became after I transitioned.
But I was also embarrassed by the cringe things I did as a teenager, and reminded of the mistakes I've made as an adult.
There are dear friends in those photos I haven't spoken to in years.
We didn't fall out; our lives just drifted apart and we fell out of touch.
It hurt to see all the good people I've let slip out of my life.

Reviewing my old photos wasn't easy, and some days I could only look at a few at a time.

It took eleven months to look at everything, and I've cut my library from 32,000 photos to 25,000.
That still feels like a lot -- more than 2 photos for every day I've been alive -- but it's an improvement.

I'm thinking about ways to prune further, or highlight the photos I actually care about -- like putting them on my walls, or making some printed albums.
I want to do more here.

[blink]: /2023/blink/

### 2. My podcast collection

I used to keep every podcast episode I'd ever listened to.

I can trace this behaviour to a specific podcast called *IRL Talk*, which I listened to around 2012.
It came at a formative moment in my life, and it's associated with some very fond memories -- but it disappeared from the Internet after one of the hosts passed away.
I was sad when I couldn't listen to it any more, and delighted when somebody uploaded the entire run to the Internet Archive.

To avoid ever losing a podcast again, I wrote a Python script that would download every episode I played.
I could get a complete list of episodes from my podcast app, and it was easy to parse that list and shove the files in a folder.

But I never actually looked in the folder.
I was accumulating thousands of MP3 files, but most of them were episodes I didn't want to listen to again -- once was plenty.
A lot of podcasts I subscribe to are very timely -- tech news or politics, which is interesting in the moment but quickly drops off in value.
When there was an episode I wanted to go back to, it was easier to find it on the web than in my local archive.

I threw the whole thing away, and built a new archive which is much more selective.
It only contains a hundred or so episodes, and it's just my favourites -- the episodes I've already listened to multiple times.
These are the files I know I'll want to go back to in future.

### 3. My bundle of bookmarks

I've saved a lot of links, but I'm not going to read all of them again.
News articles; outdated reference material; fics I don't want to re-read -- I saved them because it was so easy to create bookmarks, but I've never gone back to them.

I'm going through my bookmarks, reducing it to a more focused collection.
What's the stuff I actually want to remember?

As I remove the bookmarks I don't care about, I've been improving the ones I want to keep.
I'm adding proper descriptions and summaries, so I know why a link is important and worth keeping.
This is a useful litmus test -- if I don't care enough to write this small amount of metadata, it's probably not that important.

I'm also fixing the local backups of each bookmark.
I pay for Pinboard's archiving service, which is meant to create a backup of every bookmark -- but maybe a third of those backups are unusable.
There are broken pages, 404 errors, paywalls and login screens.
This is the risk of bulk, automated scraping of the web -- nobody is checking whether the scraped page is actually useful.
As I decide which bookmarks to keep, I'm manually checking the backup version and replacing it if it's broken.
This takes longer, but now I know that all my archived web pages are useful copies, and not dead weight.

These two steps add more friction to the process, but I think that's a good thing.
It's slowing me down, and making me more thoughtful about what I save -- do I really want to save this link for later, or am I just saving it for the sake of saving it?

---

## Reflections

I've substantially reduced my digital footprint.
My data used to be split across my internal disk and multiple external hard drives, and now I can consolidate all my data back onto my internal disk -- much simpler.

The data I'm keeping is much better organised, so it's easier to find stuff I care about.
And the improved metadata has paid off in unexpected ways -- for example, I can give better recommendations.
When somebody asks me for links about a topic, or photos from a trip, it's easier to find the stuff that's worth sharing.

I have to be careful.
Refining data is a boundless task -- there's always more you could do.
It would be easy to let my hyperfocus take over and spend all my time on this, but that would be a mistake.
I've been doing this slowly, taking a few minutes at a time.

This digital decluttering is part of a broader goal to be more intentional about how I use technology, and I've found it useful to introduce some constraints.
I'm not buying the most powerful computer, or the fastest Internet connection, or the biggest disk -- I'm reducing my scope, and that makes it easier to ignore the clutter and focus on what's really important.
