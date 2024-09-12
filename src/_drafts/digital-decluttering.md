---
layout: post
title: Digital decluttering
summary:
tags:
---
I spent a lot of my formative Internet years in online fandom.
I read novel-length stories about *Doctor Who* characters; I swooned over fan art of the *Lizzie Bennet Diaries*; I pored over in-depth analyses of each episode of *Carmilla*.
I was surrounded by the creativity of strangers, sharing my own ideas, and taking the first steps towards my queer awakening.

Most of that is gone now.

Links rot at an extraordinary rate, and much of that early-2010s fan culture has now vanished from the Internet.
Accounts get deleted, websites go down, domain names lapse.
We might think the Internet is written in ink, but really it's more like chalk on a pavement.
Stuff is visible for a while, and over time it washes away.

Every fan eventually realises that if there's something they love, they have to save your own copy.
We all learnt this lesson the hard way, when we went to find something we remembered from years ago, and it had vanished from the face of the Internet.

So I started saving, and I kept saving.
Digital storage has become cheap and abundant, and I could afford to keep local copies of everything.
I didn't have to be picky with what I was saving.

I saved web pages and photos and PDFs and videos and audio files, and I wrote scripts to save as much as possible, all so I'd never lose anything again.
I kept every photo I'd ever taken, every tweet I'd written, every link I'd read.
If you look at early posts on this site or my old GitHub repos, you'll see my excitement at code that could scrape down data and squirrel it away on my hard drive.
I always thought "what if I want to go back to this someday?"

Looking back, I could skip 95% of this data and I'd be fine.
There are some things that I'm glad I saved, but there's an awful lot of other stuff that I've never gone back to, and I know I'm never going to look at again.
And because I was more interested in saving lots of files than organising what I had, it's difficult to find that 5% I actually care about.

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

## Are you going to look at that photo again?

I used to keep every photo I'd ever taken.
I was snapping away on my smartphone, and uploading each picture to iCloud Photo Library and my local hard drive.

Some of those photos record important memories and life moments, and I'm so glad that I have them.
But a lot of them are complete junk -- blurry shots, duplicate pictures, long-passed reminders of something I had to do.
(I had *so* many photos of books I wanted to read.)

The junk photos were drowning out the ones I actually cared about, so I decided to prune my library of all the bad pictures.
Last year I [wrote a Mac app called Blink][blink] to help me with this task.
The app has a simple keyboard-driven interface, where I can step through my photo library and mark each photo as "approved", "rejected", or "needs action".
I can review most photos with one or two keystrokes, which minimises the impact on my wrists.

A few times a week, I use Blink to review all my new photos.
I'm keeping maybe a quarter of the photos I take, and deleting the rest.

I also went through all of my old photos.
I started with 32,000 photos, and after eleven months I'd looked at all of them, and reduced it to 25,000.
That still feels like a lot -- more than 2 photos for every day I've been alive -- but it's an improvement.

The photos of places and objects were easy to review.
It was pretty easy to work out whether I recognised the subject of the photo, and if not, I deleted it.
I got rid of a lot of photos of generic landscapes and builings that I've just forgotten in the intervening years.

The photos of people were harder.
My earliest digital photos are from 2003, and a lot has happened.
I was reminded of good memories; I could see how much I've grown; I could see how much happier I became after I transitioned.

But my memories are also a catalogue of mistakes.
I was embarrassed by the cringe things I did as a teenager, and reminded of the mistakes I've made as an adult.
There are dear friends in those photos I haven't spoken to in years.
We didn't fall out or break up or have any hard feelings; our lives just drifted apart and we fell out of touch.
I felt a lot of guilt going through these photos.

It wasn't an easy process, and some days I could only look at a few photos before I had to stop.

Although this is an improvement, it stills feels like I have a *lot* of photos.
There are probably hundreds that I'll never look at again.
I'm thinking about ways to prune further, or highlight the photos I actually care about -- like putting them on my walls, or making some printed albums.
I want to do more here.

[blink]: /2023/blink/

## When will you have time to listen to all those podcasts?

