---
layout: post
title: Beware the incomplete PDF redaction
summary: If you're not careful when redacting PDFs, it's possible to share more information than you intended.
tags: images python
---

A while back I was reviewing some legal documents.
I had to check that everything was correct, and that they were ready to be made public.

To avoid leaking personal information, black boxes had been added to redact certain sections:

<img src="/images/2021/redacted_contract.png" style="width: 287px;">

I received the documents as a set of PDFs, and as I was reading them, something felt off about the black boxes.
It's hard to explain, but I got a spidey sense that the boxes were somehow separate from the rest of the document.
As I dragged to select text, the boxes weren't being selected.

If the boxes were separate – could they be removed?

If they could be removed – could I get the personal information that was meant to be redacted?

I found a blog post with [code for extracting images from a PDF in Python][external_post], which I adapted into [my own script][own_script].
I ran it over the PDFs, and to my horror, a bunch of images that were meant to be redacted fell out.
Oops.

PDF is a complicated format, and getting redaction right is moderately tricky.

PDF documents can be made up of multiple layers, and when you view the document those layers get flattened into a single page.
In this case, the black rectangle was on a separate layer to the unredacted document:

<img src="/images/2021/pdf_with_layers.png" style="width: 369px;">

I was able to extract the original layers, and the redacted information.
Although I used a Python script, plenty of other programs can also extract individual PDF layers – so this wouldn't have been safe to make public.

If you want to redact information in a PDF safely, you need to remove it from the original layer.
This means that even if somebody picks apart the original layers, they can't find the information:

<img src="/images/2021/pdf_single_layer.png" style="width: 369px;">

The problem is, a PDF with and without layers look near identical.
There was a difference which tipped me off to the issue, but it's so subtle I don't know how to explain it.

I'd love to provide a foolproof approach to redacting PDFs; a set of how-to steps that guarantee security.
Unfortunately it's not something I do very often, and I'm not sure I could do it correctly – using the layers is one way to get around redaction, but maybe there's another I'm not aware of.



[external_post]: https://www.thepythoncode.com/code/extract-pdf-images-in-python
[own_script]: /files/2021/extract_images_from_pdf.py
