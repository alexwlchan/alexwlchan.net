---
layout: post
title: Digital decluttering
summary:
tags:
  - personal
  - digital-preservation
---
I spent a lot of my formative Internet years in online fandom, where I was surrounded by the creativity of strangers.
I read novel-length stories about *Doctor Who* characters; I swooned over fan art of the *Lizzie Bennet Diaries*; I pored over in-depth analyses of each episode of *Carmilla*.

Most of that is gone now.

Links rot at an extraordinary rate, and much of that early-2010s fan culture has now vanished from the Internet.
Accounts get deleted, websites go down, domain names lapse.
Every fan learns that if there's something you love, you can't rely on the Internet to keep it safe.
You have to save your own copy.

So I started saving, and I kept saving.
Digital storage was cheap and abundant, and I could afford to keep local copies of *everything*.
I didn't have to be picky with what I was saving.

I kept every photo I'd ever taken, every tweet I'd written, every link I'd read.
If you look at early posts on this site or my old GitHub repos, you'll see my excitement at code that could scrape down data and squirrel it away on my hard drive.
I always thought "what if I want to go back to this someday?"

Looking back, I could throw away 95% of this data and I'd be fine.
There are some things that I'm glad I saved, but there's an awful lot of other stuff that I don't actually care about.
I've never gone back to it, and I know I'm never going to look at it again.
It's just noise, and it makes it harder to find that 5% I actually care about.

I'm trying to simplify.
My data is currently split across my internal disk and several external hard drives, and those external drives need to be replaced soon.
Ideally I'd like to shrink my data until it fits on a single, internal disk.

As I save new stuff today, I'm trying to be more intentional about what I keep.
Before I save something, I ask myself "when will you want to look at this again?"
If I can't imagine a scenario in which I'd be glad to have saved this particular thing, I don't save it.
I've been collecting for fifteen years, and I know what sort of stuff I go back to.
Heartfelt stories and in-depth essays? Yes.
Current affairs and political news? Not so much.

That's slowing the influx of new data, but there's still the data I've already collected.
I've been gradually pruning it, deleting what I don't want and organising what I do.
It's a slow and arduous process, because there's no easy way to automate this -- ultimately, I have to look at every item and decide if it's worth keeping.

---

## Three examples of digital clutter

It took me years to accumulate my data, so I'm not going to clear it in a day.
I've spent months chipping away at it, reviewing a few items at a time, and there's plenty more to go.
I've already shed thousands of files and tossed an entire hard drive, but more importantly, I can now find more of the data I actually care about.

Let's look at a few examples of what I'm been deleting.

### 1. My photo library

I used to keep every photo I'd ever taken.
I was snapping away on my smartphone, and uploading everything to iCloud Photo Library and my local hard drive.

Some of those photos record precious memories and life moments, and I'm so glad that I have them.
But a lot of them are complete junk -- blurry shots, duplicate pictures, long-passed reminders of something I had to do.
(I had *so* many photos of books I wanted to read.)

The bad photos were drowning out the good ones, so I decided to get rid of them.
Using a [custom Mac app][blink], I went through every photo in my library and decided whether to delete it.

The photos of places and objects were easy to review.
If I didn't recognise the subject of the photo, I deleted it.
I got rid of a lot of photos of generic landscapes and builings that I've just forgotten in the intervening years.

The photos of people were harder.
My earliest digital photos are from 2003, and a lot has happened in that time.
I was reminded of good memories; I could see how much I've grown; I can see how much happier I became after I transitioned.

But those memories are also a source of guilt.
I was embarrassed by the cringe things I did as a teenager, and reminded of the mistakes I've made as an adult.
There are dear friends in those photos I haven't spoken to in years.
We didn't fall out or break up; our lives just drifted apart and we fell out of touch.
It hurt to see all the good people I've let slip out of my life.

Reviewing my old photos wasn't easy, and some days I could only look at a few before I had to stop.

