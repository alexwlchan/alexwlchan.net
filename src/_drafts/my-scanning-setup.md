---
layout: post
title: How I scan and organise my paperwork
summary:
---

I get a lot of documents as paper, which I scan and store as PDFs files.
This lets me shred or recycle the originals (if I don't need the physical copy), and minimise the space the paper takes up my office.
I organise the PDFs in a Python app I wrote called *docstore*.

People ask me how I do my scanning, so here I'm going to explain how I got to my current setup.



## How do I scan paper?

I have a portable document scanner that I use to scan my paper.
It's a Canon ImageFORMULA P-215:

((image))

When I want to scan a document, I separate the pages and place them face down in the scanner.
It automatically pulls in the pages one at a time, and scans both sides at once -- I don't have to feed it pages individually.
If I'm scanning a long document, I can leave it unsupervised, and it works through the whole pile.

It connects to my Mac with a micro-USB.
Newer scanners have Wi-Fi, which is especially useful if you use it with a laptop or mobile device -- mine stays on my desk, so less of an issue for me.

I use the bundled scanning software, so I don't need to install anything on my computer.
The software is basic, but works well:

((screenshot))

The software can recognise printed text, and it performs OCR on the scans.
This means the PDF contains both an image and a transcription of the text, which I can search for later.

I've used this scanner for over six years, and it's always worked reliably.
I bought it for £225, and it looks like prices haven't changed much -- the portable scanner market isn't a hotbed of innovation.
When this unit fails, I'll likely replace it with whatever Canon's newest model is.

The quality of the scans isn't amazing.
In particular, the colour reproduction isn't great, and the pages are sometimes shown at a skewed angle.
It's fine for home scans of black-and-white printed documents, but if you're digitising photographs or archival material, it might not be such a great fit.
This is for speed and convenience, not quality.

There are scanning apps for smartphones, but they depend on the quality of your camera, and you need to photograph each page individually.
I've scanned nearly 24,000 pages with this scanner, and I wouldn't want to try that with a phone.



## How do I want to search my files?

Once I've used the scanner, I have a folder full of PDF files with vague filenames.
For anything more than a few files, this gets messy -- how do I organise them so I can find documents later?

(( screenshot ))

When I was designing docstore, it was useful to think about the type of searches I might want to make -- if I'm building a system just for me, it should suit my use case!
Here are some examples of questions I've asked recently:

*   _Can I find a recent utility bill?_
	  This is often used as a proof of address.

*   _Where was I living three years ago?_
	  When I'm applying to rent a flat, letting agents want to know where I've lived for the last three years.
	  It's easier to find the move-in papers and name of the estate agent, than try to recall from memory.

*   _What were the results of my last eye test?_
	  When I go for an eye test, I take the results from my last test, so I can see if my eyesight has changed recently.

*   _Does ACME Corp have my new address?_
	  When I move house, companies usually send me a letter to confirm they've got up my new address.
	  If I can't remember whether I've given a company my new address, I look at recent letters they've sent me, and which address they were sent to.

*   _What are my travel plans for my next trip?_
	  When I travel, I like to have printed copies of my tickets and accommodation notes (even if they were originally sent by email).
	  Even if my phone is stolen, lost, or out of battery in a strange place, I can still get around.

So typically I want to find documents within some loose categories, and then maybe narrow my search by date.
With those searches in my mind, let's thing about how I might organise the files.



## How should I organise my files?

Most computers support organising files with directories.
A directory is a collection of related files, and you can put directories inside other directories to create a hierarchy of files.
This is like managing physical pieces of paper: you put a page in a folder, a folder in a filing cabinet, the filing cabinet in an aisle, and so on.

This gives us a tree-like view of our files:

((screenshot))

I've tried to sort my PDFs this way a couple of times, but it's never stuck.
I always run into the same issue: what's the "right" set of folders to create?

Each file has one and exactly one place in a hierarchy.
I have to pick a way to sort my files, and I can only make searches that fit that classification.
I can't make searches that span multiple directories.

An example: suppose I have an electricity bill.
Do I put it in a folder called "home", or "utility bills", or a folder with the name of the provider?
I might want to search for it later by any of those criteria, but I can only put it one directory.

<figure style="width: 600px;">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 330 120" fill="rgba(0,0,0,0)">
  <circle cx="55" cy="50" r="40" stroke="#d01c11" stroke-width="2" fill="rgba(208, 28, 17, 0.18)"/>
  <text x="55" y="112" fill="#d01c11" text-anchor="middle" font-size="0.8em;">home</text>

  <circle cx="165" cy="50" r="40" stroke="#11a01c" stroke-width="2" fill="rgba(17, 160, 28, 0.18)"/>
  <text x="165" y="112" fill="#11a01c" text-anchor="middle" font-size="0.8em;">utility bills</text>

  <circle cx="275" cy="50" r="40" stroke="#0C34D4" stroke-width="2" fill="rgba(12, 52, 212, 0.18)"/>
  <text x="275" y="112" fill="#0C34D4" text-anchor="middle" font-size="0.8em;">acme energy</text>
</svg>
<figcaption>
Imagine each circle in this Venn diagram is a directory.
There's no overlap between <em>home</em>, <em>utility bills</em>, and <em>acme energy</em> &mdash; I have to pick a single directory, and I can only put my file in that directory.
</figcaption>
</figure>

So if I don't want to use files and folders, what else can I try?

Something I've used in other systems is keyword tagging, and that works much better for my brain.
When I store something, I add a number of "tags" – one or more keywords that describe the document.
Later, I can filter to find documents that have particular tags as a form of search.

I once heard tags described as a ["search engine in reverse"], and it's a nice metaphor.
I'm adding the keywords that I'll likely use to search for something later.
If I think I might look for something in three different ways, I can give it three different tags.

Consider the electricity bill again.
Rather than putting it in a single folder, I could tag it with "home" and "utility bills" and "acme energy", and I could find it later by searching for any one of those tags.

<figure style="width:600px;">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 330 165" fill="rgba(0,0,0,0)">
  <circle cx="140" cy="50" r="40" stroke="#d01c11" stroke-width="2" fill="rgba(208, 28, 17, 0.18)"/>
  <text x="95" y="40" fill="#d01c11" text-anchor="end" font-size="0.8em">home</text>

  <circle cx="190" cy="50" r="40" stroke="#11a01c" stroke-width="2" fill="rgba(17, 160, 28, 0.18)"/>
  <text x="236" y="40" fill="#11a01c" text-anchor="start" font-size="0.8em">utility bills</text>

  <circle cx="165" cy="96.650635095" r="40" stroke="#0C34D4" stroke-width="2" fill="rgba(12, 52, 212, 0.18)"/>
  <text x="165" y="157" fill="#0C34D4" text-anchor="middle" font-size="0.8em">acme energy</text>

  <circle cx="165" cy="66.650635095" r="5" fill="black"/>
</svg>
</figure>

It helps that I have a good model of tagging to emulate.
Tagging is very popular in the world of fandom.
On bookmarking sites like Pinboard and Delicious, fans have created intricate systems of tags to describe fanfiction, and by combining tags you can make very specific queries.
There are shared conventions to describe word count, the fandom, the pairing, the trope, and many other things beside -- you can even search bookmarks that were tagged by somebody else.
For examples, I really recommend Maciej Cegłowski's talk [Fan is a Tool-Using Animal].

I use tagging in my Pinboard account, so I'm quite used to it, and I know I like it.
I decided to use tagging as the basis for my PDF organisation.



## Creating an app to tag my PDFs

At a minimum, I want a PDF organiser that:

* Lets me store a file and give it some tags
* Shows me all the tags I've used
* Lets me find all the documents with a particular set of tags

This is similar to other tools I've built before -- I've built lot of variants of an image organiser that uses tags.
I chose to write it in Python, because that's the language I'm most familiar with, and it let me get started quickly, but you could implement this idea in a lot of languages.
(If I was starting fresh today, I'd be tempted to write it in Rust.)

I built the initial prototype with the [responder web framework](https://github.com/taoufik07/responder).
That was a year ago, and I got the core features working in a few hours -- then I've been adding polish and new features ever since.

I've recently switched to the more popular [Flask](https://pypi.org/project/Flask/), which is a great library for writing small web apps.
(If you aren't familiar with it, start with Miguel Grinberg's [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).)

I have a bunch of libraries doing the heavy lifting, including:

* pdftocairo and ImageMagick to create thumbnails
* whitenoise for serving static files
* python-magic and mimetypes to detect the type of a file
* hyperlink for manipulating URL query parameters

The whole app is packaged in a Docker image, to make deployments easy.
I can just as easily run it on my Linux web server as on my home Mac.
If you have Docker installed, you can run it like so:

```console
$ docker run --publish 8072:8072 --volume /path/to/documents:/documents greengloves/docstore
```

This starts the web app running on <http://localhost:8072>, and any files you upload will be saved to `/path/to/documents`.

If you'd like to read the source code, it's all available [on GitHub](https://github.com/alexwlchan/docstore).



## How do you use docstore?

For simplicity, docstore only has a single screen.
Here's what it looks like, storing some of my ebooks:

(( screenshot ))

Most of the screen is taken up with a list of documents.
Each document has a one-line description, a thumbnail, and some metadata.

The thumbnails make it easy to identify a document at a glance -- book covers are particularly good for this, but it works in letters too.
Companies tend to use consistent letterheads, so I learn to spot that particular letterheads as I'm scrolling a list.

The metadata includes the date I saved something (not necessarily the date of the document itself -- I scanned a lot of stuff long before I saved it in docstore), and a list of tags.
If I click one of the tags, it filters the documents to ones that have that tag.
Tags stack, so if I click "programming" and then "programming:python", I'll only see documents that have both of those tags.

There are options to sort by title or by date:

(( screenshot ))

There are two buttons on the top of the screen.
The first, "Store document", opens the form for adding a new document.
It's a fairly standard web form:

(( screenshot ))

Although I originally built this to handle scanned PDFs, I get a lot of correspondence electronically -- for example, I get my bank statements from an online portal, not in the post.
I want to keep all those documents in the same place, so the source URL lets me track where I downloaded a file from.

The second button, "Show tags", shows a list of tags in the current view.
Clicking any one of the tags will filter the documents to ones that have that tag:

(( screenshot ))

This list is context-dependent: if I've already applied a tag query, it shows me the list of tags for documents that match my query.
For example, if I selected the "programming" tag, I'd only see the tags used by files that are tagged with "programming".



## Implementation details

I wrote this app for personal use.
There's only a single user (me), and I'm only using it to store a few thousand documents at most.
That lets me ignore lots of hard problems around scaling, trusted input, concurrent reads and writes -- and the code is simpler for it.

There are a few interesting design choices, which work well in the context of a personal tool, but you shouldn't use in larger software.

### Storing the individual PDF files

When I save a file to disk, I normalise the filename into something computer-friendly.
This means stripping out all the special characters, lowercasing the whole name, and replacing spaces with hyphens.
The files get sorted into directories based on their first letter.
(( ASCIIFYING ))
Something like:

```
files
 ├─ a
 │   ├─ advice-for-renters.pdf
 │   └─ alex-chan-contract.pdf
 └─ b
     ├─ breakdown-cover-ipid-document.pdf
     └─ british-gas-terms-and-conditions.pdf
```

If you download a file, I use the Content-Disposition HTTP header to send the original filename -- so this normalisation is completely hidden from the user.

Initially I was using UUIDs for filenames, but they're quite opaque.
This way keeps the filenames computer-friendly, but still close to the original, so they'll stay usable if you stop using docstore but lose the database.

If you upload a file with the same name twice, I append a random string to the filename to avoid clashes.
Something like:

```
files
 └─ a
     ├─ advice-for-renters.pdf
     └─ advice-for-renters_a187b.pdf
```

The thumbnails are kept in a separate folder -- they're less important than the original files, and I don't want to mix them up.

### Storing the metadata

All the metadata is kept in a single JSON file.
JSON means it's human-readable and human-editable, and not tied to any particular software or language.
Here's what it looks like:

```json
{
  "000914e9-be70-4d11-bba5-6c902e9bcb44": {
    "filename": "Advice for renters.pdf",
    "file_identifier": "a/advice-for-renters.pdf",
    "checksum": "sha256:8b9...b40",
    "date_created": "2019-11-25 00:05:52 +0000",
    "tags": [
	  "home:renting",
	  "home:123-sesame-street"
    ],
    "thumbnail_identifier": "0/000914e9-be70-4d11-bba5-6c902e9bcb44.jpg",
    "title": "2019-11: Advice for renters"
  },
  ...
}
```

I use UUIDs as IDs, which is a holdover from an early version -- right now they're only used to identify the thumbnail images.
I could probably get away with storing a list of documents, but it's not worth changing.

When I upload a file, the app records a SHA256 checksum.
These documents should all be immutable, so this is a way to spot file corruption.

When the app starts, it loads the entire JSON file into memory.
It also polls the file periodically, and if it detects a change, it reloads the file.
This would cause issues if I was running at large scale, but for a few thousand documents this isn't a problem.

### Finding documents with a given set of tags

I query documents with a Python list comprehension:

```python
query = [
    "utilities",
    "home:123-sesame-street",
]

matching_documents = [
    doc
    for doc in documents
    if all(query_tag in doc.get("tags", []) for query_tag in query)
]
```

You could use a fancier data structure, or a database join, or something else, but this is fast enough for a small number of documents that it's not an issue.
Because all the documents are already in memory, it takes fractions of a millisecond to query thousands of documents.



## My current procedure

When I get a piece of paper, this is what I do with it:

1. I scan it with my document scanner, and get a PDF
2. I upload the PDF to docstore, adding some appropriate tags
3. If the page has sensitive information, like my bank details, I shred it. If it's not sensitive, say marketing material, it goes in the paper recycling.

I try to scan everything the day I get it, so I don't build up a backlog.
When I was first starting, I made a big pile of all the paper I wanted to scan, and worked through it in big batches.
It took months to get through everything, but now pretty much all my paper has been scanned and organised with docstore.

I use semi-structured tags, with a common prefix to group similar tags.
Here are some examples of what my tags look like:

* bank:credit-card-4567
* car:austin-WLG142E
* health:optician
* home:667-dark-avenue
* payslips
* providers:bulb-energy
* travel
* utilities:water

I run several instances of docstore:

*   Home correspondence. Letters, manuals, insurance documents, that sort of thing.
*   Manuals and reference documents.
    Whenever I get a new appliance, I download the manual from the manufacturer website.
    Docstore makes it easy to find, and then I can to full-text search on the PDF to answer specific questions.
*   Old schoolwork. I haven't looked at some of my school books in over a decade, so I recently scanned it and recycled the paper.  I don't want it in my main instance, but it's nice to know it's catalogued and available if I ever want to read it.
*   Work documents. I run an instance on my work laptop, so I can manage any documents I need for work in the same way -- but the files never leave the corporate network.

Collectively, I've got 1585 PDFs with 23,795 pages, and most of the original paper has now been recycled.
It's a big saving!



## Get the code

can get code on GitHub, MIT license, and can run in Docker so fairly simple to deploy: https://github.com/alexwlchan/docstore



## Interesting links

* [Designing better file organization around tags, not hierarchies](https://www.nayuki.io/page/designing-better-file-organization-around-tags-not-hierarchies)
* Fan is a Tool-Using Animal ([video](https://vimeo.com/88001038), [transcript](https://idlewords.com/talks/fan_is_a_tool_using_animal.htm))
* [Digital Preservation at Wellcome](https://stacks.wellcomecollection.org/digital-preservation-at-wellcome-3f86b423047)
* [Situated Software](https://www.drmaciver.com/2018/11/situated-software/)
