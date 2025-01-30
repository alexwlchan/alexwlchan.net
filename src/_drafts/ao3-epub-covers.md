---
layout: post
title: Adding auto-generated cover images to EPUBs downloaded from AO3
summary: I wrote a small tool to help a friend browse the fics she's downloaded from AO3. Adding colourful, readable covers makes it easier for her to find them in a grid.
tags:
  - ao3
  - epub
  - my tools
---
I was chatting with a friend recently, and she mentioned an annoyance when reading fanfiction on her iPad.
She [downloads fic from AO3][ao3_downloads] as an EPUB file, and reads it in the Kindle app -- but AO3 downloads don't have a cover image, and so the preview thumbnails aren't very readable:

{%
  picture
  filename="kindle_grid.png"
  width="600"
  class="screenshot"
%}

She's downloaded several hundred stories, and these thumbnails are too small to be readable -- it's difficult to find things in the app's "collections" view.

This felt like a solvable problem.
There are already sites that allow you to add cover images to EPUB files -- if you already have the image.
The EPUB file embeds some key metadata, like the title and author.
What if you had a site that could extract that metadata, auto-generate the image, and add it as the cover?

So I built that.
It's a small site where you upload EPUB files you've downloaded from A3, and the site generates the cover image based on the metadata, and gives you a modified EPUB with the new cover image.
The new covers show the title and author in large text on a coloured background, and are much easier to browse in a grid:

[[screenshot]]

If you'd find this helpful, you can use it at [alexwlchan.net/my-tools/add-cover-to-ao3-epubs/](https://alexwlchan.net/my-tools/add-cover-to-ao3-epubs/)

Otherwise, I'm going to talk about how it works, and what I learnt from building it.
There are three steps to this process:

1.  Open the existing EPUB to get the title and author
2.  Generate a cover image for this fic
3.  Modify the EPUB to insert this image

Let's go through them in turn.

[ao3_downloads]: https://archiveofourown.org/faq/downloading-fanworks



---



## Open the existing EPUB

I've not worked with EPUB before, and I don't know much about it.

My first instinct was to look for Python EPUB libraries [on PyPI][pypi], but there was nothing appealing.
The results were either very specific tools (convert EPUB to format X) or very unmaintained (the top result was last updated in April 2014).
This made me wonder if I could just write my own code to manipulate EPUBs, rather than using somebody else's library.

I had a vague memory that EPUB files are zips, so I tried unzipping one -- and it turns out that yes, it is a zip file, and the internal structure is fairly simple.
I found a file called `content.opf` which contains metadata, including the title and author I'm looking for:

<pre><code>&lt;?xml version='1.0' encoding='utf-8'?&gt;
&lt;package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uuid_id"&gt;
  &lt;metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata"&gt;
    <strong>&lt;dc:title&gt;Operation Cameo&lt;/dc:title&gt;</strong>
    &lt;meta name="calibre:timestamp" content="2025-01-25T18:01:43.253715+00:00"/&gt;
    &lt;dc:language&gt;en&lt;/dc:language&gt;
    <strong>&lt;dc:creator opf:file-as="alexwlchan" opf:role="aut"&gt;alexwlchan&lt;/dc:creator&gt;</strong>
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

That `dc:` prefix was instantly familiar from my time working at Wellcome Collection -- this is [Dublin Core][dc], a standard set of metadata fields used to describe books and other things.

I found an article that explains the [structure of an EPUB file][structure], and that I can find the `content.opf` file by looking at the `root-path` element inside the mandatory `META-INF/container.xml` file which is every EPUB.
I wrote some code to find the `content.opf` file, then a few [XPath] expressions to extract the key fields, and I had the metadata I needed.

[pypi]: https://pypi.org/search/?q=epub
[dc]: https://en.wikipedia.org/wiki/Dublin_Core
[structure]: https://www.edrlab.org/open-standards/anatomy-of-an-epub-3-file/

## Generate a cover image

I sketched a simple cover design which shows the title and author.
I didn't realise until later, but this is very similar to the autogenerated book covers in the Apple Books app.

I wrote the first version of the drawing code in [Pillow], because that's what I'm familiar with.
It was fine, but the code was quite flimsy -- it didn't wrap properly for long titles, and I couldn't get custom fonts to work.

[[ image ]]

Later I rewrote the app in JavaScript, so I had access to the HTML `<canvas>` element.
This is another tool that I haven't worked with before, so a fun chance to learn something new.
The API felt fairly familiar, similar to other APIs I've used to build HTML elements.

This time I did implement some line wrapping -- there's a `getSize()` API in `<canvas>`, so you can see how much space text will take up before you draw it.
I break the text into words, and keeping adding words to a line until the line is going to overflow the page.
It's not the most sophisticated technique in the world, but it works well enough.

I was also able to get fonts working, so I picked Georgia to match the font used for titles on AO3.

Here are some examples:

[[ image ]]

I had several ideas for choosing the background colour.
I'm trying to help my friend browse her collection of fic, and colour would be a useful way to distinguish things -- but how to use it?

I realised I could get the fandom from the EPUB file, so I decided to use that.
I use the fandom name as a seed to a random number generator, then I pick a random colour.
This means that all the fics in the same fandom will get the same colour -- for example, all the Star Wars stories are a shade of red, while Star Trek are a bluey-green.

This was a bit harder than I expected, because it turns out that JavaScript doesn't have a built-in seeded random number generator -- I ended up using some snippets from [a Stack Overflow answer][rng], where bryc has written several pseudorandom number generators in plain JavaScript.

[rng]: https://stackoverflow.com/a/47593316/1558022

## Add the cover image to the EPUB

My first attempt to add a cover image used [pandoc]:

```
pandoc input.epub -o output.epub --epub-cover-image cover.jpeg
```

This approach was no good: although it added the cover image, it destroyed the formatting in the rest of the EPUB.
This made it easier to find the fic, but harder to read once you'd found it.

[[ screenshots ]]

So I thought about if I could do it myself, and it turned out to be quite easy!
I unzipped another EPUB I had on my computer which already had a cover image.
I found the cover image in `OPS/images/cover.jpg`, and then I looked for references to it in `content.opf`.
I found two elements that referred to cover images:

<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="PrimaryID"&gt;
   &lt;metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf"&gt;
       …
       <strong>&lt;meta name="cover" content="cover-image"/&gt;</strong>
   &lt;/metadata&gt;
   &lt;manifest&gt;
        <strong>&lt;item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/&gt;</strong>
        …
   &lt;/manifest&gt;
&lt;/package&gt;</code></pre>

This gave me a simple process for adding a cover image to an EPUB file: add the image file to the zipped bundle, then add these two elements to the `content.opf`.

## Where am I going to deploy this?

I wrote the initial prototype of this in Python, because that's the language I'm most familiar with.
Python has all the libraries I need:

*   The [zipfile] module is built-in for unpacking and modifying the EPUB/ZIP bundle
*   The [xml.etree] or [lxml] modules can manipulate XML
*   The [Pillow] library can generate images

And so I built a small Flask web app: you upload the EPUB to my server, my server does some processing, and sends the EPUB back to you.
But for such a simple app… do I need a server?

Before I put this online, I tried rebuilding it as a static web page, doing all the processing in client-side JavaScript.
That's simpler for me to host, and it doesn't involve a round-trip to my server, which has lots of other benefits -- it's faster, less of a privacy risk, and doesn't require a persistent connection.
I lovie static websites, so can they do this?

Yes!
I just had to pick a different set of libraries:

*   The [JSZip] library gives me the ability to process zips, and is the only third-party code
*   Browsers include DOMParser for manipulating XML
*   I've already mentioned the HTML `<canvas>` element for rendering the image
  
This took a bit longer because I'm not as familiar with JavaScript, but I got it working.

As a bonus, this now makes the tool very portable.
All the JavaScript is compiled into a single file, so if you download that file, you have the whole tool.
If my friend finds this tool useful, she can save the HTML file and have a local copy of it -- she doesn't have to rely on my website to keep using it.

## What should it look like?

My first design was very "engineer brain" -- I just put the basic controls on the page.
It was fine, but it wasn't good.
That might be okay, because the only person I need to be able to use this app is my friend -- but wouldn't it be nice if other people were able to use it?

If they're going to do that, they need to know what it is -- most people aren't going to read a 1000+ word blog post to understand a tool they've never heard of.
(Although if you have read this far, I appreciate you!)
I started designing a proper page, including some explanations and descriptions of what the tool is doing.

I got something that felt pretty good, including FAQs and acknowledgements, and I added a grey area for the part where you actually upload and download your EPUBs, to draw the user's eye and make it clear this is the important stuff.
But even with that design, something was missing.

I realised I was telling you I'd create covers, but not showing you what they'd look like.
Aha!
I sat down and made up a bunch of amusing titles for fanfic and fanfic authors,  so now you see a sample of the covers before you upload the first EPUB:

[[screenshot]]

This makes it much clearer what the app is doing, and was a fun way to wrap up the project.

---

## What did I learn from this project?

### Don't be scared of new file formats

My first instinct was to look for a third-party library that could handle the "complexity" of EPUB files.
In hindsight, I'm glad I didn't find one -- it forced me to learn more about how EPUBs work, and I realised I could write my own code using built-in libraries.
EPUB files are essential ZIP files, and I could write my own code for this basic use case.

Now I know a bit about EPUBs, I have code that's simpler and easier for me to understand, and I don't have a dependency that may cause me trouble later.

There are definitely some file formats where I need existing libraries (I'm not going to write my own JPEG library, for example) -- but I should be more open to writing my own code, and not jumping to add a dependency.

### Static websites can handle complex file manipulations

I love static websites and I've used them for a lot of tasks, but mostly read-only display of information -- not anything more complex or interactive.
But modern JavaScript is very capable, and you can do a lot of things with it.
Static pages aren't just for static data.

One of the first things I made that got popular was [find untagged Tumblr posts], which was built as a static website because that's all I knew how to build at the time.

I want to build more tools this way.

### Async JavaScript calls require careful handling

The JSZip library I'm using has a lot of async functions, and this is my first time using async JavaScript.
I got caught out several times, because I forgot to wait for async calls to finish properly.

For example, I'm using `canvas.toBlob` to render the image, which is async.
I wasn't waiting for that call to finish, and then the zip would be repackaged before the cover image was ready to add -- so I got an EPUB with a missing image.
Oops.

I'll always prefer the simplicity of synchronous code, but I'm sure I'll get better at async JavaScript with practice.

---

## Final thoughts

I know my friend will find this helpful, and that feels great.

Writing software that's designed for one person is my favourite software to write.
It's not hyper-scale, it won't launch the next big startup, and it's not breaking new technical ground -- but it is useful.
I can see how I'm making that person's life better, and isn't that what computers are meant to do?
If other people like it, that's a nice bonus, but it's not the point.

Normally the one person I'm writing software for is me, so it's extra nice when I can do it for somebody else.

If you want to try this yourself, go to [alexwlchan.net/my-tools/add-cover-to-ao3-epubs/](https://alexwlchan.net/my-tools/add-cover-to-ao3-epubs/).

If you want to read the code, it's all [on GitHub].

[on GitHub]: https://github.com/alexwlchan/add-cover-to-ao3-files
