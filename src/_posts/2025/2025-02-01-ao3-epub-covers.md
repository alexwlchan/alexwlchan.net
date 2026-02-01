---
layout: post
date: 2025-02-01 22:28:59 +00:00
title: Adding auto-generated cover images to EPUBs downloaded from AO3
summary: I built a handy tool to generate cover images for stories downloaded from AO3, making them easier to browse. Along the way, I learnt about how EPUBs work, the power of static sites, and some gotchas of async JavaScript.
tags:
  - ao3
  - epub
  - my tools
---
I was chatting with a friend recently, and she mentioned an annoyance when reading fanfiction on her iPad.
She [downloads fic from AO3][ao3_downloads] as EPUB files, and reads it in the Kindle app -- but the files don't have a cover image, and so the preview thumbnails aren't very readable:

{%
  picture
  filename="kindle_grid.png"
  width="600"
  class="screenshot"
  alt="A row of four document thumbnails, three of which are a preview of the text but too small to be readable, and the fourth is a generic ‘Doc’ icon with a short preview of the title ‘Whittled Down By…’."
%}

She's downloaded several hundred stories, and these thumbnails make it difficult to find things in the app's "collections" view.

This felt like a solvable problem.
There are tools to add cover images to EPUB files, if you already have the image.
The EPUB file embeds some key metadata, like the title and author.
What if you had a tool that could extract that metadata, auto-generate an image, and use it as the cover?

So I built that.
It's a small site where you upload EPUB files you've downloaded from AO3, the site generates a cover image based on the metadata, and it gives you an updated EPUB to download.
The new covers show the title and author in large text on a coloured background, so they're much easier to browse in the Kindle app:

{%
  picture
  filename="kindle_thumbnails_improved.png"
  width="600"
  class="screenshot"
  alt="Another row of four document thumbnails, each of which has a coloured background with the title in large white text, and the author name in slightly lighter text."
%}

If you'd find this helpful, you can use it at [alexwlchan.net/my-tools/add-cover-to-ao3-epubs/](https://alexwlchan.net/my-tools/add-cover-to-ao3-epubs/)
Otherwise, I'm going to explain how it works, and what I learnt from building it.

There are three steps to this process:

1.  Open the existing EPUB to get the title and author
2.  Generate an image based on that metadata
3.  Modify the EPUB to insert the new cover image

Let's go through them in turn.

[ao3_downloads]: https://archiveofourown.org/faq/downloading-fanworks



---



## Open the existing EPUB

I've not worked with EPUB before, and I don't know much about it.

My first instinct was to look for Python EPUB libraries [on PyPI][pypi], but there was nothing appealing.
The results were either very specific tools (convert EPUB to/from format X) or very unmaintained (the top result was last updated in April 2014).
I decied to try writing my own code to manipulate EPUBs, rather than using somebody else's library.

I had a vague memory that EPUB files are zips, so I changed the extension from `.epub` to `.zip` and tried unzipping one -- and it turns out that yes, it is a zip file, and the internal structure is fairly simple.
I found a file called `content.opf` which contains metadata as XML, including the title and author I'm looking for:

<pre><code>&lt;?xml version='1.0' encoding='utf-8'?&gt;
&lt;package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id"&gt;
  &lt;metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata"&gt;
    <mark>&lt;dc:title&gt;Operation Cameo&lt;/dc:title&gt;</mark>
    &lt;meta name="calibre:timestamp" content="2025-01-25T18:01:43.253715+00:00"/&gt;
    &lt;dc:language&gt;en&lt;/dc:language&gt;
    <mark>&lt;dc:creator opf:file-as="alexwlchan" opf:role="aut"&gt;alexwlchan&lt;/dc:creator&gt;</mark>
    &lt;dc:identifier id="uuid_id" opf:scheme="uuid"&gt;13385d97-35a1-4e72-830b-9757916d38a7&lt;/dc:identifier&gt;
    &lt;meta name="calibre:title_sort" content="operation cameo"/&gt;
    &lt;dc:description&gt;&lt;p&gt;Some unusual orders arrive at Operation Mincemeat HQ.&lt;/p&gt;&lt;/dc:description&gt;
    &lt;dc:publisher&gt;Archive of Our Own&lt;/dc:publisher&gt;
    &lt;dc:subject&gt;Fanworks&lt;/dc:subject&gt;
    &lt;dc:subject&gt;General Audiences&lt;/dc:subject&gt;
    &lt;dc:subject&gt;Operation Mincemeat: A New Musical - SpitLip&lt;/dc:subject&gt;
    &lt;dc:subject&gt;No Archive Warnings Apply&lt;/dc:subject&gt;
    &lt;dc:date&gt;2023-12-14T00:00:00+00:00&lt;/dc:date&gt;
  &lt;/metadata&gt;
  …</code></pre>

