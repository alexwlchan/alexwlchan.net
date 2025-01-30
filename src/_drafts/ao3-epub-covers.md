---
layout: post
title: Adding auto-generated cover images to EPUBs downloaded from AO3
summary: I wrote a small tool to help a friend browse the fics she's downloaded from AO3. Adding colourful, readable covers makes it easier for her to find them in a grid.
tags:
  - ao3
  - epub
  - my tools
---

# Blog post

A friend wants a way to browse AO3 fics on her iPad
But no cover images!
(Explicitly disabled)

Felt like a solvable problem

There are already sites where you can add a cover image, what if you could extract title/author from fic and generate image directly?

So that's what I built:

[[screenshot]]

And makes it much easier to browse her Kindle now:

[[screenshot]]

You can try it, or read on to learn how I built it.

## How it works

Process takes three steps:

1. Open the existing ePub to get the title and author
2. Generate a cover image for this fic
3. Add the cover image to the ePub

Let's go through in turn

### Open the existing ePub

Have never worked with ePub before, don't know how it works
Looked for ePub libraries on PyPI, nothing appealing
Either very specific tools (convert ePUB to X) or very unmaintained (last updated April 2014)

Hmm… maybe I don't need a library?

Vague memory -- isn't an epub a zip?
Let's try unzipping it:

    unzip Operation_Cameo.epub

Oh! It is a zip with files inside it, sweet
Found a file called `content.opf` which contains metadata incl. title and author, for example:

    <?xml version='1.0' encoding='utf-8'?>
    <package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id">
      <metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata">
        <dc:title>Operation Cameo</dc:title>
        <meta name="calibre:timestamp" content="2025-01-25T18:01:43.253715+00:00"/>
        <dc:language>en</dc:language>
        <dc:creator opf:file-as="alexwlchan" opf:role="aut">alexwlchan</dc:creator>
        <dc:identifier id="uuid_id" opf:scheme="uuid">13385d97-35a1-4e72-830b-9757916d38a7</dc:identifier>
        <meta name="calibre:title_sort" content="operation cameo"/>
        <dc:description>&lt;p&gt;Some unusual orders arrive at Operation Mincemeat HQ.&lt;/p&gt;</dc:description>
        <dc:publisher>Archive of Our Own</dc:publisher>
        <dc:subject>Fanworks</dc:subject>
        <dc:subject>General Audiences</dc:subject>
        <dc:subject>Operation Mincemeat: A New Musical - SpitLip</dc:subject>
        <dc:subject>No Archive Warnings Apply</dc:subject>
        <dc:date>2023-12-14T00:00:00+00:00</dc:date>
      </metadata>

It's Dublin Core metadata!
Something I know about from my time working at Wellcome Collection

Wrote a function to find the `content.opf`
Initially searched by path, then discovered there's a `META-INF/container.xml` file that points to it

Then write XPath expressions to extract key fields

### Generate a cover image

Wanted to show title/author
Didn't realise until later, but this is similar to autogen covers in Apple Books

First attempt with Pillow, because that's what I'm more familiar with
They were fine:

[[ image ]]

But later rewrote app in JavaScript, so I had access to `<canvas>`
Had to write some code to handle line wrapping and long titles
Better:

[[ image ]]

How to choose background colour?
Idea: does colour matter, or consistency?
Use colour to communicate similarity: same fandom
Can get fandom from DC metadata as third subject (first two are "Fanworks" and rating)
Then use that as seed for RNG to choose colour

### Add the cover image to the EPUB

Tried using pandoc, no good
Different idea: let's look at an existing EPUB with a cover
FOund the cover image, then searched in `content.opf` for references:

    <<xml>>

Aha! Okay, so need to add to zip file and add these two references
Sweet

---

Lessons Learned

ePub files are essentially zip archives
Static websites can handle complex file manipulations
Async JavaScript calls require careful handling
JavaScript has no seeded random

## How do I build this?

### Is it a server or a static site?

We wrote the initial prototype on my sofa in Python
Because that's language I'm most familiar with
Python has all the libraries for it:

