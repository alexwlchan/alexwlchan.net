---
layout: post
title: Scanning and organising my paperwork
summary:
---

talked about scanning my documents on twitter

why?

## How I scan the documents

I scan most of my documents
Page scanner

Does good-enough copies, not high-quality digital facsimiles
Useful for keeping home documents, not good enough for digital preservation
e.g. poor colour reproduction, doesn't get blank pages, may be misaligned or not straight
Optimisied for speed, not quality

Now I have a pile of PDF documents!
What to do with them?

tried a bunch of systems (Yep, files in Finder, Devonthink), none felt quite right
Build my own!

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
