---
layout: post
title: Using static websites for tiny archives
summary:
tags:
  - html
  - digital preservation
index:
  feature: true
---
In [my previous post][decluttering], I talked about how I'm trying to be more intentional and deliberate with my digital data.
I don't just want to keep everything -- I want to keep stuff that I'm actually going to look at again.
As part of that process, I'm trying to be better about organising my files -- there's no point keeping something if I can't find it later.

Over the last year or so, I've been creating static websites to browse my local archives.
I've used this for collections like:

*   paperwork I've scanned
*   documents I've created
*   screenshots I've taken
*   web pages I've bookmarked
*   videos and audio files I've saved

I create one website per collection, and each website has a different design, suited to the files in that collection.
For example, my collection of screenshots is shown as a grid of images, whereas my bookmarks are a list of text links.

[[screenshots]]

These websites aren't complicated -- they're just meant to be a slightly nicer way of browsing files than I get in the macOS Finder.
I can put more metadata on the page, and build my own ways to search and organise the files.

Each collection is a folder on my local disk, and the website is a handful of HTML files in the root of that folder.
To use the website, I open the HTML files in my web browser.

I'm deliberately going low-scale, low-tech.
There's no web server, no build system, no dependencies, and no JavaScript frameworks.
I'm writing everything by hand, which is very manageable for small projects.
Each website is a few hundred lines of code at most.

Because this system has no moving parts, and it's just files on a disk, I hope it will last a long time.
I've already migrated a lot of my files to this approach, and I'm pleased with how it's going.
I get all the simplicity and portability of a file full of folders, with just a bit of extra functionality sprinkled on top.

[decluttering]: /2024/digital-decluttering/

---

I've tried a variety of tools and apps for organising my files, but they always came unstuck.

**I've made several attempts to use files and folders, the plain filesystem.**
Where I always had issues is that folders require you to use hierarchical organisation, and everything has to be stored in exactly one place.
That works well for some data -- all my code, for example -- but I struggle to use it for media.

I much prefer the flexibility of keyword tagging.
Rather than put a file in a single category, I can apply multiple labels and use any of them to find the file later.
The macOS Finder does support tagging, but I've always found its implementation to be a bit lacklustre, and I don't want to use it for anything serious.

**When I was younger, I tried a category of apps called "everything buckets".**
Think of apps like [DEVONThink], [Evernote], and [Yojimbo]. 
I know lots of people like these apps, but I was never been able to get into them.
I always felt like I had to wrap my brain around the app's way of thinking -- I changed myself to fit the developer's mental model, not the other way round.
This friction built up until I just stopped using the app.

**Once I had some programming experience, I tried writing my own tools to organise my files.**
The last of which was [docstore], which I initially created to manage my scanned paperwork.
Now I could build something that worked exactly how I thought, but I was on the hook for ongoing maintenance.
Every time I [upgraded Python][xkcd] or updated macOS, something would break and I'd have to do work to get it back into a usable state.
These tools never required a lot of maintenance, but it was enough to be annoying.

Every time I stopped using an app, I had another go at using plain files and folders.
They're the only thing that's likely to last for the long-term.
They're lightweight, portable, require minimal maintenance, and I expect to be able to read them for many years to come.
But the limited support for custom metadata and keyword tags was always an issue.

**At some point I realised I could solve these problems by turning folders into mini-websites.**
I could create an HTML file in the top-level folder, which could be an index for that folder – a list of all the files, displayed with all the custom metadata and tags I wantd.

HTML is low maintenance, it's flexible, and it will last a long time.
The entire web runs on HTML, and pretty much every computer knows how to read HTML pages.
These files will remain readable for a very long time – probably decades, if not more.

(I still have the very first website I made, for a school class in 2006.
It renders flawlessly in a modern browser.
I feel safe betting on HTML.)

[docstore]: /my-scanning-setup/#how-did-i-create-an-app-to-tag-my-pdfs
[xkcd]: https://xkcd.com/1987/
[Yojimbo]: https://www.barebones.com/products/yojimbo/
[DEVONThink]: https://www.devontechnologies.com/apps/devonthink
[Evernote]: https://evernote.com/