* zipfile module built in
* xml.etree for XML
* Pillow for generating images

And it could definitely work as a Flask web app: you upload the EPUB to my server, my server does some processing, you download the EPUB back

But such a simple app… do I need a server?

Before I put the prototype online, I tried rebuilding it as a static web page
Simpler for me to host, doesn't involve a round trip to my server (= less privacy invasive, faster, can do if Internet connection drops)
I love static websites, could they do this?
Yes!

* JSZip is a great zip library, only 3rd party dependency
* DOMParser for XML in browser
* Use <canvas> element to render the image

This took a bit longer because I'm not as familiar with JavaScript
And got caught out a few times with async calls that I didn't wait to finish properly
e.g. canvas.toBlob is async; if you don't wait the zip got repackaged before the cover image could be added, oops

as a bonus, this now makes the tool very portable
if my friend finds this tool useful, she can save the HTML file and have a local copy of it
she doesn't have to rely on my website to keep using it

### what should it look like?

my first design was very engineer brain -- just putting the basic controls on the page
and it was … fine
honestly, if my friend is the only person who ever uses it, that's okay
she will find it useful and that's plenty
[https://www.robinsloan.com/notes/home-cooked-app/]

but wouldn't it be nice if other people wanted to use it?
or could tell if they'd want to?
i started designing a proper landing page
wrote some actual prose to go with it

got most of the way there
added some FAQs explaining how it works, plus acknowledgements
used grey "well" area for user interaction -- to draw eye, make it clear this is important, and that's where covers appear

but somehow … missing something
realised I was telling you I'd create covers, but not showing you what they'd look like
aha!
sat down and wrote a bunch of pun titles and authors

[[screenshot]]

this was a super fun way to wrap up the project

---

i had fun writing this and i know my friend will find it useful, and that's what I want my software to do
writing software that will make one person's life better is among my favourite software to write
it's not hyper-scale, it won't launch the next big startup, it's not breaking new technical ground
but it's useful




==== TIL ====

---

How to find the content.opf file in an ePub

With alt tools:
    Find content.opf by looking in container.xml
    Write an XPath expression

    <?xml version="1.0"?>
    <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
       <rootfiles>
          <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>

       </rootfiles>
    </container>


---

How to add a cover image to an ePub

With pandoc:
    pandoc input.epub -o output.epub --epub-cover-image=cover.png

Boo:
    - big dependency
    - mangles formatting

Better:
    1. Add image to package
    2. Add reference to <manifest>:

        <item id="cover-image" properties="cover-image" href="media/cover.png" media-type="image/png"/>

    3. Add reference to <metadata>:

        <meta name="cover" content="cover-image"/>

---

How to find metadata about an ePub

1. Find the content.opf file, then you get Dublin Core metadata
2. e.g.

    <?xml version='1.0' encoding='utf-8'?>
    <package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id">
      <metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata">
        <dc:title>Operation Cameo</dc:title>
        <meta name="calibre:timestamp" content="2025-01-25T18:01:43.253715+00:00"/>
        <dc:language>en</dc:language>
        <dc:creator opf:file-as="alexwlchan" opf:role="aut">alexwlchan</dc:creator>
        <dc:identifier id="uuid_id" opf:scheme="uuid">13385d97-35a1-4e72-830b-9757916d38a7</dc:identifier>
        <meta name="calibre:title_sort" content="operation cameo"/>
        <dc:description>&lt;p&gt;Some unusual orders arrive at Operation Mincemeat HQ.&lt;/p&gt;</dc:description>
        <dc:publisher>Archive of Our Own</dc:publisher>
        <dc:subject>Fanworks</dc:subject>
        <dc:subject>General Audiences</dc:subject>
        <dc:subject>Operation Mincemeat: A New Musical - SpitLip</dc:subject>
        <dc:subject>No Archive Warnings Apply</dc:subject>
        <dc:date>2023-12-14T00:00:00+00:00</dc:date>
      </metadata>

3. Provide XPath expressions