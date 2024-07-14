---
layout: post
title: How I lay out a basic web page
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
When I design web pages, I always start with a single-column layout:

{%
  picture
  filename="one_column.png"
  width="400"
%}

It's a sandwich: I have a header/footer at the top/bottom of the page, and all the main content in the middle.
I add a coloured background to the header and footer to make them stand out visually, and I centre everything on the page.
I also cap the width to maintain readability.

To get this layout in HTML, I have some CSS snippets that I copy from project to project.
I recently pulled them out into a standalone template, and I wrote some notes to make sure I really understood how this all works.
In this post, I'll explain what I've learnt.

## Start with semantic HTML

Here's a basic HTML template for this layout: [a `<header>`][header], [a `<main>`][main] and [a `<footer>`][footer].

```
<html>

<body>
  <header>
    <h1>Welcome to my web page</h1>
  </header>

  <main>
    <p>This is some text on my web page.</p>
  </main>

  <footer>
    <p>This is some information about the web page.</p>
  </footer>
</body>

</html>
```

I always try to use [semantic HTML elements][semantic].
The more I lean on these standard components of the web, the more nice behaviour I get "for free".

Here I mean things like default browser styles or screen reader descriptions.
Other people have put a lot of time and thought into how these tools should behave when they encounter semantic HTML -- how a heading should appear, how a list should be described, how you navigate a series of paragraphs.
By using semantic HTML and opting-in to these behaviours, my website will be familiar to readers -- it will look and feel like other websites.

I can still add personality and flare, but I get all the key functionality of the web.

This [unstyled HTML](/files/2024/step1.html) is a pretty boring page, but it's a start:

{%
  picture
  filename="Screenshot1.png"
  width="500"
  class="screenshot"
%}

Let's jazz it up.

[header]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/header
[main]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/main
[footer]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/footer
[semantic]: https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML#good_semantics

## Adding a dash of colour

I like to add a coloured background to my header and footer, to distinguish them from the rest of the page.
It's a good place to add a strong colour and give the page an identity, and then I can use more subtle colours in the main content.

Here's the CSS:

```
:root {
  --header-background-color: LightGreen;
  --footer-background-color: PowderBlue;
}

header { background: var(--header-background-color); }
footer { background: var(--footer-background-color); }
```

I'm using [CSS variables] to define my palette, and then setting the [`background` property][background] on the header and footer.

I've only started using CSS variables quite recently, but I like them so far.
Their behaviour feels very intuitive to me -- for example, the way I can define a default variable on `:root` but then override it on the styles of individual elements.
(That's how I do the per-card colours on my [articles page](/articles), for example.)
They've also allowed me to remove CSS preprocessors from some of my projects, and just write vanilla CSS.

Here's what the [coloured header and footer](/files/2024/step2.html) look like:

{%
  picture
  filename="step2.png"
  width="500"
  class="screenshot"
%}

[CSS variables]: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
[background]: https://developer.mozilla.org/en-US/docs/Web/CSS/background
[Sass]: https://sass-lang.com/

## Removing the default margins

I don't like the whitespace around the edges of the coloured backgrounds -- I want them to extend all the way to the edge of the page, so let's fix that next.
Using the web inspector, I can see that the whitespace comes from a margin on the `<body>` element, which is added by my browser's default stylesheet.
I can override it:

```
body {
  margin:  0;
  padding: 0;
}
```

Now the coloured sections touch the [left and right edges](/files/2024/step3.html), like I want:

{%
  picture
  filename="step3.png"
  width="500"
  class="screenshot"
%}

## Putting the text in the middle

As well as touching the sides of the window, I want the footer to touch the bottom -- I don't like having all that empty space below the footer if the content is too short.
I want to push it all the way down, and have the main content fill the window.

There are [several ways to get this effect](https://stackoverflow.com/q/643879/1558022); personally I like using CSS Grid because it's a tool I'm quite familiar with:

```
body {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr auto;
}
```

The first line makes the `<body>` at least as tall as the window.
The second line tells the `<body>` to display as a grid.
The third line sets the height of the rows: the first and third row should be as short as they can be, and the middle row should take all the remaining space.

If the page is shorter than the window, the middle row (`<main>`) will expand to take all the vertical space not taken by the header and footer.
If the page is taller than the window, the middle row will be as tall as the main content, but no more.

This pushes the footer [to the bottom](/files/2024/step3.html), but also expands the coloured regions:

{%
  picture
  filename="step4.png"
  width="500"
  class="screenshot"
%}

Where did the extra space come from?
I had a look at the page in the web inspector, and found out that this space is the default margins around an `<h1>` and a `<p>` element -- but why are they only appearing now?
Why didn't we see them before?

After some googling, I learnt that this is caused by a CSS behaviour called [margin collapsing].
When you have two vertically adjacent components, their top and bottom margins will be combined into a single margin which is big enough to include both margins.
For example, if one element has `10px` of margin and the other element has `20px` of margin, then margin collapsing will put a `20px` margin between them -- rather than `30px`.
The two margins can overlap.

In the previous example, the margins on the header `<h1>` and the footer `<p>` were being collapsed with elements outside the header/footer -- the margins were still there, but they were outside the coloured regions.
But when you're inside a container with `display: grid`, margins don't collapse, so those margins are now *inside* the coloured regions.

[margin collapsing]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model/Mastering_margin_collapsing

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