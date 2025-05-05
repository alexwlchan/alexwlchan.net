---
layout: post
title: Learning how to make websites by reading two thousand web pages
summary:
tags:
  - bookmarking
  - web development
---
I built a web archive of about 2,500 web pages – I wanted to save my own copy of everything I've bookmarked over the past 15 years. I created a lot of these archive copies by hand, editing the HTML of the web page I'd saved to point images at local copies, strip out ads and tracking, remove lazy loading that's not necessary in a local archive.

This meant I read a lot of web pages written by other people or by tools I'm unfamiliar with. I learnt a lot about how the web works, and this is what sustained me through this multi-month project – I was constantly learning about new aspects of web tech that I’d never encountered before, and seeing how they were used in practice.

There’s a lot of bloat on the web, of course, but that’s not news, and you don’t need to read thousands of web pages to know it. Instead, let’s talk about all the cool and useful stuff I learned!

## How people use semantic HTML

I'm loosely aware of semantic HTML exists -- using HTML tags that describe the meaning of your content, not their visual appearance. For example, using a heading tag `<h1>` rather than a bold tag `<b>`. I know the theory and I've read a list of available elements once, but I found it really helpful to see what tags are popular, and how people are actually using them in practice:

* `<section>` is a standalone section of a document, and a tag I'd completely forgotten. I've already started using it in several places in the Flickr Commons Explorer, in place of a more generic `<div>`.
* `<aside>` is a tag I was aware of, but I didn't know when I'd use it. I saw lots of examples where it was used to embed content in the middle of the article, like ads, newsletter sign-up forms, pull quotes, links to related or popular articles.

	I also saw `<ins>` used for ads on a few sites, which is novel but doesn't feel semantically correct.

* `<mark>` is a tag for marking or highlighting text, which is used for highlights on Medium articles and pull quotes on other sites. I haven't used it myself yet, but I can imagine using it in code snippets in future.

	{Example from MDN; replace with my own}

	```html
	<p>Search results for "salamander":</p>

	<hr />

	<p>
	  Several species of <mark>salamander</mark> inhabit the temperate rainforest of
	  the Pacific Northwest.
	</p>

	<p>
	  Most <mark>salamander</mark>s are nocturnal, and hunt for insects, worms, and
	  other small creatures.
	</p>
	```

* `<hgroup>` is a tag for grouping a heading and related content, like a title and a subtitle, for example:
	```html
	<hgroup>
		<h1>All about web bookmarking</h1>
		<p>Posted 16 March 2025</p>
	</hgroup>
	```
	This is another tag I didn’t know about, and I’ve started using it on this site.

* I replaced a lot of embedded videos with the `<video>` element pointing to a locally downloaded copy of the video, which is the first time I've used this tag in earnest. I still remember reading Kroc Camen’s article [Video is for Everybody](https://camendesign.com/code/video_for_everybody), and it’s nice to finally put that knowledge to use.

  One mistake I kept making was forgetting to close the tag:

  ```html
	<!-- this is wrong -->
	<video controls src="videos/Big_Buck_Bunny.mp4"/>
	```

	This feels like `<img>` which is a self-closing tag, but that's not how `<video>` works. Because it can take child elements, you have to explicitly close it with `</video>`

## The `<base>` tag in HTML

## CSS supports import statement

CSS has `@import` statements, so one stylesheet can load another stylesheet:
```css
@import "fonts.css";
```
I've used the import statement in Sass, and I didn't know this was a feature of vanilla CSS now – but it was in fairly common use.

My CSS is small enough that I package it into a single file for websites served over HTTP (the CSS for this website is only 13KB) – but I've started to use this for static websites I load from my local filesystem.

I don't think CSS supports this yet, but I think imports conditional on a selector might be useful – you can already do conditional imports based on a media query ("only load these styles on a narrow screen") and I think conditional imports based on the presence of a selector would be useful too ("only load these styles if a particular class is use"). I have some longer CSS rules that I don't need on every page, and might be nice to load conditionally (like my styles for good embedded toots).

## The many features of CSS

I'm a CSS novice at best – I can lay out a basic web page, but nothing fancy. I wrote down a lot of notes on CSS features that caught my eye as I was reading.

* A lot of sites have a "reset" or "normalize" stylesheet, which removes all the browser styles and gives you a blank slate. I’d seen these names but never understood their purpose before; it’s not my preference but now I’ve seen them in action.


* `cursor: zoom-in` is a common rule for images which link to a larger size, for example in photo galleries. I knew about `cursor` but I'd never thought to use it that way.
* I saw the `data-href` attribute used on `<style>` tags on a number of sites, for example `<style data-href="https://example.com/style.css">` – a way of indicating where the CSS defined in that `<style>` tag comes from. I thought that was a neat idea.
* I have a better understanding of `@font-face`, which is used all over the web but I've mostly ignored – I prefer web-safe fonts because they look "good enough" to my eyes and are much simpler to implement.
* Entertainment Weekly (?) uses `box-shadow: inset` to get a fancy-looking underline in their links.
	```html
	<style>
	  div {
	    box-shadow: inset 0 -6px 0 #b0e3fb;
	  }
	</style>

	<div>hello world</div>
	```

{cursor: zoom-in} – I should use this

## Developers like to leave messages in the JavaScript console

I always smiled at sites that left a message for people looking in the developer console – often a wave to fellow web developers, or a link to a jobs page.

A couple of sites also used this as a place to leave security warnings for non-developers – apparently there are scammers who send people snippets of JavaScript to run in their web console, which can potentially do a lot of damage. Sites would print scary looking messages "don't trust people who tell you to run code here", but it doesn't seem especially widespread.

## What does GPT mean on a web page?

Thanks to the rise of ChatGPT, I'm used to "GPT" being associated with generative AI – so I was surprised to see it cropping up on web pages that predate the widespread use of LLMs. For example:

```html
<div id="div-gpt-ad-1481124643331-2"
```

It turns out GPT also stands for "Google Publisher Tag", an ad tagging library used by Google Ad Manager.

(What does "ad tagging" mean? / https://developers.google.com/publisher-tag/guides/get-started)