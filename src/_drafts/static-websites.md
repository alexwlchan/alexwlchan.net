---
layout: post
title: Static websites for tiny archives
summary:
tags:
---
For a while now I’ve been creating static websites to browse my local media archives. This includes podcast episodes I like, cool or meaningful tweets, my screenshots, and my bookmark collection.

These mini-websites give me a nice interface to browse my media, which are better than just looking through a folder full of files.
I can show metadata and media files next to each other in a single interface, and build more sophisticated ways to search and organise my media.

[[podcast viewer]]

To build these websites, I’m putting metadata in JavaScript files, organising the media files by hand, and then writing a small HTML viewer that renders the metadata and files in a small and simple interface.
There's a bit of interactivity for sort, search, and filtering.
To use the website, I open the HTML viewer in my web browser, directly from my local disk.

Each viewer is typically a few hundred lines of code.
They’re self-contained files, with no build system, JavaScript framework, or dependencies – very manageable.

This isn’t a new idea – Instagram and Twitter already give you a static website to browse your account exports, and we're doing something similar for Data Lifeboat at work. I think this could be a good approach for other “tiny archives”, not just my local media collections.

This is part of my work to [declutter my digital life](/2024/digital-decluttering/).
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