---

I'm doing a lot of this by hand -- organising the files, writing the metadata, building the viewer.
It's a slow and manual process, so it doesn't scale to a large collection.
Even storing a few hundred items this way takes a non-trivial amount of time -- but I actually like that.

Introducing a bit of friction is helping me to decide what I really care about saving.
What's worth taking the time to organise properly, and what can't I be bothered with?
If I don't want to save it properly, am I going to look at it again?

I used to have large, amorphous folders where I collected stuff en masse.
I had thousands of poorly organised files and I couldn't find anything,, so I never looked at them.
Now I have tiny websites with a hundred or so carefully selected items, and I look at them more often -- they're just the gems.

Even though I love automation, I'm enjoying the constraints imposed by a more manual process.

---

I already have a lot of files, which are spread across my disk.
I'd love to consolidate them all in this new approach, but that would be a tremendous amount of work.

My colleague Jessamyn wrote about this [in a follow-up to my digital decluttering article][jessamyn]: *"no one is ever starting at the beginning, not in 2024"*.

So rather than moving everything at once, I'm doing a little at a time.
I'm organising all my new files with static websites, and moving over old files as I go to look for them.
Whenever I find something in my old storage, I pull it out and move it into the appropriate static site folder.

I'm really enjoying this approach, so I'm going to keep using it.
Most of these websites are personal archives, so don’t expect to see them online any time soon – but individual snippets of code may escape [here][1] [and][2] [there][3].

This website is a platform for my writing, but it’s also a place for me to try new ideas and techniques.
HTML was one of those ideas -- when I started this website in 2012, I built it on HTML.
It is and always has been a statically-generated site.

In hindsight, it's surprising it’s taken me this long to use HTML in more parts of my life.

[jessamyn]: https://www.librarian.net/stax/5585/be-organized-from-the-very-beginning/
[1]: /til/2024/convert-an-animated-gif-to-mp4/
[2]: /2024/hover-states/
[3]: /til/2024/create-image-placeholders/











---

Eventually I came to wonder if I needed 












## What are my goals?

It's worth explaining what my goals are for organising my files:

*   **Find stuff quickly.**
    If I want a specific file, I should be able to find it in under a minute.
*   **Require minimal maintenance**

---

*   **I want to organise my files with keyword tags.**
    If I'm trying to choose whether something should be categorised as A or B or C, I can tag it with all three labels -- they're not mutually exclusive.
    I find this easier that trying to come up with a precise set of rules for distinct categories.
    This is an idea I [picked up from fandom][fandom] and it's a good fit for my brain.
    
    <!-- For example, if I'm using hierarchical folders, I'd have to choose whether a water bill goes in the `household` folder, the `utility bills` folder, or the `ACME Water Co` folder -- but with tags, I can apply all three as keywords and move on. -->

*   **I want to do minimal maintenance.**
    I don't want a system that requires continual attention and upkeep.
    I have better things to do with my time.

*   **I want something that will last for the long-term.**
    I want a system that I can use for a good long while.
    I don't want a system that will need replacing or overhauling every year.
    <!-- This sort of long-term thinking is rare in software development, but I've worked in digital preservation for eight years -- I'm used to designing systems to last for decades. -->
    (I may not be able to design a system that lasts the rest of my life, but I do like to think on a multi-decade timeline -- it forces me to think about sustainability and maintenance.)

[fandom]: https://idlewords.com/talks/fan_is_a_tool_using_animal.htm#:~:text=One%20of%20his%20many%20innovations%20was%20a%20"tags"%20field%20on%20each%20bookmark

## How did I end up at static websites?

I already had a couple of approaches for organising my files:

1.  **Not organising them at all.**
    My Desktop is a mess of unorganised files -- stuff I'm currently working on, or need to work on, or which I haven't organised yet.
    I try not to have too many files on my Desktop, or it becomes impossible to find anything.