That `dc:` prefix was instantly familiar from my time working at Wellcome Collection -- this is [Dublin Core][dc], a standard set of metadata fields used to describe books and other objects.
I'm unsurprised to see it in an EPUB; this is exactly how I'd expect it to be used.

I found an article that explains the [structure of an EPUB file][structure], which told me that I can find the `content.opf` file by looking at the `root-path` element inside the mandatory `META-INF/container.xml` file which is every EPUB.
I wrote some code to find the `content.opf` file, then a few [XPath] expressions to extract the key fields, and I had the metadata I needed.

[pypi]: https://pypi.org/search/?q=epub
[dc]: https://en.wikipedia.org/wiki/Dublin_Core
[structure]: https://www.edrlab.org/open-standards/anatomy-of-an-epub-3-file/
[XPath]: https://developer.mozilla.org/en-US/docs/Web/XPath

## Generate a cover image

I sketched a simple cover design which shows the title and author.

I wrote the [first version of the drawing code][pydraw] in [Pillow], because that's what I'm familiar with.
It was fine, but the code was quite flimsy -- it didn't wrap properly for long titles, and I couldn't get custom fonts to work.

<style>
  .covers {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    width: 600px;
    grid-gap: 1em;
    margin-left:  auto;
    margin-right: auto;
  }
</style>

<div class="covers">
  {% picture width="150" alt="" filename="py_LordOfTheFiles.png" %}
  {% picture width="150" alt="" filename="py_PrideAndPlotBunnies.png" %}
  {% picture width="150" alt="" filename="py_KudosOfMonteChristo.png" %}
  {% picture width="150" alt="" filename="py_WaitingForGoncharov.png" %}
</div>

Later I rewrote the app in JavaScript, so I had access to the [HTML canvas element][canvas].
This is another tool that I haven't worked with before, so a fun chance to learn something new.
The API felt fairly familiar, similar to other APIs I've used to build HTML elements.

This time I did implement some line wrapping -- there's a [`measureText()` API][measureText] for canvas, so you can see how much space text will take up before you draw it.
I break the text into words, and keeping adding words to a line until `measureText` tells me the line is going to overflow the page.
I have lots of ideas for how I could improve the line wrapping, but it's good enough for now.

I was also able to get fonts working, so I picked Georgia to match the font used for titles on AO3.

Here are some examples:

<div class="covers">
  {% picture width="150" alt="" filename="cv_Ficard.png" %}
  {% picture width="150" alt="" filename="cv_CoffeeShop.png" %}
  {% picture width="150" alt="" filename="cv_ShipHappens.png" %}
  {% picture width="150" alt="" filename="cv_FastestFluffiest.png" %}
</div>

I had several ideas for choosing the background colour.
I'm trying to help my friend browse her collection of fic, and colour would be a useful way to distinguish things -- so how do I use it?

I realised I could get the fandom from the EPUB file, so I decided to use that.
I use the fandom name as a seed to a random number generator, then I pick a random colour.
This means that all the fics in the same fandom will get the same colour -- for example, all the Star Wars stories are a shade of red, while Star Trek are a bluey-green.

This was a bit harder than I expected, because it turns out that JavaScript doesn't have a built-in seeded random number generator -- I ended up using some snippets from [a Stack Overflow answer][rng], where bryc has written several pseudorandom number generators in plain JavaScript.

I didn't realise until later, but I designed something similar to the placeholder book covers in the Apple Books app.
I don't use Apple Books that often so it wasn't a deliberate choice to mimic this style, but clearly it was somewhere in my subconscious.

{%
  picture
  filename="apple_books.png"
  width="600"
  class="screenshot"
  loading="lazy"
  alt="A row of four books with placeholder covers. Each cover is a coloured gradient with the title and author shown in white sans serif text."
%}

