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



## Hierarchies, search and tags

Could put them in a hierarchy of folders

https://www.nayuki.io/page/designing-better-file-organization-around-tags-not-hierarchies

Why are hierarchies good?
* Physical storage analogy, easy to understand
* Mimics a filing cabinet

But only have one and only one classification
* e.g. should I file documents under "home" or under "electricity bills"?
* e.g. lemony snicket

* Hierarchies are great if you have a well-defined classification
* Natural hierarchy or sorting, e.g. alphabetisin the books on a shelf

Less freedom of filenames

Two systems I like:
* I like email!

	I throw all my mail into a single "archive" folder, then use searching to find the emails I want.
	I can search by coarse attributes (sender email) or full text of the body.

* Tags.
	"what will I search for in future"
	maciej talk

You can implement search, but it's hard and not my speciality
Lots of ways a full-bore document search could be useful (e.g. rank documents that you look at more frequently higher), but more than I wanted to try

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
