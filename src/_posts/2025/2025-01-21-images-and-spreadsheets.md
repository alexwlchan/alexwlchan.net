---
layout: post
date: 2025-01-21 09:33:48 +00:00
title: Looking at images in a spreadsheet
summary: The `IMAGE` and `HYPERLINK` functions allow me to use a spreadsheet as a lightweight, collaborative space for dealing with images.
tags:
  - spreadsheets
  - images
  - photo management
---
I’ve had a couple of projects recently where I needed to work with a list that involved images.
For example, choosing a series of photos to print, or making an inventory of Lego parts.
I could write a simple text list, but it's really helpful to be able to see the images as part of the list, especially when I'm working with other people.

The best tool I've found is Google Sheets -- not something I usually associate with pictures!

{%
  picture
  filename="lego_spreadsheet.png"
  width="582"
  alt="Screenshot of a spreadsheet showing a list of four Lego bricks, plus a count of how many I have/need. There are images showing an illustration of the four bricks."
  class="screenshot"
%}

I'm using Google Sheets, and I use [the IMAGE function][image_sheets], which inserts an image into a cell.
For example:

```
=IMAGE("https://www.google.com/images/srpr/logo3w.png")
```

There's a similar function in [Microsoft Excel][image_excel], but not in Apple Numbers.

This function can reference values in other cells, so I'll often prepare my spreadsheet in another tool -- say, a Python script -- and include an image URL in one of the columns.
When I import the spreadsheet into Google Sheets, I use `IMAGE()` to reference that column, and then I see inline images.
After that, I tend to hide the column with the image URL, and resize the rows/columns containing images to make them bigger and easier to look at.

I often pair this with the [HYPERLINK function][hyperlink], which can add a clickable link to a cell.
This is useful to link to the source of the image, or to more detail I can't fit in the spredsheet.

I don't know how far this approach can scale -- I've never tried more than a thousand or so images in a single spreadsheet -- but it's pretty cool that it works at all!

Using a spreadsheet gives me a simple, lightweight interface that most people are already familiar with.
It doesn’t take much work on my part, and I get useful features like sorting and filtering for “free”.
Previously I'd only thought of spreadsheets as a tool for textual data, and being able to include images has made them even more powerful.

[image_sheets]: https://support.google.com/docs/answer/3093333?hl=en-GB
[image_excel]: https://support.microsoft.com/en-gb/office/image-function-7e112975-5e52-4f2a-b9da-1d913d51f5d5
[hyperlink]: https://support.google.com/docs/answer/3093313?hl=en-GB
