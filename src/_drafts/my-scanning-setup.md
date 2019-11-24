---
layout: post
title: Scanning and organising my paperwork
summary:
---

If you follow me on Twitter, you'll see I often tweet about scanning my paperwork.
I scan all the letters I receive, and often I shred or recycle the originals.
Digital documents are usually easier to search, and it means I have to keep less physical paper in my flat.
That's less stuff on my shelves, and when I do need the actual bit of paper (for instance, my passport), there's less to look through.

People often ask about how I do my scanning, and how I organise the scanned files -- so in this post, I'm going to explain how I came to my current setup.



## How I scan the paper to PDF

I have a small document feed scanner that I use to scan paper, and save the pages as a PDF on my Mac.
It's a [Canon ImageFORMULA P-215], which looks like this:

<figure>
  <img src="/images/2019/canon_scanner.jpg" alt="A black document-feed scanner sitting on a wooden desk.">
  <figcaption>With an A5 sheet of paper for comparison.</figcaption>
</figure>

When I'm scanning something, I separate the pages (for example, removing staples and paperclips), and place them face-down in the scanner.
It pulls in the pages one at a time, and scans both sides at once.
Occasionally it pulls in more than one page, and the sheets in the middle get skipped, but mostly I can leave it to scan documents without supervision.

I connect it to my Mac with a USB cable.
I can run the built-in scanning software directly from the scanner, without installing anything on my computer.
The software is basic, but works well.

<img src="/images/2019/canon_scanner.png" alt="Screenshot of scanning software. A preview of the page is shown in the centre, with some action buttons along the bottom of the window.">

There's a nice big preview of the pages, so I can check it's scanning correctly.
I can rearrange pages if they're in the wrong order, or remove a page if I don't want it saved.
I can also adjust the rotation of the pages -- the scanner tries to guess the correct orientation, but I can correct the page if it guesses wrong.

