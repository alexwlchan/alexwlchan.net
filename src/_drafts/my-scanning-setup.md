---
layout: post
title: How I scan and organise my paperwork
summary:
---

If you follow me on Twitter, you'll see I often tweet about scanning my paperwork.

I scan all the letters I receive, and I organise the digital copies in an app I created called _docstore_.
The app lets me store and search my documents using keyword tags

Whenever I receive a letter or a bill, I scan it and save it.
Digital documents are easier to search, and when everything is scanned, I can get rid of the paper copies.
I keep the original paper for some things -- but mostly I scan or recycle the paper, and save the space on my shelves.

People often ask about how I do my scanning, and how I organise the scanned files -- in this post, I'm going to explain how I came to my current setup.

The post is quite long, so here's a table of contents:

* Table of contents
{:toc}


## How do I scan paper to PDF?

I have a small document scanner that creates PDFs from the scanned pages.
It's a [Canon ImageFORMULA P-215]:

<figure>
  <img src="/images/2019/canon_scanner.jpg" alt="A black document-feed scanner sitting on a wooden desk.">
  <figcaption>With an A5 sheet of paper for comparison.</figcaption>
</figure>

When I'm scanning something, I separate the pages, and place them face-down in the scanner.
It pulls in the pages one at a time, and scans both sides at once.
It's a bit slow, but normally I can leave it to scan without supervision -- I don't have to feed in each page individually.

I connect it to my Mac with a single USB cable.
I use the scanning software that's bundled with the scanner, so I don't have to install anything on my computer.
The software is basic, but works well.

<img src="/images/2019/canon_scanner.png" alt="Screenshot of scanning software. A preview of the page is shown in the centre, with some action buttons along the bottom of the window.">

The software has a nice big preview of the scanned images, so I can check it's scanning correctly.
I can rearrange pages if they're in the wrong order, or remove a page if I don't want it saved.
I can also adjust the rotation of the pages -- the scanner tries to guess the correct orientation, but I can correct the page if it guesses wrong.

The software is also doing [optical character recognition (OCR)][OCR] on the text.
The PDF it produces contains both an image and a transcription of any printed text.

I've used this scanner for over six years, and never had any issues.
My particular model cost £225 in 2013.
It's been discontinued, but replacement models are available for a similar price.
When this one fails, I'll likely replace it with another Canon.

The quality of the scans isn't amazing.
In particular, the colour reproduction isn't great, and the pages are sometimes shown at a skewed angle.
It's fine for home scans of black-and-white printed documents, but if you're digitising photographs or archival material, it might not be such a great fit.
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

Before I wrote a line of code, I wanted to think about how to organise my PDFs.

When I've got all my documents, I want to be able to find everything about a particular topic.
For example, every bill from one company, or everything about a place I'd lived, or all my tax paperwork.
Sometimes I'm looking for a specific document, sometimes I'm looking for a collection of files.

How do I organise my files to enable that type of searching?

There are a couple of possibilities -- let's consider them in turn.

### Storing files in a hierarchy

Most modern computers use a hierarchical file system.
We can put related files in a collection, called a *directory* or *folder*.
We can also put directories inside other directories, which creates a hierarchy of information. 
This is analogous to managing physical pieces of paper – you put a page in a folder, the folder in a filing cabinet, the filing cabinet in an aisle, the aisle in a room, and so on.

This gives us a tree-like view of files that might look familiar:

```
documents
 ├─ bills
 │   ├─ electricity-bill.pdf
 │   └─ water-bill.pdf
 └─ health
     ├─ optician
     │   └─ eye-test.pdf
     └─ nhs
         └─ welcome-to-gp.pdf
```

Because hierarchical file systems are ubiquitous, this would be easy to implement -- I just create the right set of folders in Finder.
But what are the "right" set of folders?
This turns out to be quite a hard question.

Each file has one and exactly one place in a hierarchy.
I have to pick a way to sort my files, and I can only make searches that fit that classification.
I can't make searches that span multiple directories.

An example: suppose I have an electricity bill.
Do I put it in a directory called "home", or "utility bills", or a directory with the name of the provider?
I might want to find it later by any of those criteria, but I can only put it one directory.
A hierarchy doesn't give me the flexibility to find documents the way I want.

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