One difference is that Apple's app seems to be picking from a small selection of background colours, whereas my code can pick a much wider variety of colours.
Apple's choices will have been pre-approved by a designer to look good, but I think mine is more fun.

[pydraw]: /files/2025/draw_basic_cover.py
[canvas]: https://developer.mozilla.org/en-US/docs/Glossary/Canvas
[Pillow]: https://pypi.org/project/pillow/
[measureText]: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/measureText
[rng]: https://stackoverflow.com/a/47593316/1558022

## Add the cover image to the EPUB

My first attempt to add a cover image used [pandoc]:

```
pandoc input.epub --output output.epub --epub-cover-image cover.jpeg
```

This approach was no good: although it added the cover image, it destroyed the formatting in the rest of the EPUB.
This made it easier to find the fic, but harder to read once you'd found it.

<style>
  #pandoc_comparison {
    width: 400px;
    margin-left:  auto;
    margin-right: auto;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-column-gap: 1em;
  }

  #pandoc_comparison picture:nth-child(1) img {
    border-top-right-radius:    0;
    border-bottom-right-radius: 0;
  }

  #pandoc_comparison picture:nth-child(2) img {
    border-top-left-radius:    0;
    border-bottom-left-radius: 0;
  }

  #pandoc_comparison figcaption {
    grid-column: 1 / span 2;
  }
</style>

<figure id="pandoc_comparison">
  {%
    picture
    filename="pre_pandoc.png"
    alt="Screenshot of an e-reader, showing a series of headings and links for key metadata (rating, category, characters, and so on.)"
    width="300"
    class="screenshot"
  %}
  {%
    picture
    filename="post_pandoc.png"
    alt="Screenshot of the same page, but now all the formatting is gone and replaced by plain, unstyled text."
    width="300"
    class="screenshot"
  %}
  <figcaption>
    An EPUB file I downloaded from AO3, before/after it was processed by pandoc.
  </figcaption>
</figure>

So I tried to do it myself, and it turned out to be quite easy!
I unzipped another EPUB which already had a cover image.
I found the cover image in `OPS/images/cover.jpg`, and then I looked for references to it in `content.opf`.
I found two elements that referred to cover images:

<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="PrimaryID"&gt;
  &lt;metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf"&gt;
    <mark>&lt;meta name="cover" content="cover-image"/&gt;</mark>
    …
  &lt;/metadata&gt;
  &lt;manifest&gt;
    <mark>&lt;item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/&gt;</mark>
    …
  &lt;/manifest&gt;
&lt;/package&gt;</code></pre>

This gave me the steps for adding a cover image to an EPUB file: add the image file to the zipped bundle, then add these two elements to the `content.opf`.

[pandoc]: https://pandoc.org/

## Where am I going to deploy this?

I wrote the initial prototype of this in Python, because that's the language I'm most familiar with.
Python has all the libraries I need:

*   The [zipfile] module can unpack and modify the EPUB/ZIP
*   The [xml.etree] or [lxml] modules can manipulate XML
*   The [Pillow] library can generate images

I built a small Flask web app: you upload the EPUB to my server, my server does some processing, and sends the EPUB back to you.
But for such a simple app, do I need a server?

I tried rebuilding it as a static web page, doing all the processing in client-side JavaScript.
That's simpler for me to host, and it doesn't involve a round-trip to my server.
That has lots of other benefits -- it's faster, less of a privacy risk, and doesn't require a persistent connection.
I love static websites, so can they do this?

Yes!
I just had to find a different set of libraries:

*   The [JSZip] library can unpack and modify the EPUB/ZIP, and is the only third-party code I'm using in the tool
*   Browsers include [DOMParser] for manipulating XML
*   I've already mentioned the HTML [`<canvas>` element][canvas] for rendering the image

This took a bit longer because I'm not as familiar with JavaScript, but I got it working.

As a bonus, this makes the tool very portable.
Everything is bundled into a single HTML file, so if you download that file, you have the whole tool.
If my friend finds this tool useful, she can save the file and keep a local copy of it -- she doesn't have to rely on my website to keep using it.