This scanner is also doing [OCR] on the text.
The PDF it produces contains both an image and a transcription of any printed text (although I've never actually used the transcriptions).

I've used this scanner for over six years, and never had any issues.
My particular model cost £225 in 2013, although it's been discontinued.
When it fails, I'll likely replace it with another Canon.

The quality of the scans isn't amazing.
In particular, the colour reproduction isn't great, and the pages are sometimes shown at a skewed angle.
It's fine for scanning black-and-white printed documents, but if you're digitising photographs or archival material, it might not be such a great fit.
This is for speed and convenience, not quality.

<img src="/images/2019/scans_folder.png">

Once I've used the scanner, I have a folder full of PDF files -- so how do I organise them?
How do I make sure I can find a document in six months time?

I've tried a bunch of apps -- the Finder, [DEVONthink], [Yojimbo], [Yep], among others -- but none of them felt right.
I know a fair bit of Python, so I decided to write my own instead.

[Canon ImageFORMULA P-215]: https://www.usa.canon.com/internet/portal/us/home/support/details/scanners/support-document-scanner/imageformula-p-215-scan-tini-personal-document-scanner
[OCR]: https://en.wikipedia.org/wiki/Optical_character_recognition
[DEVONthink]: https://www.devontechnologies.com/
[Yojimbo]: https://www.barebones.com/products/yojimbo/
[Yep]: http://ironicsoftware.com/yep/



## How do I want to search and store PDFs?

Before I wrote a line of code, I wanted to think about how I'd organise my PDFs.

I want to be able to find all the PDFs about a particular topic.
For example, every bill from one company, or everything about a place I'd lived, or all my tax paperwork.
Sometimes I'm looking for a specific document, more often I'm looking for a collection of files.

How do I organise my files to enable that type of searching?

There are a couple of possibilities -- let's consider them in turn.

### Storing files in a hierarchy

Most modern computers use a hierarchical file system.
We can put related files in a collection, called a *directory* or *folder*.
We can nest directories to create a hierarchy of information. 
This is analogous to managing physical pieces of paper – you put a page in a folder, the folder in a filing cabinet, the filing cabinet in an aisle, the aisle in a room, and so on.

This gives us a tree-like view that you might be familiar with:

```
documents
 │
 ├─ bills
 │   ├─ 2019-11-17-electricity-bill.pdf
 │   └─ 2019-11-24-water-bill.pdf
 │
 └─ health
     ├─ optician
     │   └─ 2019-11-08-eye-test.pdf
     └─ nhs
         └─ 2018-07-01-welcome-to-gp.pdf
```

Because hierarchical file systems are ubiquitous, this would be easy to implement -- I just create the right set of folders in Finder.
But what are the "right" set of folders?

In this system, each file has one and exactly one place in the hierarchy.
I have to pick a classification, and I can only make searches that fit that classification.
I can't make searches that span multiple directories.

<figure style="border: 1px solid black;">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 330 120" fill="rgba(0,0,0,0)">
  <circle cx="55" cy="50" r="40" stroke="#d01c11" stroke-width="2" fill="rgba(208, 28, 17, 0.18)"/>
  <text x="55" y="112" fill="#d01c11" text-anchor="middle">home</text>
  
  <circle cx="165" cy="50" r="40" stroke="#11a01c" stroke-width="2" fill="rgba(17, 160, 28, 0.18)"/>
  <text x="165" y="112" fill="#11a01c" text-anchor="middle">utility bills</text>
  
  <circle cx="275" cy="50" r="40" stroke="#0C34D4" stroke-width="2" fill="rgba(12, 52, 212, 0.18)"/>
  <text x="275" y="112" fill="#0C34D4" text-anchor="middle">spark energy</text>
</svg>
</figure>

An example: suppose I have an electricity bill.
Do I put it in a directory called "home", or "utility bills", or a directory with the name of the provider?
I might want to find it later by any of those criteria, but I can only put it one directory.
I don't have the flexibility to find documents the way I want.

There's a passage from a book I read years ago that's stuck with me, which illustrates the problem of a hierarchy when the classification isn't clear.
Hal is the librarian at a hospital, and Klaus is helping him organise incoming paperwork -- but there are no rules on where to put things:

> [Hal] paused, unclipped a small stack of paper, and squinted at the top page. "For instance," he continued, "You only have to read a few words to see that these paragraphs are about the weather last week at Damocles Dock, which is on the shore of some lake someplace. So you would ask me to unlock cabinets in aisle D, for Damocles, or W, for weather, or even P, for paragraphs. It's your choice."
>
> "But won't it be difficult for people to find that information again?" Klaus asked. "They won't know whether to look under D, W, or P."
>
> "Then they'll have to look under all three letters," Hal said. "Sometimes the information you need is not in the most obvious place."
> 
> <p class="cite"><cite><em>The Hostile Hospital</em>, by Lemony Snicket</cite></p>

Hierarchives are great if you have a well-defined classification.
For example, many people keep their fiction books in alphabetical order, with different shelves for different parts of the alphabet.
The system tells you where each book should be stored, and where to find it later.
They're harder if you don't have a good classification system.

I've tried using files and folders a couple of times, but it never stuck.
I struggled to find things quickly, but also to store them as well.
Whenever I went to file a new PDF, I found myself rethinking the system, and questioning if this was the right folder.

### Searching an unorganised pile of files

Hierarchies and classification are a highly ordered system.
The opposite is to do no organisation -- put all my files in a single directory, and use searching to find the right files.

This is how I manage my email: I have 26,000 emails in a single "Archive" folder, and I use the search feature to find the email I want.
I can search by attributes (say, messages from a particular sender), or do full text search on the body of the message, and I usually find the message I want pretty quickly.

It's also how I find pretty much everything on the web -- I ask a search engine a question, and it shows me web pages that might be helpful.
(I've written blog posts just so they'll show up in search engine result the next time I look something up.
But I can only do that with something I can make public -- say, notes about programming, and not my bank statements.)

Unfortunately, I've never got along with the builtin Mac OS X search.
There's not a specific reason, I just find it a bit slow and the 
search syntax has never clicked in my brain.

I could set up my own search system, but doing search well is hard, and it's not my speciality.
There are lots of ways a document search could be useful -- for example, boosting documents that I look at frequently -- but it's more work than I wanted to put into this project.

### Keyword tagging

Something I've used a lot in the last few years is keyword tagging.
When I store something, I add a number of "tags" – keywords that describe the document.
Later, I can filter to find documents that have particular tags as a form of search.

Here's a nice description of tagging from a talk a couple of years ago:

> I remember not knowing what [the tags field] was for. He explained it to me basically as a search engine in reverse. Rather than typing in something to find results, when you save something for later, why don’t you type down the the stuff that you’re going to probably use as keywords when you look for it long after it’s forgotten?
>
> <p class="cite"><cite><em>Fan is a Tool-Using Animal</em>, by Maciej Cegłowski</cite></p>

Tagging is particular common in the world of fandom.
On bookmarking sites like Pinboard and Delicious, fans have created intricate systems of tagging for describing fanfiction, and by combining tags you can make very specific queries.
For example, a single bookmark could have tags for the word count, the fandom, the pairing, the trope, or many other things beside.
(The rest of Maciej's talk explains this in more detail.)

I use tagging a lot in Pinboard, I'm quite used to it, and I find it quite easy to both save and search using tags.
I have 4.5k bookmarks and the tagging remains usable, so I know it scales.

<figure style="border: 1px solid black;">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 330 165" fill="rgba(0,0,0,0)">
  <circle cx="140" cy="50" r="40" stroke="#d01c11" stroke-width="2" fill="rgba(208, 28, 17, 0.18)"/>
  <text x="95" y="40" fill="#d01c11" text-anchor="end">home</text>
  
  <circle cx="190" cy="50" r="40" stroke="#11a01c" stroke-width="2" fill="rgba(17, 160, 28, 0.18)"/>
  <text x="236" y="40" fill="#11a01c" text-anchor="start">utility bills</text>
  
  <circle cx="165" cy="96.650635095" r="40" stroke="#0C34D4" stroke-width="2" fill="rgba(12, 52, 212, 0.18)"/>
  <text x="165" y="157" fill="#0C34D4" text-anchor="middle">spark energy</text>
  
  <circle cx="165" cy="66.650635095" r="5" fill="black"/>
</svg>
</figure>

A tag-based system allows me to save a single document with multiple tags.
Consider an earlier example: my electricity bill.
Rather than filing it in a single directory, I could tag it with "home" and "utility bills" and "spark energy", and I could find it later by searching for any one of those tags.
Tagging is more flexible.

[venn diagram of tags]

Tagging is also more future-proof: if I discover I want a new tag, I can start using it alongside my existing tags.

Finally, tagging is much simpler to implement than full-bore search.
Rather than matching on free text and ranking documents, it's a simple boolean: either a document has a particular tag, or it doesn't.

I'm a big fan of tag-based systems, so I decided to use it as the basis for my document organisation.

---

## A general design

When I started building this system, I'd been working on a new archival storage service at work.

https://www.nayuki.io/page/designing-better-file-organization-around-tags-not-hierarchies


Two systems I like:
* I like email!

	I throw all my mail into a single "archive" folder, then use searching to find the emails I want.
	I can search by coarse attributes (sender email) or full text of the body.

* Tags.
	"what will I search for in future"
	maciej talk

for a few thousand documents, a tagging implementation is good enough
so I want a system that:

* Lets me upload a scanned document and apply tags
* See all tags
* Find all documents with a specific set of tags (e.g. all with "water-bills" and "home:123-smith-street")





## Architecture

Inspired by Wellcome Archival Storage, which I'd been working on
https://stacks.wellcomecollection.org/digital-preservation-at-wellcome-3f86b423047

1. Upload a bag (package of files)
2. verify checksums
3. Copy to S3 buckets

Architecture is a bit different:

1. Upload a single file (not a bundle), apply tags
2. Create a SHA256 checksum (browsers don't supply this in form uploads)
3. Normalise the filename to something similar but computer-friendly (e.g. "November’s Bank Statement.pdf" becomes "november-s-bank-statement.pdf"), save to disk
4. Present in a list of documents

I can then see a list of documents, and any tag is clickable -- click to filter to all documents with that tag.
Plus thumbnail for easy browsing.



## IMplementation

Implementation is very simple.
Files are stored in a flat heirarchy, e.g.

	docstore/files/
		a/
			advice-for-renters.pdf
			alex-chan-contract.pdf
		b/
			breakdown-cover-ipid-document.pdf
			british-gas-terms-and-conditions.pdf
		...

so still usable if I lose the database

Database is a flat JSON file.
JSON = human-readable and editable, not tied to particular software, no lock-in
Looks like this:

	{
		"000914e9-be70-4d11-bba5-6c902e9bcb44": {
			"filename": "November’s Bank Statement.pdf",
			"file_identifier": "n/november-s-bank-statement.pdf",
			"checksum": "sha256:CHECKSUM",
			"date_created": "2019-11-24 14:14:01 +0000",
			"tags": [
				"bank:account-1234",
				"bank:statements",
			],
			"thumbnail_identifier": "0/000914e9-be70-4d11-bba5-6c902e9bcb44.jpg",
			"title": "2019-11: Bank statement"
		},
		...
	}

IDs are UUIDs for simplicity
Record original filename, so it can be retrieved later
SHA256 checksum for immutability (so can spot file corruption)
Title is meant to be human-readable, but never used as a filename

Python app, load all into memory
Be a problem with lots of documents, but for personal use is fine

To do a tag query, it's a Python list comprehension:

	query = [
		"water-bills",
		"home:123-smith-street",
	]

	matching_documents = [
		doc
		for doc in documents
		if all(qt in doc.get("tags", []) for qt in query)
	]

Could do fancy data structure/join in database or something, but is fast enough that it's not an issue

then very heavily tested, because I want to trust code that's looking after my precious documents

can get code on GitHub, MIT license, and can run in Docker so fairly simple to deploy: https://github.com/alexwlchan/docstore

considered a hosted version, but security eek and would not database rewrite for scaling
if you want it, run it on your own computer!


## my current procedure

1. Scan the page
2. Upload it to docstore with the appropriate tags
3. If it's sensitive (e.g. has my bank details), goes in the shredder. If it's not sensitive (e.g. marketing material), goes in the recycling bin. envelopes, naturally, go in recycling

several instances:

* home correspondence
* old schoolwork -- I haven't looked at for a decade, so scan and recycle the lot
* work documents -- runs on my work computer, so data never leaves the corporate network

collectively put in XX PDFs with YY pages of paper.
nice saving!


## Suggested links

* https://www.nayuki.io/page/designing-better-file-organization-around-tags-not-hierarchies
* Fan is a tool-using animal