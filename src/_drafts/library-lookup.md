---
layout: post
title: Finding books in nearby library branches
summary:
tags: books
---

<style>
  img {
    border: 3px solid #f0f0f0;
    border-radius: 8px;
  }
</style>

I'm trying to make better use of my local public library.
I want to read more books, and borrowing from the library keeps the habit sustainable.
It saves a fair bit of money, and I don't have to decide what to do with books when I'm done.

Recently, I built a tool to help me find books to borrow, and it's working pretty well.

It starts with my library's online catalogue.
When I find a book I might be interested in reading, I tap the bookmark icon in the upper right-hand corner:

<img src="/images/2022/library_online_catalogue.png" style="width: 593px;">

This saves the book to a list, which I can view on my account page.
But the website makes it hard to work out what I can actually borrow.
The example above says "92 copies", which means 92 physical books floating around the library network -- but they could be on loan, on hold for another reader, or in a branch halfway across the county.

If I tap "View availability", I get a long list of every copy in the network, its location and status:

<img src="/images/2022/library_availability_1x.png" srcset="/images/2022/library_availability_1x.png 1x, /images/2022/library_availability_2x.png 2x" style="width: 593px;">

Given there are dozens of books I'm interested in, scrolling lists like this gets tedious.
There must be a better way!

I've written a Python script that scrapes the library website, fetches all this information, then presents it in a nicer way.
The library website uses a platform called Spydus, and I found [some existing code] for logging into Spydus sites by pretending to be a browser.
Then I use [BeautifulSoup] to parse the data from the library HTML, and [Jinja] to render it in a different way.

This is what the cleaned-up page looks like:

<img src="/images/2022/library_lookup_1x.png" srcset="/images/2022/library_lookup_1x.png 1x, /images/2022/library_lookup_2x.png 2x, /images/2022/library_lookup_3x.png 3x" style="width: 604px;">

It shows the list of books I'm interested in, and highlights the copies which are actually available -- and specifically, copies that are available in branches within walking distance of my home.
I could walk straight in and borrow any of these books.

Over time, I books to gradually move around as they're borrowed by other readers -- so even if a book isn't in a local branch today, it might be sometime in the future.
There is a way for me to order books across branches, but right now I have plenty to choose from.

This filtered list is particularly useful when I'm in a hurry.
There's a library branch near the train station, so I can pop in and pick up a few books on the way to the office -- but I can't take too long, or I'll be late for work.
Having a list of what's available means I can be in and out quickly.

I also created a pick list of branches.
For example, if I'm visiting Ware to get my pictures framed, I can find out if there's anything I want to borrow at the library branch just down the road:

<img src="/images/2022/library_branch_picker_1x.png" srcset="/images/2022/library_branch_picker_1x.png 1x, /images/2022/library_branch_picker_2x.png 2x, /images/2022/library_branch_picker_3x.png 3x" style="width: 616px;">

This is some JavaScript that listens to the [onchange event] on the checkboxes; it re-sorts the list whenever I check or uncheck a branch.

I've already used this for several rounds of borrowing, and it's working great.
Having a steady supply of new and interesting books is encouraging me to read more, and I feel less guilt about abandoning a book I'm not enjoying -- I'm not losing anything.
(I usually read one book at a time, so a bad book can really stop me in my tracks.)

I'm not going to share the code, because it's scrappy and hard-codes the names of my local branches -- and let's be real, nobody else is actually going to use it.
The point of this post isn't to share this exact project, it's to showcase the general approach.

I love making this sort of single-user software, to solve a problem for me and nobody else.
I build a lot of tools like this: creating a presentation of a data set that's specifically designed for me.

You may not have this precise problem -- but I bet there's another annoyance you could fix with software written just for you.
And while you think about that, I have a stack of library books to read.

[some existing code]: https://github.com/mjagdis/spydus
[BeautifulSoup]: https://www.crummy.com/software/BeautifulSoup/
[Jinja]: https://jinja.palletsprojects.com/en/3.1.x/
[onchange event]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/change_event
[mechanize]: https://github.com/python-mechanize/mechanize