[zipfile]: https://docs.python.org/3/library/zipfile.html
[xml.etree]: https://docs.python.org/3/library/xml.etree.elementtree.html
[lxml]: https://lxml.de/
[JSZip]: https://stuk.github.io/jszip/
[DOMParser]: https://developer.mozilla.org/en-US/docs/Web/API/DOMParser
[canvas]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas

## What should it look like?

My first design was very "engineer brain" -- I just put the basic controls on the page.
It was fine, but it wasn't good.
That might be okay, because the only person I need to be able to use this app is my friend -- but wouldn't it be nice if other people were able to use it?

{%
  picture
  filename="epub_design1.png"
  width="600"
  alt="My initial design. It's a basic web page with plain serif text and a couple of buttons."
  class="screenshot"
%}

If they're going to do that, they need to know what it is -- most people aren't going to read a 2,500 word blog post to understand a tool they've never heard of.
(Although if you have read this far, I appreciate you!)
I started designing a proper page, including some explanations and descriptions of what the tool is doing.

I got something that felt pretty good, including FAQs and acknowledgements, and I added a grey area for the part where you actually upload and download your EPUBs, to draw the user's eye and make it clear this is the important stuff.
But even with that design, something was missing.

I realised I was telling you I'd create covers, but not showing you what they'd look like.
Aha!
I sat down and made up a bunch of amusing titles for fanfic and fanfic authors,  so now you see a sample of the covers before you upload your first EPUB:

{%
  picture
  filename="epub_design2.png"
  width="600"
  alt="Screenshot of the app. There are some a few lines of instruction on a white background, then a grey rectangle where you upload files. There are four grayscale covers to show what they’ll look like."
  class="screenshot"
%}

This makes it clearer what the app will do, and was a fun way to wrap up the project.

---

## What did I learn from this project?

### Don't be scared of new file formats

My first instinct was to look for a third-party library that could handle the "complexity" of EPUB files.
In hindsight, I'm glad I didn't find one -- it forced me to learn more about how EPUBs work, and I realised I could write my own code using built-in libraries.
EPUB files are essentially ZIP files, and I only had basic needs.
I was able to write my own code.

Because I didn't rely on a library, now I know more about EPUBs, I have code that's simpler and easier for me to understand, and I don't have a dependency that may cause problems later.

There are definitely some file formats where I need existing libraries (I'm not going to write my own JPEG parser, for example) -- but I should be more open to writing my own code, and not jumping to add a dependency.

### Static websites can handle complex file manipulations

I love [static websites] and I've used them for a lot of tasks, but mostly read-only display of information -- not anything more complex or interactive.
But modern JavaScript is very capable, and you can do a lot of things with it.
Static pages aren't just for static data.

One of the first things I made that got popular was [find untagged Tumblr posts], which was built as a static website because that's all I knew how to build at the time.
Somewhere in the intervening years, I forgot just how powerful static sites can be.

I want to build more tools this way.

[static websites]: /2024/static-websites/
[find untagged Tumblr posts]: https://finduntaggedtumblrposts.com

### Async JavaScript calls require careful handling

The JSZip library I'm using has a lot of async functions, and this is my first time using async JavaScript.
I got caught out several times, because I forgot to wait for async calls to finish properly.

For example, I'm using `canvas.toBlob` to render the image, which is an async function.
I wasn't waiting for it to finish, and so the zip would be repackaged before the cover image was ready to add, and I got an EPUB with a missing image.
Oops.

I think I'll always prefer the simplicity of synchronous code, but I'm sure I'll get better at async JavaScript with practice.

---

## Final thoughts

I know my friend will find this helpful, and that feels great.

Writing software that's designed for one person is my favourite software to write.
It's not hyper-scale, it won't launch the next big startup, and it's usually not breaking new technical ground -- but it is useful.
I can see how I'm making somebody's life better, and isn't that what computers are for?
If other people like it, that's a nice bonus, but I'm really thinking about that one person.

Normally the one person I'm writing software for is me, so it's extra nice when I can do it for somebody else.

If you want to try this tool yourself, go to [alexwlchan.net/my-tools/add-cover-to-ao3-epubs/](https://alexwlchan.net/my-tools/add-cover-to-ao3-epubs/)

If you want to read the code, it's all [on GitHub].

[on GitHub]: https://github.com/alexwlchan/add-cover-to-ao3-files