I used to keep every podcast episode I'd ever listened to.

I can trace this to a specific podcast called *IRL Talk*, which I listened to around 2012.
It's associated with some very fond memories, but it fell off the Internet after one of the hosts passed away.
I was sad when I couldn't listen to it any more, and delighted when somebody uploaded the complete collection to the Internet Archive.

At some point I discovered that Overcast (my podcast app of choice) could give me an export of every episode I'd played.
I wrote a Python script that downloaded every episode in my exports, so I'd never have another *IRL Talk* moment.

This gave me a folder with hundreds of MP3 files, most of which I'll never want to play again.
I listen to lots of podcasts about news and current affairs, whose value drops off quickly with age.
Why was I keeping those?

Further, the contents of this folder was the output of a scrappy script and not a polished podcast app.
It was poorly organised, and it was easier to find podcasts by redownloading them in Overcast -- so I never looked in the folder.
(The only time I looked in this folder was to find a podcast that had been deleted from the web, so I couldn't download it in Overcast any more.
In some bizarre irony, it was a podcast about digital preservation and longevity.)

So I had a growing collection of MP3 files, which were poorly organised and most of which I didn't want to listen to.
I threw the whole thing away.

As a replacement, I built a new podcast archive which just includes episodes I'd starred in Overcast.
It's a much smaller list of episodes that are timeless and interesting, and which I've already listened to multiple times -- only a hundred or so episodes.
I built a simple HTML interface on top of this archive, which I can browse locally.

This curated collection uses 4% of the disk space of the folder that hoovered up everything, and I can go straight to those most-favoured episodes.

## Is that bookmark ever coming back?

At its peak, I had a collection of over 6000 bookmarks.
Some of them were links I've returned to many times, and others were links I'm never going to go back to.
I'm gradually going through them, and trying to reduce it to a more focused collection.
I'm about halfway through so far.

There are several common forms of clutter in my bookmarks -- current affairs and politics; reference material I'd re-find through Google and not my bookmarks; fic I don't want to read again.
I've found a lot of bookmarks which were nothing more than a URL and a couple of tags -- if I hadn't bothered to leave even a shred of descriptive text, was it really that important?

As I'm going through my bookmarks, I'm checking my backups.
This has been a sobering experience.
I pay for Pinboard's archiving service, which has ostensibly created a separate copy of every bookmark, in case the original site goes away -- but maybe a third of those copies are unusable.
It's saved broken pages, 404 errors, paywalls and login screens.
This is the risk of bulk, automated scraping of the web -- nobody is checking that the scraped page is a useful copy.

I've been creating a new archive of saved pages, where I'm checking each URl individually.
I'm keeping the archive from Pinboard if it's good, and if not I'm creating my own.
This takes longer, but now I know that all my archived web pages are useful copies, and not dead weight.

I'm also adding proper descriptions and summaries to all my bookmarks, so I know why a link is important and worth keeping.

These two steps add more friction to the process, but I think that's a good thing.
It's slowing me down, and making me more thoughtful about what I save -- do I really want to be able to find this link later, or am I just saving it for the sake of saving it?

---

## Can we do better?

It took me years to accumulate my data, so I'm not going to clear it in a week.
I've spent months chipping away at it, reviewing a few items a day, and there's plenty more to go.
I've already shed thousands of files and tossed an entire hard drive, but more importantly, I can now find the items I actually care about.

Some of this is a problem of my own making -- present!me is having to clean up the pile of data collected by past!me -- but some of it is a culture that encourages us to be lavish with storage.
For most people their biggest pile of data will be their photo collection, and smartphone makers have made it easy for us to snap away and save limitless photos to their cloud.
(For a small fee, of course. Whether or not we ever look at them again. Plus it creates inertia and lock-in.)

I said earlier that storage is "cheap and abundant", but that's only half-true -- it's cheap for me to buy large hard drives or copious cloud storage, but the cost is being felt elsewhere.
The material used to make hard drives; the electricity and water to power the data centres; the cognitive load of owning so much data.
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
