---
layout: post
date: 2025-09-14 21:44:01 +0000
title: Linking to text fragments with a bookmarklet
summary: I've written a bookmarklet that helps me link to specific text on a web page.
tags:
  - javascript
  - bookmarklets
---
One of my favourite features added to web browsers in the last few years is [text fragments].

Text fragments allow you to link directly to specific text on a web page, and some browsers will highlight the linked text -- for example, by scrolling to it, or adding a coloured highlight.
This is useful if I'm linking to a long page that doesn't have linkable headings -- I want it to be easy for readers to find the part of the page I was looking for.

Here's an example of a URL with a text fragment:

<a href="https://example.com/#:~:text=illustrative%20examples"><code>https://example.com/<strong>#:~:text=illustrative%20examples</strong></code></a>

But I don't find the syntax especially intuitive -- I can never remember exactly what mix of colons and tildes to add to a URL.

To help me out, I've written a small bookmarklet to generate these URLs:

<style type="x-text/scss">
  @use "components/bookmarklets";
</style>

<a class="bookmarklet" href="javascript:(function()%7Bconst%20selectedText%20%3D%20window.getSelection().toString().trim()%3B%0A%0Aif%20(!selectedText)%20%7B%0A%20%20alert(%22You%20need%20to%20select%20some%20text!%22)%3B%0A%20%20return%3B%0A%7D%0A%0Aconst%20url%20%3D%20new%20URL(window.location)%3B%0Aurl.hash%20%3D%20%60%3A~%3Atext%3D%24%7BencodeURIComponent(selectedText)%7D%60%3B%0A%0Aalert(url.toString())%3B%7D)()%3B">Create link to selected text</a>

To install the bookmarklet, drag it to my bookmarks bar.

When I'm looking at a page and want to create a text fragment link, I select the text and click the bookmarklet.
It works out the correct URL and shows it in a popup, ready to copy and paste.
You can try it now -- select some text on this page, then click the button to see the text fragment URL.

It's a small tool, but it's made my link sharing much easier.

[text fragments]: https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment/Text_fragments

> **Update, 16 September 2025:** [Smoljaguar](https://spacey.space/@Smoljaguar/115207596961573171) on Mastodon pointed out that Firefox, Chrome, and Safari all have menu items for "Copy Link with Highlight" which does something very similar.
> The reason I don't use these is because I didn't know they exist!
>
> I use Safari as my main browser, and this item is only available in the right-click menu.
> One reason I like bookmarklets is that they become items in the Bookmarks menu, and then it's easy for me to assign keyboard shortcuts.

## Bookmarklet source code

This is the JavaScript that gets triggered when you run the bookmarklet:

```javascript
const selectedText = window.getSelection().toString().trim();

if (!selectedText) {
  alert("You need to select some text!");
  return;
}

const url = new URL(window.location);
url.hash = `:~:text=${encodeURIComponent(selectedText)}`;

alert(url.toString());
```

