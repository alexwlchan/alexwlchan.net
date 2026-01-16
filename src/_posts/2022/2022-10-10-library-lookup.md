---
layout: post
date: 2022-10-10 19:47:42 +00:00
title: Finding books in nearby library branches
summary: Some web scraping and Python helps me find books that I can borrow immediately.
tags:
  - books
  - libraries
colors:
  index_light: "#527345"
  index_dark:  "#97b18a"
---

<!-- Cover image from https://wellcomecollection.org/works/u7xetmy2/images?id=mbrj8865, Public Domain -->

I'm trying to make better use of my local public library.
I want to read more books, and borrowing from the library keeps the habit sustainable.
It also saves a fair bit of money, and I don't have to decide what to do with books when I'm done.

Recently, I built a tool to help me find books to borrow, and it's working pretty well.

It starts with my library's online catalogue.
When I find a book I might be interested in reading, I tap the bookmark icon in the upper right-hand corner of the search result:

{%
  picture
  filename="library_online_catalogue.png"
  alt="A search result in my library’s online catalogue. The result includes the title, the author, and the publication year. In the top right-hand corner is a small green bookmark icon."
  width="494"
  class="screenshot"
%}

This saves the book to a list on the library site, which I can view on my account page.
But the website makes it hard to work out what I can actually borrow.
The example above says "92 copies", which means 92 physical books floating around the library network -- but they could be on loan, on hold for another reader, or in a branch halfway across the county.

If I tap "View availability", I get a long list of every copy in the network, its location and status:

{%
  picture
  filename="library_availability.png"
  alt="A modal dialog labelled ‘Availability’. It’s a long list. Each entry in the list has a location (e.g. Abbots Langley Library), a collection (e.g. Hot picks), a call number (e.g. General fiction) and a status/description (e.g. Available). Only two results are visible in the current scroll position."
  width="593"
  class="screenshot"
%}

Given there are dozens of books I'm interested in, scrolling lists like this gets tedious.
There must be a better way!

I've written a Python script that scrapes the library website, fetches all this information, then presents it in a nicer way.
The library website uses a platform called Spydus, and I found [some existing code] for logging into Spydus sites by pretending to be a browser.
Then I use [BeautifulSoup] to parse the data from the library HTML, and [Jinja] to render it in a nicer way.

This is what my new page looks like:

{%
  picture
  filename="library_lookup.png"
  alt="A list of books. The first two books have large titles, a summary, and a list of branches where copies are available for immediate borrowing. There are two more books which are shown in smaller text and with greyed-out covers -- these aren't available nearby."
  width="623"
  class="screenshot"
%}

It shows the list of books I'm interested in, and highlights the copies which are actually available -- and specifically, copies that are available in branches within walking distance of my home.
I could walk in and borrow any of these books immediately.

Over time, I expect books to gradually move around as they're borrowed by other readers -- so even if a book isn't in a nearby branch today, it might be sometime in the future.
I can order books from a different branch to pick up locally, but right now I have plenty to choose from.

This filtered list is particularly useful when I'm in a hurry.
There's a library branch near the train station, so I can pop in and pick up a few books on the way to the office -- but I can't take too long, or I'll be late for work.
Having a list of what's readily available means I can be in and out quickly.

The tool includes a pick list of branches.
For example, if I'm visiting Ware to get my pictures framed, I can find out if there's anything I want to borrow at the library branch just down the road:

{%
  picture
  filename="library_branch_picker.png"
  alt="A list of library branch names with tickboxes. A single branch is ticked ‘Ware Library’, and below is shown a book with a single copy in Ware Library."
  width="663"
  class="screenshot"
%}

This is some JavaScript that listens to the [onchange event] on the checkboxes; it re-sorts the list whenever I check or uncheck a branch.

I've already used this for several rounds of borrowing, and it's working great.
Having a steady supply of new and interesting books is encouraging me to read more, and I feel less guilt about abandoning a book I'm not enjoying -- I'm not losing anything.
(I can only read one book at a time, so a bad book really stops me in my tracks.)

Although I don't expect anybody else to use this tool directly, I've [put the code on GitHub][github].
There may be ideas or techniques here that apply to a different problem you have -- and while you read through that, I have a stack of library books to finish.

[some existing code]: https://github.com/mjagdis/spydus
[BeautifulSoup]: https://www.crummy.com/software/BeautifulSoup/
[Jinja]: https://jinja.palletsprojects.com/en/3.1.x/
[onchange event]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/change_event
[mechanize]: https://github.com/python-mechanize/mechanize
[github]: https://github.com/alexwlchan/library-lookup