A second example: there's a passage from a book I read years ago that's stuck with me, which illustrates the problem of a hierarchy when the classification rules aren't clear.
Hal is the librarian, and Klaus is helping him organise incoming paperwork:

> [Hal] paused, unclipped a small stack of paper, and squinted at the top page. "For instance," he continued, "You only have to read a few words to see that these paragraphs are about the weather last week at Damocles Dock, which is on the shore of some lake someplace. So you would ask me to unlock cabinets in aisle D, for Damocles, or W, for weather, or even P, for paragraphs. It's your choice."
>
> "But won't it be difficult for people to find that information again?" Klaus asked. "They won't know whether to look under D, W, or P."
>
> "Then they'll have to look under all three letters," Hal said. "Sometimes the information you need is not in the most obvious place."
> 
> <p class="cite"><cite><em>The Hostile Hospital</em>, by Lemony Snicket</cite></p>

When Klaus starts filing his own paperwork, he's going to have to invent some rules.
And because there isn't a definitive ruleset, he'll have to re-evaluate the rules every time he files something new.
Are the rules still consistent?
Do they still make sense?
Does he need some new cabinets or folders?
And so on.

This is what happens whenever I try to sort files into folders -- I'm constantly rethinking it, trying to come up with the "best" classification system.
It becomes a low-level mental drag, and it's tempting to start fiddling with the folder structure to get the "right" arrangement.

It's possible to come up with a good classification system that puts every file in a single directory, but it takes a lot of upfront thought and design.
Libraries can only put a book on one place on the shelf, so they use [Dewey Decimal] -- but somebody had to design it first.

I've tried using files and folders a couple of times, but it never stuck.
Between the inflexible search, and the ambiguous filing, it's not a good fit for me.

[Dewey Decimal]: https://en.wikipedia.org/wiki/Dewey_Decimal_Classification

### Searching an unorganised pile of files

Hierarchies are a highly ordered system.
The opposite is to do no organisation at all -- just put all my files in a single directory, and use searching to find the right files.

An example: this is how I manage my email: I have 26,000 emails in a single "Archive" folder, and I use the search function to find the email I want.
I can search by attributes (say, messages from a particular sender), or do full text search on the body of the message, and I usually find the message I want pretty quickly.

Another example: search is how I find pretty much everything on the web -- I ask a search engine a question, and it shows me web pages that might be helpful.
(I've even written blog posts so they'll show up in search engine result the next time I look something up.
But I can only do that with something I can make public -- say, notes about programming, and not my bank statements.)

Unfortunately, I've never got along with the builtin Mac OS X file search.
There's not a specific reason, I just find it a bit slow and the 
search syntax has never clicked in my brain.

I could set up my own search system, but doing search well is hard, and it's not my speciality.
There are lots of ways a document search could be useful -- but it's more work than I wanted to put into this project.

### Keyword tagging

I've used several systems that organise objects with keyword tagging.
When I store something, I add a number of "tags" – one or more keywords that describe the document.
Later, I can filter to find documents that have particular tags as a form of search.

Recall an earlier example: my electricity bill.
Rather than filing it in a single directory, I could tag it with "home" and "utility bills" and "acme energy", and I could find it later by searching for any one of those tags.

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

Tagging is more flexible, both for searching and for storing.
I can add as many keywords as I think might be useful, and there's less overhead to creating a new tag.
And tagging is simpler to implement than full-text search.
Rather than matching on free text and ranking documents, it's a simple boolean: either a document has a particular tag, or it doesn't.

I like this idea of tags as a reverse search engine:

> I remember not knowing what [the tags field] was for. He explained it to me basically as a search engine in reverse. Rather than typing in something to find results, when you save something for later, why don’t you type down the the stuff that you’re going to probably use as keywords when you look for it long after it’s forgotten?
>
> <p class="cite"><cite><em>Fan is a Tool-Using Animal</em>, by Maciej Cegłowski</cite></p>

Tagging is particularly popular in the world of fandom.
On bookmarking sites like Pinboard and Delicious, fans have created intricate systems of tagging to describe fanfiction, and by combining tags you can make very specific queries.
A single fic could have tags for the word count, the fandom, the pairing, the trope, and many other things beside.
Maciej's talk has some examples.