2.  **Using files and folders.**
    Leaning on the filesystem is very appealing because it's simple and supported by the OS vendor, but it means I have to organise my files in a hierarchical way.
    That works well for some data -- for example, all of my code -- but less so for media.
    
    In particular, I've never found a good implementation of keyword tags in the filesystem.
    The macOS Finder does have support for tags, but I find it unsatisfactory so I don't use it.
    (In particular, there's no easy way to see all my tags, nor all the tags used in a particular folder.)

3.  **Using an app that manages my files with keyword tags.**
    There are lots of apps that aim to manage your files, and I've tried 
    
    I know lots of people like these apps, but I've never been able to get into them -- I feel like I have to wrap my brain around the app's way of thinking, which doesn't match the way I want to organise files.
    The only app like this which has really stuck for me is [Photos.app].
    
    When I have tried them, it's been annoying and time-consuming to extract my data from the app when I decide to stop using it.
    I don't really want to do that again, so it's unlikely I'll try more apps in this vein.
    
4.  **Writing my own app to manage my files with keyword tags.**
    Long-time readers may remember a project called [docstore], which I wrote to manage my scanned paperwork.
    This was a Python web app that fit my mental model, because I could design it to match my exact way of thinking.
    And I had all the code, so there was no lock-in to worry about.
    
    This worked initially, but it broke down over time.
    In particular, I had to have the local Python web app running to be able to browse my files -- which would inevitably break when I [upgraded Python][xkcd] or macOS, and I'd have to do work to get it back into a usable state.
    It didn't need a lot of maintenance, but it was enough to be annoying.
    
    I also made the mistake of using it for too many things.
    I want to organise my scanned paperwork differently to my books, or my screenshots, or my downloaded videos.
    Trying to fit everything into a single app created something bloated and messy.

Of this list, only files and folders are likely to last for the long-term.
They're lightweight, portable, require minimal maintenance, and I expect to be able to read them for many years to come.
But they're not as flexible as I'd like -- they have limited metadata fields (filename, folder name, creation date) and they don't support keyword tags in a way I like.

At some point I realised I could solve these problems by turning folders into mini-websites.
I could create an HTML file in the top-level folder, which could be an index for that folder -- a list of all the files, displayed with more metadata fields.
Now I can add keyword tags and other metadata I think is useful, and see it all in one place.

This approach has a number of benefits:

*   **HTML is low maintenance.**
    I write all the HTML files by hand, with zero dependencies or build system.
    Each file is a self-contained entity, so there's nothing to rot or break.
    If I don't touch them for a year, they'll still open just fine when I look at them again.

*   **HTML is flexible.**
    I can create a custom index file for each folder, so my screenshots and scanned documents and saved podcasts can all get a bespoke interface.
    It's easy for me to write different files for different folders, because each HTML file is small.

    And because there's no build system, I can always pick up where I left off -- if I decide to change something in six months, I have everything I need to make changes in that single file.

*   **HTML is portable.**
    static web server -> iPhone

*   **HTML will last a long time.**
    The entire web runs on HTML, and pretty much every computer knows how to read HTML pages.
    These files will remain usable for a very long time -- probably decades, if not more.
    
    I still have the very first website I made, for a school class in 2006.
    It renders flawlessly in a modern browser.
    I feel safe betting on HTML.

Lots of people love to use plain text files for their notes, and HTML feels like a natural extension of that.
Plain text is great for linear prose, and I use a lot of it, but a Markdown or text file struggles as a way to organise audiovisual media -- HTML gives me that extra oomph to build a nice interface for those collections.


[Photos.app]: https://en.wikipedia.org/wiki/Photos_(Apple)
[xkcd]: https://xkcd.com/1987/
[docstore]: /2019/my-scanning-setup/#how-did-i-create-an-app-to-tag-my-pdfs
[break over time]: https://en.wikipedia.org/wiki/Software_rot

## Emphasis on "tiny"

---

## What's next?

I'm going to keep building mini-websites this way, because I find it so useful.
Most of them are my personal archives, so don't expect to see them online any time soon -- but individual snippets of code may escape [here][1] [and][2] [there][3].

still migrating old stuff

This website is a platform for my writing, but it's also a place for me to try new ideas and techniques.
HTML was one of those ideas -- when I started this website in 2012, I built it on HTML.
It is and always has been a statically-generated site.

In hindsight, it's surprising it's taken me this long to use HTML in more parts of my life.

---

In 2012, I created this website, and I built it on HTML.

As well as a writing platform

[1]: /til/2024/convert-an-animated-gif-to-mp4/
[2]: /2024/hover-states/
[3]: /til/2024/create-image-placeholders/

i’m going to keep doing this because I find it really useful mostly private archives so don’t expect to see them get published any time soon – saving media for personal copy, often in copyright and not suitable for distribution

would love to hear about other people using this technique!



https://www.pexels.com/photo/multi-colored-folders-piled-up-159519/

---
---
---
---
---
---
---
---
---
---





[[podcast viewer]]


Each viewer is typically a few hundred lines of code.
They’re self-contained files, with no build system, JavaScript framework, or dependencies – very manageable.

This isn’t a new idea – Instagram and Twitter already give you a static website to browse your account exports, and we're doing something similar for Data Lifeboat at work. I think this could be a good approach for other “tiny archives”, not just my local media collections.

This is part of my work to [declutter my digital life]().
As well as reducing the amount of data I store, I'm trying to better organise the stuff I'm keeping.
Creating tiny websites that give me a nice way to browse these collections is helping me do that.

# Examples

* podcast archive
* video archive
* screenshots
* cool tweets

# Why use a static website for this?

simple



simple => future-proof

---

*   **Static websites are simple.**
    It's easy for me to open my text editor, write an HTML page in an empty file, and open the file in a web browser.
    Boom.
    Website.

*   **Static websites are flexible.**
    The initial site can be very small and simple, and then I can evolve it in whatever direction I like.
    Because I start from scratch each time, I can choose the visual design, metadata structure, and filtering tools I want to build (or not).
    I'm not tied to any existing designs or approaches.

    I deliberately keep each site quite small, so it's easy to change course if I have a new idea later.

*   **Static sites are future-proof.**


*   They're simple
*   They're future-proof
*   They're portable
*   They're low-tech
*   They're hackable

The reason I love static websites is the simplicity.
It’s not hard for me to write an HTML file, open it in a web browser, and start using it.
The initial skeleton can be very small, I can design it however I want, and I can add more features with JavaScript as I need them.
I particularly like that I can sort and filter my files with metadata that isn’t exposed in the Finder.

```html
<ul>
  <li><img src="screenshots/home_screen1.png"> My iPhone home screen on 12 October 2024</li>
  <li><img src="screenshots/website.png"> My website homepage after the August 2024 redesign</li>
  <li><img src="screenshots/spirograph.png"> A toy I made for generating spirographs</li>
</ul>
```

Because I write these tiny websites by hand, with no build chain or dependencies, they’re very future-proof.
HTML has been around longer than me, and it’s probably our best bet as a medium to long-term format for information.
These files are very likely to be readable for the rest of my life (and after that, I don’t care).

I have static websites I wrote in 2016, haven’t touched since, and they work today as well as they did when I wrote them.
And all the source code is in the HTML files, so I could easily make changes if I want to.
Even if I have all the source code, this is much harder for pretty much any other software project -- imagine, for example, trying to work on a Python project that's been unchanged since 2016.
Hand-written websites are a rare exception in modern software toolchains.

Lots of people love using plain text for their notes.
Plain text is great for linear prose, and it's what I use, but a Markdown or text file struggles for audiovisual media -- HTML gives me that extra oomph to build a nice interface for those collections.

## How to get started

```
const images = [
  {
    "path": "images/cat.jpg",
    "description": "A photo of my cat Bailey"
  }
]
```

read HTML for People

## Emphasis on "tiny"

I'm doing a lot of this by hand -- organising the files, writing the metadata, building the viewer.
This approach doesn't scale to a large collection.
Even storing a few hundred items this way takes a non-trivial amount of time.
But that's okay -- it's the point, even!

Introducing a bit of friction into the process helps me think about what I really care about saving.
What's worth taking the time to save properly, and what can't I be bothered?
If I can't be bothered, am I going to look at it again?

I used to have a lot of large, amorphous folders where I collected stuff en masse.
I had thousands of poorly organised files, so I never looked at them.
Now I have tiny websites with a hundred or so carefully selected items, and I look at them more often -- they're the real gems.

This lack of scale is a good constraint.
It's forcing me to pick the most meaningful stuff -- most of these websites only have a few hundred items, and only my bookmarks collection has over a thousand.

---
---
---

The big reason I like static websites is that they’re flexible and lightweight.

I can build different interfaces for different types of media, each suited to that media type. If I don’t like an interface I’ve built, I can throw it away and build something new.

* More flexible
* Future-proof
* Low-tech
* Portable

Abstract away key details

## more legible

but not legible to me

needs a better discoverability layer
a simple website can make it easier to find what's in my collection, and allows searching it in a more sophisticated way than files and folders
e.g. filter by tag, or sort by date

still keep human-readable folder structure

# Emphasis on “tiny”

---



# What’s the problem I’m solving?

I have a lot of digital files – either stuff I’ve saved from the Internet, or stuff I’ve created myself. Although I’ve [trying to declutter](https://alexwlchan.net/2024/digital-decluttering/) and be more selective about what I’m keeping, I still have thousands of files on my hard drive.

Typically each file has a small amount of associated metadata: where I got it from, when I got it, a short textual description, that sort of thing.



 – and I want to make it easier to find things among my collection.



have gradually accumulated a large collection of files, stuff I've saved or thought worth keeping
I accumulate a lot of stuff!
Am I looking at it?
Can I find the good bits?
No

messy and disorganised, not structured
hard to know what's there; hard to find stuff I care about

theoretically all findable – metadata is in plain text + machine readable formats
I'm a programmer, I could write tools to read the metadata and find stuff
bUt I don't, not motivating

wanted better way to browse my local collections

---
---
---


bringing order to the drive full of files I'd gradually accumulated
turning hoarder's clutter into a meaningful collection

example: podcast player
(interactive demo)

this article: why and how

ToC
* the problem
* why use a static website?
* how does it work? (aka the code)
* emphasis on tiny
* what else do I use this for?
* what else could this be used for?

# the problem

have gradually accumulated a large collection of files, stuff I've saved or thought worth keeping
I accumulate a lot of stuff!
Am I looking at it?
Can I find the good bits?
No

messy and disorganised, not structured
hard to know what's there; hard to find stuff I care about

theoretically all findable – metadata is in plain text + machine readable formats
I'm a programmer, I could write tools to read the metadata and find stuff
bUt I don't, not motivating

wanted better way to browse my local collections

# why use a static website for this?

## more legible

but not legible to me

needs a better discoverability layer
a simple website can make it easier to find what's in my collection, and allows searching it in a more sophisticated way than files and folders
e.g. filter by tag, or sort by date

still keep human-readable folder structure

## more portable

static HTML can be opened on any computer
I've used Macs for most of my adult life, but as Apple becomes more predatory I'm trying to loosen their grip
an open standard like HTML is an excellent way to do that!

## more future-proof

both technical + humane PoV

technical: static HTML is very future-proof
has worked for >30 years (check), will likely continue to work mostly unchanged for a long time to come
and likely to work on future devices (check iOS)
No active component, minimal migration work, just copy files to new disk
I have another HTML app I created in 2016 (Alfred+iTunes) that I still use from time-to-time, works unmodified

humane: HTML website gives me a more designed, readable presentation
can highlight things I thought were important or significant
don't need to remind myself of metadata schema or file structure
I _could_ work those things out if I wanted to, but I don't have to

sharing: many many ways to share static HTML with minimal technical fuss
so many ways to share static site
easier to share than complex web app!
(and can scale easily – could probably run everything off a $5/mo Linux server for years without breaking the bank)

## v low-tech

HTML, CSS and JS are foundation of modern web stack
v well-understood, lots of documentation and advice and people who can use them
if an archive like this drops in your lap, will be able to find somebody who can do something with it

I hesitate to say "easy" because I've been professional dev for nearly decade, hard to know what's "easy"
but do think has fairly low on-ramp, and it would be possible for people who aren't otherwise programmers to build something like this

DIY archivists
* can already do this with tech you have installed!
* lots of people see potential of programming, but can't install e.g. Python because of corporate IT (I say with love as a current IT person)
* can run within constraints of literally any IT environment in the world
* if you have Notepad and a browser? gr9 you can do this

## hackable

the virtues of "view source"
if I don't like how something works, can hack around in HTML and make it do the right thing now, as a one-off
e.g. change colours or appearance or behaviour
e.g. complex/bespoke queries I didn't think of in initial implementation
because these apps are small (<250LOC) much easier to wrap head around and make changes

archive being "hackable" might seem scary – this is separation of presentation + data
data can be left as-is, but can build interesting new views

also used for data-cleaning
"give me a one-off query to highlight all broken records"
=> fix, see query empty, delete query

# how

HTML
* metadata in JS (example)
* `window.addEventListener("DOMContentLoaded", {} =>)`
* React-like components
	* but never changing state, write once
	* basically building a static site generator
* query params + links

here's an example:

have other tools that go in here:
* made small Python library to modify metadata file, e.g. for bulk edits
* dominant_colours
* thumbnailer

# emphasis on "tiny"

all of this is created by hand
this approach doesn't scale!
yes, that's the point!

when I had a large, amorphous folder where I collected stuff en masse:
* had a lot of stuff I didn't care that much about
* couldn't find the stuff I do care about

100,000 items = never look
100 items = look at the gems

this lack of scale is a constraint, forcing function, makes me pick the most meaningful stuff
good!
typically store a few hundred archives

# what else do I use this for?

docstore, active server app
that works for a while
* but codebase becomes large and I forget how things work
* environment stops working
* temptation to over-engineer

again, constraints are good
can't do all features, can't build sophisticated stuff
but can build something "good enough", with escape hatch for more complex tools if useful

# what else could this be used for?

archives
* a lot of projects get up-front funding and then no maintenance
* static site – not zero maintenance, but substantially less
* plain text format, won't become unreadable
* temptation to build big dynamic apps that sprawl a dozen AWS services, which break within two years

archiving websites
* watched too many good sites fall offline because backend rotted
* create a static snapshot!
* host that!

born-digital archives
worked on components for providing access, e.g. static file hierarchy
what if we could create a static website that was embedded with files, allow for richer exploration of these archives

# what's next?

i'm going to keep doing this because I find it really useful
mostly private archives so don't expect to see them get published any time soon – saving media for personal copy, often in copyright and not suitable for distribution

would love to hear about other people using this technique!

---

# more examples

* saved videos
* screenshots
* AO3
* Turing Way illustrations
* AWS icon browser

----

why?

* machine-readable metadata kinda sucks
* and not v motivating
* hard to get an overview

* better than folder listing
* more legible than folder of machine-readable data

advantages?

* very likely to be readable in future / lots of web browsers
* no software dependencies / nothing to break / can work on any computer
* allows for small amount of interactivity, e.g. filtering
* solid mechanism for sharing and publishing

how?

* I write them by hand, from scratch every time
	* Single file
	* Podcasts = 250 LOC
* not complicated HTML and JS
* JS file with metadata
* HTML file which loads metadata and renders it on the page\

Recently ran an HTML+JS app I wrote in 2018 / 2016 / https://alexwlchan.net/2016/itunes-images-with-alfred/
Worked flawlessly