I've cut my library from 32,000 photos to 25,000.
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
When there was an episode I wanted to go back to, it was easier to find it on the web than in my local archive.

I threw the whole thing away, and built a new archive which is much more selective.
It only contains a hundred or so episodes, and it's just my favourites -- the episodes I've already listened to multiple times.
These are the files I know I'll want to go back to in future.

### 3. My bundle of bookmarks

I've saved a lot of links, but I'm not going to read all of them again.
News articles; outdated reference material; fics I don't want to re-read -- I saved them because it was so easy to create bookmarks, but I've never gone back to them.

I'm gradually going through my bookmarks, and trying to reduce it to a more focused collection.
What's the stuff I actually want to remember?

As well as removing the bookmarks I don't care about, I've been improving the ones I want to keep.

I'm adding proper descriptions and summaries to all my bookmarks, so I know why a link is important and worth keeping.
This is a useful litmus test -- if I don't care enough to write this small amount of metadata, it's probably not that important.

I'm also fixing the local backups of each bookmark.
I pay for Pinboard's archiving service, which is meant to create a backup of every bookmark -- but maybe a third of those backups are unusable.
There are broken pages, 404 errors, paywalls and login screens.
This is the risk of bulk, automated scraping of the web -- nobody is checking whether the scraped page is actually useful.
As I decide which bookmarks to keep, I'm manually checking the backup version and replacing it if it's broken.
This takes longer, but now I know that all my archived web pages are useful copies, and not dead weight.

These two steps add more friction to the process, but I think that's a good thing.
It's slowing me down, and making me more thoughtful about what I save -- do I really want to save this link for later, or am I just saving it for the sake of saving it?

## Can we do better?

Some of this is a problem of my own making -- present!me is having to clean up the pile of data collected by past!me -- but some of it is a culture that encourages us to be profligate with storage.
For most people their biggest pile of data will be their photo collection, and smartphone makers have made it easy for us to snap away and save limitless photos to their cloud.
(For a small fee, of course. Whether or not we ever look at them again. Plus it creates inertia and lock-in.)

I said earlier that storage is "cheap and abundant", but that's only half-true -- it's cheap for me to buy large hard drives or copious cloud storage, but the cost is being felt elsewhere.
The material used to make hard drives; the electricity and water to power the data centres; the cognitive load of owning so much stuff.
It's not sustainable for us all to have an ever-growing pile of data.

We need to keep less data, but I don't know how we get there.

I've managed to reduce my own digital footprint, but not everyone can copy my approach.
It takes time and tools -- I've spent many hours working on this, and written a lot of bespoke tools and scripts.
(And my brain is very happy to work on this sort of repetitive, slightly monotonous task -- my hyperfocus has had a field day.)
Not everyone can do that.
So what can they do?

The big tech solution is to throw more technology at the problem.
Use AI and machine learning to sift through our enormous piles of data, and extract the gems -- but this feels like throwing good money after bad.
We're building bigger and bigger houses of cards, when what we really want is smaller, more carefully selected piles of data.
And the environmental impact just continues to grow; this is even less sustainable.
(As I go about this process, I've been trying to embrace lower-tech solutions, which I'll write about in another post.)

Another fix would be to introduce more friction or constraints into our workflows.
Part of why we all have so much data is because it's so easy to create and store it.
If we made it harder, we might be more thoughtful about what we're storing, and not throw it into a limitless cloud.
Unfortunately this runs counter to the goals of large tech companies, who enjoy the lock-in that comes from having a lot of data in their platforms.

I don't know what the answer is.
It feels like there's a real problem here of ever-growing data piles, and it's not something we can fix with individual action.
We need the platforms we use to provide tools to make it easier for us to manage our data -- but that doesn't seem to be a priority.

Modern storage has allowed us to keep everything, but that doesn't mean we should.
"As much as I can save" isn't a collecting strategy; it's hoarding.