I use tagging a lot in Pinboard, I'm quite used to it, and I find it easy to both save and search using tags.
I have 4.5k bookmarks and the tagging remains usable, so I know it scales.
I decided to use tagging as the basis for my document organisation.



## A brief spec

With tagging in mind, I came up with a brief spec for what I wanted.

I wanted a web app with three parts:

1. A form where I could upload new file, and tag it with keywords.
	When it gets uploaded, save the file somewhere on disk.
2. A list of all the files I've uploaded, and a way to view the original file.
3. A list of all the tags I've used, and a way to filter to documents with a given set of tags.

I started building a prototype in Python, which eventually became an app called [_docstore_](https://github.com/alexwlchan/docstore).
You can read more about it below, browse the source code on GitHub, or run it from [Docker Hub](https://hub.docker.com/r/greengloves/docstore).



## The front end

You can use docstore to manage arbitrary files -- scanned PDFs were the original idea, but any sort of PDF is fine.
Here's what it looks like with my ebook library:

<img src="/images/2019/docstore_screenshot.png">

In the default view, you see a list of documents, and you can click on the thumbnail or the title to see the original.
There are also buttons to see the "store a document" form, and a list of the current tags.
When you click the button, those panels expand into view.
Let's compare it to the spec above.

This is the form for uploading a new document.
It has fields for a human-readable title, tags and an optional source URL.
Sometimes I can download PDFs from online portals rather than getting a paper letter I have to scan, and I can record where I saved it in the source URL field.

<figure>
  <img src="/images/2019/docstore_upload_form.png" alt="A form titled 'Store a document' with fields 'Title', 'Tags', and 'Source URL'.">
  <figcaption>If I start typing something that looks like an existing tag, the tags field will offer to autocomplete for me.</figcaption>
</figure>

TODO: Rename "Submit" to "Store".

If you click "Submit", 

green banner or red banner

This is what the list of documents looks like:

<img src="/images/2019/docstore_document_list.png" alt="A list of five documents, showing a thumbnail on the left, plus a date stored, tags, and the source URL.">

I have code for creating thumbnails from PDFs ([with pdftocairo](/2019/09/creating-preview-thumbnails-of-pdf-documents/)), images ([with ImageMagick](https://imagemagick.org/index.php)), and ebooks in both [epub](https://github.com/alexwlchan/epub-thumbnailer) and [mobi](https://github.com/alexwlchan/get-mobi-cover-image) formats.
The thumbnails make it easy to identify a document at a glance -- book covers are particularly good for this, but it works in letters too.
Companies often use the same letterhead for everything they send me, so I learn to spot that as I'm scrolling a list.

The title field is meant to be human-readable, even if it includes characters that aren't suitable in a filename.
This is my one-line description of the document.

Clicking on the title or the thumbnail opens the original document.

Below the title is a bit of metadata -- when I uploaded the document, any tags I've attached, and the source URL (if provided).
The source URL is a clickable link, and clicking on the tags will filter the documents on the page to ones that have that tag.

The document list is paginated, so it's not loading thousands of thumbnail images on every visit.

To help me find documents, there are options to sort by title or by upload date:

<figure>
  <img src="/images/2019/docstore_sorting.png" alt="A 'sort by' dropdown menu with four options: 'title (a-z)', 'title (z-a)', 'date created (newest first)' and 'date created (oldest first)'.">
  <figcaption>When I'm labelling a sort option, I much prefer explicit sort options to "ascending" or "descending". It always takes me a moment to work out which one I actually want, and half the time I pick wrong.</figcaption>
</figure>

Finally, here's the list of all the tags I've used.
This gives me a way to see what tags I've already used, and to quickly drill down into my documents:

<figure>
  <img src="/images/2019/docstore_tag_list.png">
  <figcaption>I use a colon in tags to create a mini-hierarchy, which is reflected in the tag list. For example, in the list above, I have three programming-related tags: <em>programming</em>, <em>programming:ruby</em>, and <em>programming:scala</em>.
  </figcaption>
</figure>



## Under the hood

What is this section?

### Libraries

The spec isn't complicated, and you could write this in a variety of programming languages.
I chose Python, because that's what I'm most comfortable using, but it's certainly not the only choice.
If I was starting today, I might consider using Rust as a learning exercise (and I'm still tempted to do a big rewrite at some point).

Because this is code that's storing important documents, it's heavily tested -- I have 100% branch and line coverage as a minimum.

I originally wrote the app with the [responder web framework](https://github.com/taoufik07/responder), but the library wasn't being properly maintained, so I switched to the more popular [Flask](https://pypi.org/project/Flask/).
This is a great library for writing small web apps.
If you aren't familiar with it, start with Miguel Grinberg's [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

I have a bunch of libraries doing the heavy lifting, including:

* pdftocairo and ImageMagick for the thumbnailing
* whitenoise for serving static files
* python-magic and mimetypes to detect the type of a file
* hyperlink for manipulating URL query parameters

The whole app is packaged in a Docker image, for simple deployments.
I can just as easily run it on my Linux web server as on my home Mac.

### Storing the individual PDF files

When I save a file to disk, I normalise the filename into something computer-friendly.
This means stripping out all the special characters, lowercasing the whole name, and replacing spaces with hyphens.
The files get sorted into directories based on their first letter.
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

If you download a file, I use the Content-Disposition header to send the original filename -- this normalisation should be completely hidden from the user.
The internal filenames are still close to the original, so they'll stay usable if you decide to stop using docstore.

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

The original filename is recorded, so it can be returned later.

When I upload a file, the app records a SHA256 checksum.
These documents should all be immutable, so this is a way to spot file corruption.

The title is meant to be human readable, and can include characters that are difficult to put in filenames: things like spaces, slashes and colons.

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

### Limitations to scaling

This app is designed for me to store my personal documents.
It's not meant to be a high-scale, multi-user document manager.
There are lots of ways it would fall over if used at scale:

* JSON isn't a database, and holding the JSON in memory is unsustainable. As you add more documents, reading/writing the JSON would take longer and longer, and eventually there'd be too many documents to hold in memory. You'd need to rewrite it to use a proper database.
* There's no encryption or built-in security controls. I only run this on machines I trust -- if you have access to those machines, I'm already screwed.
* I've only ever tested with one user at a time (me). There's no way to split documents between different users, and I don't know how the Flask server would hold up if more than one person tried to use it at once.

In short: don't expect a hosted version any time soon.

This isn't a bad thing.
It's okay to write software that doesn't scale, if you know it will never be asked to.
I know I'm only ever going to run this as single-user instances, so I made choices to keep the code simple, rather than support a use-case I'd never use.



## My current procedure

When I get a piece of paper, this is what I do with it:

1. I scan it with my document scanner, and get a PDF
2. I upload the PDF to docstore, adding some appropriate tags
3. If the page has sensitive information, like my bank details, I shred it. If it's not sensitive, say marketing material, it goes in the paper recycling.

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

* Home correspondence. Letters, manuals, insurance documents, that sort of thing.
* Old schoolwork. I haven't looked at some of my school books in over a decade, so I recently scanned it and recycled the paper.  I don't want it in my main instance, but it's nice to know it's catalogued and available if I ever want to read it.
* Work documents. I run an instance on my work laptop, so I can manage any documents I need for work in the same way -- but the files never leave the corporate network.

Collectively, I've got 1585 PDFs with 23,795 pages, and most of the original paper has now been recycled. Nice saving!

<!-- stedwards = 352 / 9542
	 cambridge = 110 / 3653
	 berky = 47 / 1615
	 linode = 1076 / 8985 -->



## Do this yourself

can get code on GitHub, MIT license, and can run in Docker so fairly simple to deploy: https://github.com/alexwlchan/docstore



## Interesting links

* [Designing better file organization around tags, not hierarchies](https://www.nayuki.io/page/designing-better-file-organization-around-tags-not-hierarchies)
* Fan is a Tool-Using Animal ([video](https://vimeo.com/88001038), [transcript](https://idlewords.com/talks/fan_is_a_tool_using_animal.htm))
* [Digital Preservation at Wellcome](https://stacks.wellcomecollection.org/digital-preservation-at-wellcome-3f86b423047)
* [Situated Software](https://www.drmaciver.com/2018/11/situated-software/)
