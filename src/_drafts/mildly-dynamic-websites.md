---
layout: post
title: mildly-dynamic-websites
summary:
tags:
index:
  feature: true
---
Last year I wrote about [using static websites for tiny archives][static_sites].
Modern web tech is powerful, portable, and likely to remain readable for a long time.
I've been converting more and more of my local data to be stored in static websites, and I really like this approach.

[static_sites]: /2024/static-websites/

I got a lot of positive feedback on the post, but the most common reply was "can you give an example".
People wanted to see examples of the HTML and JavaScript I was using.
I deliberately omitted these examples from the original post, for a couple of reasons.

I wanted to focus on the concept, not the detail.
I was trying to persuade people that static websites are a good idea for this use cases, and I didn't want to get distracted by implementation details or code snippets.

There are lots of ways to build websites; I think that's the beauty of the web.
My own static site collection has a lot of variety -- no two sites are the same.
I want people to have their own ideas and build their own websites; not just copy what I'm doing.

And even a simple site can be very powerful -- you don't need much code to make something useful.
I don't have any shared code between my different archives because I start from scratch each time.
I open an empty text file, I start writing HTML, and I'm off.

With all that said, there is a common pattern emerging in my larger sites: metadata stored in JSON, rendered as HTML using JavaScript and template literals.
That's what I'm going to explain today.

This requires more technical skill than writing plain HTML, which is another reason I didn't describe it in the original post -- there are much simpler ways to get started, and I don't want anyone to be put off.
Websites should be for everyone!

I’m going to describe the basic approach, go through some more advanced features, and then I'll provide

https://www.nytimes.com/2018/09/29/opinion/sunday/in-praise-of-mediocrity.html
https://estherschindler.medium.com/the-old-family-photos-project-lessons-in-creating-family-photos-that-people-want-to-keep-ea3909129943
https://leancrew.com/all-this/2011/12/more-shell-less-egg/


## A medium viable website

This is a minimum viable

---


One website is a “digital scrapbook” which is literally cobbled together bits of HTML I’ve grabbed from the web. To my mind, this variety is the value of the web! I want to encourage that spirit, and I didn’t want to just give people a template to follow.

That said, a common pattern has emerged in some of my larger sites: metadata stored in JSON, then rendered on the page with template literals. This allows me to separate metadata and presentation

* Common bit of feedback: how do you build static websites?
        * Deliberately left out of original post
        * Partly because all different
                * I have a "digital scrapbook" which is literally cobbled together bits of hand-written HTML
                * Truest form of the web!
                * And want to encourage that spirit
        * Partly because all scrappy
* Do have a common pattern
        * Metadata stored as a JavaScript value, then render it on page with template literals
        * Can write small apps this way, here's a minimal example:

Here's an MVP:

```
<script>
const bookmarks = [
   { url: 'https://www.example.com', title: 'Example' },
   { url: 'https://alexwlchan.net', title: 'alexwlchan’s website' },
]

const Bookmark = (bookmark) =>
        `
        <li>
                <a href="${bookmark.url}">${bookmark.title}</a>
        </li>
        `;

window.addEventListener("DOMContentLoaded", () => {
        document.querySelector('#listOfBookmarks').innerHTML =
                bookmarks.map(Bookmark).join("");
});
</script>

<h1>Bookmarks</h1>

<ul id="listOfBookmarks"></ul>
```

why?
* inspired by react components in wellcomecollection.org, but not dynamic
* page is rendered once, don't need to deal with updates
* DOMContentLoaded when we have all scripts loaded and parsed, don't need to wait for subresources (e.g. images/stylesheets) to load
* no web components because I don't know what they are
* this technique would not be appropriate with user-generated content because you're injecting raw values into page, but I'm writing my own metadata so I trust it

Now customise with vanilla HTML, but that's it

More features you could add:
* sorting
* filtering
* pagination
put all of those inside the `window.addEventListener` block to cut down the list of entries to the specific slice you want to show rn

Noscript and errors

Bonus features:
* tests using QUnit
* manipulate JS using Python scripts, put metadata in separate file
* Playwright

Will be posting an example of a site using this pattern soon