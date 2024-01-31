---
layout: post
title: Making a PDF that’s larger than Germany
summary: We’re gonna need a bigger printer.
tags:
  - drawing-things
  - code-crimes
---

I was browsing social media this morning, and I saw a claim I've seen go past a few times now -- that there's a maximum size for a PDF document:

{% tweet https://twitter.com/TerribleMaps/status/1674813732260655106 %}

This tweet is pretty emblematic of posts about this claim: it's stated as pure fact, with no supporting evidence or explanation.
We're meant to just accept that a single PDF can only cover about half the area of Germany, and we're not given any reason why 381 kilometres is the magic limit.

I started wondering: has anybody made a PDF this big?
How hard would it be?
Can you make a PDF that's even bigger?

A few years ago I did some [silly noodling into PostScript][ps], the precursor to PDF, and it was a lot of fun.
I've never actually dived into the internals of PDF, and this seems like a good opportunity.

Let's dig in.

[ps]: https://codegolf.stackexchange.com/a/48938/13285

## Where does the claim come from?

These posts are often accompanied by a "well, actually" where people explain this is a limitation of a particular PDF reader app, not a limitation of PDF itself.
As [the Wikipedia article for PDF][wikipedia] explains:

> Page dimensions are not limited by the format itself. However, Adobe Acrobat imposes a limit of 15 million by 15 million inches, or 225 trillion in<sup>2</sup> (145,161 km<sup>2</sup>).<a href="https://en.wikipedia.org/wiki/PDF#cite_note-pdf-ref-1.7-2"><sup>[2]</sup></a>

and if you follow the reference link, you find the [specification for PDF 1.7][spec], where an appendix item explains in more detail (emphasis mine):

> In PDF versions earlier than PDF 1.6, the size of the default user space unit is fixed at 1/72 inch. In Acrobat viewers earlier than version 4.0, the minimum allowed page size is 72 by 72 units in default user space (1 by 1 inch); the maximum is 3240 by 3240 units (45 by 45 inches). In Acrobat versions 5.0 and later, the minimum allowed page size is 3 by 3 units (approximately 0.04 by 0.04 inch); the maximum is 14,400 by 14,400 units (200 by 200 inches).
>
> Beginning with PDF 1.6, the size of the default user space unit may be set with the UserUnit entry of the page dictionary. **Acrobat 7.0 supports a maximum UserUnit value of 75,000, which gives a maximum page dimension of 15,000,000 inches (14,400 * 75,000 * 1 ⁄ 72).** The minimum UserUnit value is 1.0 (the default).

15 million inches is exactly 381 kilometres, matching the number in the original tweet.
And although it's PDF 1.6, it's "version 7" of Adobe Acrobat.

I've never come across UserUnit before, but reading this I have to wonder: even if Acrobat only goes up to 75,000, can we go bigger?

<!-- I don't know who first decided this meant "maximum size of a PDF" and lost the context about Acrobat and UserUnit, but the claim was going around [at least as early as 2007][tw_2007]. -->

[wikipedia]: https://en.wikipedia.org/wiki/PDF#:~:text=Page%20dimensions%20are%20not%20limited%20by%20the%20format%20itself
[spec]: https://web.archive.org/web/20081001170454/https://www.adobe.com/devnet/acrobat/pdfs/pdf_reference_1-7.pdf
[tw_2007]: https://twitter.com/hassmanm/status/303086542

## The inner structure of PDFs

I've never dived into the internals of a PDF document -- I've occasionally glimpsed it, but I've never really understood how they work.
If you already know how PDF works, you can skip this section.

I'm sure I could modify the UserUnit value in an existing PDF with a library or tool, but I thought this was a good opportunity to actually learn how PDFs work.
I found [a good article][callas] which explains the internal structure of a PDF, and combined with asking ChatGPT a few questions, I was able to get enough to write some simple files by hand.

I know that PDFs support a huge number of features, so this is probably a gross oversimplification, but this is the mental picture I created:

[callas]: https://help.callassoftware.com/a/798383-how-to-create-a-simple-pdf-file

<style>
  :root { color-scheme: dark light; }

  @media screen and (prefers-color-scheme: light) {
    rect.pdf_component {
      fill: white;
    }

    rect.object_wrapper {
      fill: rgba(228, 228, 228, 0.85);
    }
  }

  @media screen and (prefers-color-scheme: dark) {
    rect.pdf_component {
      fill: black;
    }

    rect.object_wrapper {
      fill: rgba(61, 61, 61, 0.75);
    }
  }
</style>

{%
  inline_svg
  filename="pdf_layout.svg"
  class="dark_aware"
  alt="tbc"
  style="width: 300px;"
%}

The start and end of a PDF file are always the same: a version number (`%PDF-1.6`) and an end-of-file marker (`%%EOF`).

After the version number comes a long list of objects.
There are lots of types of objects, for all the various things you can find in a PDF, including the pages, the text, and the graphics.

After that is the `xref` or cross-reference table, which is a lookup table for the objects.
It points to all the objects in the file: it tells you that object 1 is 10 bytes after the start, object 2 is after 20 bytes, object 3 is after 30 bytes, and so on.
By looking at this table, a PDF reading app knows how many objects there are in the file, and where to find them.

The `trailer` contains some metadata about the document, including the UserUnit value that we'll return to later.

Finally, the `startxref` value is a pointer to the start of the `xref` table.
This is where a PDF reading starts: it works from the end of the file until it finds the `startxref` value, then it can go and read the `xref` table and learn about all the objects.

Here's a simple example of a PDF that I wrote by hand.
If you copy/paste this code into a file named `myexample.pdf`, it should open and show a simple PDF with a red square in a PDF reading app:

<pre class="highlight"><code><span class="c">%PDF-1.6

% The first object.  The start of every object is marked by:
%
%     &gt;object number> &gt;generation number> obj
%
% (The generation number is used for versioning, and is usually 0.)
%
% This is object 1, so it starts as `1 0 obj`.  The second object will
% start with `2 0 obj`, then `3 0 obj`, and so on.  The end of each object
% is marked by `endobj`.
%
% This is a "stream" object that draws a shape.  First I specify the
% length of the stream (54 bytes).  Then I select a colour as an
% RGB value (`1 0 0 RG` = red), then I set a line width (`5 w`) and
% finally I give it a series of coordinates for drawing the square:
%
%     (100, 100) ----> (200, 100)
%                          |
%     [s = start]          |
%         ^                |
%         |                |
%         |                v
%     (100, 200) <---- (200, 200)
%</span>
1 0 obj
<<
	/Length 54
>>
stream
1 0 0 RG
5 w
100 100 m
200 100 l
200 200 l
100 200 l
s
endstream
endobj

<span class="c">% The second object.
%
% This is a "Page" object that defines a single page.  It contains a
% single object: object 1, the red square.  This is the line `1 0 R`.
%
% The "R" means "Reference", and `1 0 R` is saying "look at object number 1
% with generation number 0" -- and object 1 is the red square.
%
% It also points to a "Pages" object that contains the information about
% all the pages in the PDF -- this is the reference `3 0 R`.</span>
2 0 obj
<<
	/Type /Page
	/Parent 3 0 R
	/MediaBox [0 0 300 300]
	/Contents 1 0 R
>>
endobj

<span class="c">% The third object.
%
% This is a "Pages" object that contains information about the different
% pages.  The `2 0 R` is reference to the "Page" object, defined above.</span>
3 0 obj
<<
	/Type /Pages
	/Kids [2 0 R ]
	/Count 1
>>
endobj

<span class="c">% The fourth object.
%
% This is a "Catalog" object that provides the main structure of the PDF.
% It points to a "Pages" object that contains information about the
% different pages -- this is the reference `3 0 R`.</span>
4 0 obj
<<
	/Type /Catalog
	/Pages 3 0 R
>>
endobj

<span class="c">% The xref table.  This is a lookup table for all the objects.
%
% I'm not entirely sure what the first entry is for, but it seems to be
% important.  The remaining entries correspond to the objects I created.</span>
xref
0 4
0000000000 65535 f
0000000851 00000 n
0000001396 00000 n
0000001655 00000 n
0000001934 00000 n

<span class="c">% The trailer.  This contains some metadata about the PDF.  Here there
% are two entries, which tell us that:
%
%   - There are 4 entries in the `xref` table.
%   - The root of the document is object 4 (the "Catalog" object)
%</span>
trailer
<<
	/Size 4
	/Root 4 0 R
>>

<span class="c">% The startxref marker tells us that we can find the xref table 2196 bytes
% after the start of the file.</span>
startxref
2196

<span class="c">% The end-of-file marker.
%%EOF</span></code></pre>

I played with this file for a while, just doing simple things like adding extra shapes, changing how the shapes appeared, and putting different shapes on different pages.
I tried for a while to get text working, but that was a bit beyond me.

It quickly became apparent why nobody writes PDFs by hand -- it got very fiddly to redo all the lookup tables!
But I'm glad I did it; manipulating all the PDF objects and their references really helped me feel like I understand the basic model of PDFs.
I opened some "real" PDFs created by other apps, and they have many more objects and types of object -- but I could at least follow some of what's going on.

So now I have this newfound ability to edit PDFs by hand, how can I create monstrously big ones?

## Changing the page size: /MediaBox and /UserUnit

Within a PDF, the size of each page is set on the individual "Page" objects -- this allows different pages to be different sizes.
We've already seen this once:

<style>
  .mediaBox {
    font-weight: bold;
  }
</style>

<pre><code>&gt;&gt;
	/Type /Page
	/Parent 3 0 R
	<span class="mediaBox">/MediaBox [0 0 300 300]</span>
	/Contents 1 0 R
>></code></pre>

Here, the `MediaBox` is setting the width and height of the page -- in this case, a square of 300 × 300 units.
The default unit size is 1/72 inch, so the page is 300 × 72 = 4.17 inches.
And indeed, if I open this PDF in Adobe Acrobat, that's what it reports:

{%
  picture
  filename="adobe-acrobat-pdf-4in.png"
  width="724"
%}

By changing the `MediaBox` value, we can make the PDF bigger.
For example, if we change it to `600 300`, Acrobat says the size of our PDF is `8.33 x 4.17 in`.
Nice!

We can increase it all the way to `14400 300`, the max allowed by Acrobat, and then it says the PDF is now `200.00 x 4.17in`.
(You [get a warning](/images/2024/acrobat-error.png) if you try to push past that limit.)

But 200 inches is far short of 381 kilometres -- and that's because we're using the default unit of 1/72 inch.
We can increase the unit size by adding a `/UserUnit` value.
For exaple, setting the value to 2 will double the page in both dimensions:

<pre><code>&gt;&gt;
	/Type /Page
	/Parent 3 0 R
	<span class="mediaBox">/MediaBox [0 0 14400 300]</span>
	<span class="mediaBox">/UserUnit 2</span>
	/Contents 1 0 R
>></code></pre>

And now Acrobat reports the size of our document as `400.00 x 8.33 in`.

If we crank it all the way up to the maximum of `UserUnit 75000`, Acrobat now reports the size of our document as `15,000,000,000.00 x 312,500.38 in` -- 381 km in width, where we started.
If you're curious, you can [download the PDF](/files/2024/biggest.pdf).

If we crank it any further, Acrobat just ignores it.
I turned it up to `UserUnit 100000`, and Acrobat still claimed the document was 15 billion inches wide.
(Unlike when we pushed through the `MediaBox` limit, this happens silently -- there's no warning or error to suggest the value is capped.)

This probably isn't an issue -- I don't think the `UserUnit` value is widely used in practice.
I found [one Stack Overflow answer][so] saying as such, and I couldn't find any examples of it online.
The builtin macOS Preview.app doesn't even support it -- it completely ignores the value, and treats all PDFs as if the unit size is 1/72 inch.

But unlike Acrobat, the Preview app doesn't have an upper limit on what we can put in `MediaBox`.
It's perfectly happy for me to write a width which is a 1 followed by twelve 0s:

{%
  picture
  filename="preview-megawide.png"
  width="366"
%}

If you're curious, that width is approximately the distance between the Earth and the Moon.
I'd have to get my ruler to check, but I'm pretty sure that's larger than Germany.

I could keep going.
And I did.
Eventually I ended up with a PDF that Preview claimed is larger than the entire universe -- approximately 37 trillion light years square.
If you'd like to play with that PDF, you can [get it here](/files/2024/universe.pdf).

Please don't try to print it.

[so]: https://stackoverflow.com/a/59927201/1558022
