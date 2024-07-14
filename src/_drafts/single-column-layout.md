---
layout: post
title: The CSS for my single-column layout web pages
summary: |
  A deep dive on the CSS I use in my standard HTML template -- a single column with a header, main content, and a footer.
tags:
colors:
  css_light: "#0b53ad"
  css_dark:  "#d9d9d6"
tags:
  - css
  - web-development
---
When I design web pages, I start with a pretty standard single-column layout:

{%
  picture
  filename="one_column.png"
  width="400"
%}

This layout is a sandwich: a header/footer at the top/bottom of the page, and all the main content in the middle.
I usually add a coloured background to the header and footer to make them stand out visually.
Then everything is centred on the page, and I cap the width to maintain readability.
(It's the layout I'm using in this very post!)

---

good enough
i'm not an expert web developer

---

To get this layout in HTML, I have some CSS snippets that I copy from project to project.
Within each project, these template styles get mixed with project-specific CSS, and it's not always clear what's part of the template and what's part of a single project.
I wanted to pull it all out into a standalone template, and make sure I really understood what was going on.

In this post, I'm going to do a deep-dive on how I create this layout.
I'll include some comments and thoughts on how I approach HTML and CSS -- writing this out in detail has really helped me understand some fundamental concepts.

## Starting with an HTML skeleton

Here's a basic skeleton for the HTML of this page: [a `<header>`][header], [a `<main>`][main] and [a `<footer>`][footer].

```html
<html>

<body>
  <header>
    <h1>Welcome to my web page</h1>
  </header>

  <main>
    <p>This is the main content of the web page.</p>
  </main>

  <footer>
    This is the bottom of the web page.
  </footer>
</body>

</html>
```

There are [plenty of reasons][semantic] to use semantic HTML elements; what I like is that it gets me a lot of good behaviour "for free".

For example, browsers and assistive technologies know how to interpret these elements, and will provide a good experience for readers.
They know that `<h1>` is a heading, `<p>` is a paragraph, `<ul>` is a list, and so on.
They can present my pages in a useful and consistent way, and that makes them easier for my readers to navigate.

It might be possible to replicate or improve that experience with `<div>`s, the right styles, and `aria-*` attributes -- but it would require a lot of web expertise that I just don't have.
  
  listen to https://www.relay.fm/radar/282

---

Two examples:

*   Assistive technologies already know how to interpret this structure, and will provide a good experience for readers.

    They can describe the structure and navigate in an efficient way.



*   Browsers will apply some default styles to semantic elements, so they look good without any work from me.
    If I don't apply any custom CSS, they'll have a consistent appearance with other websites that also use those default styles.

---

    For example, this list is a `<ul>` and it pro

       I'm not applying any custom styles -- I'm relying on your browser to render something that looks good.

I recently read Patrick Weaver's [blog post with every HTML element], which illustrates just how many different HTML elements there are.

[header]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/header
[main]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/main
[footer]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/footer
[semantic]: https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML#good_semantics
[blog post with every HTML element]: https://www.patrickweaver.net/blog/a-blog-post-with-every-html-element/

---

The final template is [on GitHub](https://github.com/alexwlchan/web-page-template).

---

This layout is simple, but it works well for the sort of web pages I make.
Usually I'm displaying static content which can be read from top to bottom, and this layout is a good fit.



---

header at top of page; footer at bottom
usually some solid colour or texture to separate from main content of the page
want to be centred at a readable width -- don't make too wide

how to do this in CSS?

I have CSS snippets I've been copying from project to project
wanted to sit down and make it work properly

basic HTML skeleton
let's apply some CSS to make it look pretty

## approach to css

* should look good without
* no css frameworks
* write everything by hand

## pushign header all the way to the top

header at top of page by default
add coloured background
but has white border around page

## pushign footer allt he way to the bottom

add coloured background
want at bottom of screen, even if main text is a bit short
let's do flex!

## centering all the text

max-width, auto
why auto?

## final snippet

I have this snippet bound to !html
as well as default css, includes some basic `<script>` and `<link>` tags because I can never remember how to use them without an example