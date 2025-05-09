---
layout: post
title: What I learnt about web development by reading two thousand web pages
summary:
tags:
  - bookmarking
  - web development
colors:
  css_light: "#0000ff"
  css_dark:  "#00ddff"
---
Over the past year, I [built a web archive](/2025/creating-bookmark-archives/) of over two thousand web pages -- my own copy of everything I've bookmarked in the last fifteen years.
I saved each one by hand, reading and editing the HTML to build a self-contained, standalone copy of each web page.

These web pages were made by other people, many using tools and techniques I didn't recognise.
That's what kept me going: I wasn't just archiving, I was learning.
This project became a crash course in how the web is built, and how people actually use it.

Yes, there's plenty of bloat on the web, but that's not news.
You don't need to read thousands of pages to know that.
What *is* worth sharing is all the clever, thoughtful, and surprising stuff I learned along the way.

<blockquote class="toc">
  <p>This article is the second in a four part bookmarking mini-series:</p>
  <ol>
    <li>
      <a href="/2025/bookmarks-static-site/"><strong>Creating a static site for all my bookmarks</strong></a> – why do I bookmark, why use a static site, and how does it work.
    </li>
    <li>
      <a href="/2025/creating-bookmark-archives"><strong>Creating a local archive of all my bookmarks</strong></a> – web archiving, automated vs manual, what I learnt about preserving web pages.
    </li>
    <li>
      <strong>Learning how to make websites by reading two thousand web pages</strong> (this article)
    </li>
    <li>
      <a href="#"><strong>Some cool websites from my bookmark collection</strong></a> (coming 26 May) – some websites which are doing especially fun or clever things with the web.
    </li>
  </ol>
</blockquote>

<style>
  .toc {
    background: var(--background-color);
    border-color: var(--primary-color);
  }

  .toc ol > li:not(:last-child) {
    margin-bottom: 1em;
  }

  .toc a:visited {
    color: var(--primary-color);
  }
</style>

---

## Interetsing HTML tags

I'm loosely aware of semantic HTML exists -- using HTML tags that describe the meaning of your content, not their visual appearance. For example, using a heading tag `<h1>` rather than a bold tag `<b>`. I know the theory and I've read a list of available elements once, but I found it really helpful to see what tags are popular, and how people are actually using them in practice:


### what is `<aside>` for?

<details>
* `\<aside\>` is a tag I was aware of, but I didn't know when I'd use it. I saw lots of examples where it was used to embed content in the middle of the article, like ads, newsletter sign-up forms, pull quotes, links to related or popular articles.

Using `\<aside\>` for related articles is cool!
* also ads
* or see more
* or related comments
* or sidebars
</details>

### the `<mark>` tag

<details>
* `\<mark\>` is a tag for marking or highlighting text, which is used for highlights on Medium articles and pull quotes on other sites. I haven't used it myself yet, but I can imagine using it in code snippets in future.

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
</details>

### the `<section>` tag

* `<section>` is a standalone section of a document, and a tag I'd completely forgotten. I've already started using it in several places in the Flickr Commons Explorer, in place of a more generic `<div>`.

### `<ins>`

	I also saw `<ins>` used for ads on a few sites, which is novel but doesn't feel semantically correct.

`ins` used for ads: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ins


### `<hgroup>`

* `<hgroup>` is a tag for grouping a heading and related content, like a title and a subtitle, for example:
	```html
	<hgroup>
		<h1>All about web bookmarking</h1>
		<p>Posted 16 March 2025</p>
	</hgroup>
	```
	This is another tag I didn’t know about, and I’ve started using it on this site.

### `<video>`

* I replaced a lot of embedded videos with the `<video>` element pointing to a locally downloaded copy of the video, which is the first time I've used this tag in earnest. I still remember reading Kroc Camen’s article [Video is for Everybody](https://camendesign.com/code/video_for_everybody), and it’s nice to finally put that knowledge to use.

  One mistake I kept making was forgetting to close the tag:

  ```html
	<!-- this is wrong -->
	<video controls src="videos/Big_Buck_Bunny.mp4"/>
	```

	This feels like `<img>` which is a self-closing tag, but that's not how `<video>` works. Because it can take child elements, you have to explicitly close it with `</video>`

### `<progress>`

  used by Business insider/Denali to track reading progress

  ```
  <progress class="theme_back-to-home-progress-bar" value="0" data-component-type="progress-bar"></progress>
  ```

### `<base>`

## misc HTML

### ordering elements in the page

* footer/sidebar goes after main content, and then rearranged to the right place

### comments to close HTML tags

```
		</main><!-- #main -->
	</div><!-- #primary -->
```


### instapaper_ignore

* The `instapaper_ignore` attribute, e.g. Atlantic `<aside class="pullquote instapaper_ignore">Computers had doubled in power every 18 months for the last 40 years. Why hadn’t programming changed?</aside>`

https://blog.instapaper.com/post/730281947

### link rel="alternate"

* `link rel="alternate"` for other languages, e.g. Panic
	* ```
```
<link rel="alternate" hreflang="en-us" href="https://blog.panic.com/firewatch-demo-day-at-gdc/">
<link rel="alternate" hreflang="ja" href="https://blog.panic.com/ja/firewatch-demo-day-at-gdc-j/">

### link rel="preload"

link rel="preload"
dns preload

hey, I used this recently!








## CSS

### $= for elements whose

<details>
The [attribute$="value"] selector is used to select elements whose attribute value ends with a specified value.


Home Sweet Homepage:

```
img[src$="page01/image2.png"] {
  left: 713px;
  top: 902px;
}
```
</details>

### The `@import` statement

CSS has `@import` statements, so one stylesheet can load another stylesheet:
```css
@import "fonts.css";
```
I've used the import statement in Sass, and I didn't know this was a feature of vanilla CSS now – but it was in fairly common use.

My CSS is small enough that I package it into a single file for websites served over HTTP (the CSS for this website is only 13KB) – but I've started to use this for static websites I load from my local filesystem.

I don't think CSS supports this yet, but I think imports conditional on a selector might be useful – you can already do conditional imports based on a media query ("only load these styles on a narrow screen") and I think conditional imports based on the presence of a selector would be useful too ("only load these styles if a particular class is use"). I have some longer CSS rules that I don't need on every page, and might be nice to load conditionally (like my styles for good embedded toots).

### Lots of `<!--[if IE]>`

```
<!--[if IE]>
  <style>
    /* old IE unsupported flexbox fixes */
    .greedy-nav .site-title {
      padding-right: 3em;
    }
    .greedy-nav button {
      position: absolute;
      top: 0;
      right: 0;
      height: 100%;
    }
  </style>
<![endif]-->
```


```
style data-href=
or style id="

somthing someting path
```

```html
<style data-href="https://static.parastorage.com/services/editor-elements-library/dist/thunderbolt/rb_wixui.thunderbolt_bootstrap.77c2044d.min.css"></style>
```

EW: what is `box-shadow: inset`?

```
      box-shadow: inset 0 -6px 0 #b0e3fb;

```



### Misc features

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

## JavaScript

### script type=text/template

<details>
  https://stackoverflow.com/questions/4912586/explanation-of-script-type-text-template-script

  zeldman

  ```
  {% raw %}
  <script type="text/template" id="tmpl-subscriber-only-message">
  	<div class="coil-message-inner">
  		<div class="coil-message-header">
  			<# if ( data.headerLogo ) { #>
  				{{{data.headerLogo}}}
  			<# } #>
  			<# if ( data.title ) { #>
  				<p class="coil-message-title">{{data.title}}</p>
  			<# } #>
  			<# if ( data.content ) { #>
  				<p class="coil-message-content">{{data.content}}</p>
  			<# } #>
  			<# if ( data.button.href ) { #>
  				<a target="_blank" href="{{data.button.href}}" class="coil-message-button">{{data.button.text}}</a>
  			<# } #>
  		</div>
  	</div>
  </script>
  {% endraw %}
  ```

</details>

### Developers like to leave messages in the JavaScript console

I always smiled at sites that left a message for people looking in the developer console – often a wave to fellow web developers, or a link to a jobs page.

A couple of sites also used this as a place to leave security warnings for non-developers – apparently there are scammers who send people snippets of JavaScript to run in their web console, which can potentially do a lot of damage. Sites would print scary looking messages "don't trust people who tell you to run code here", but it doesn't seem especially widespread.

people doing security in web console, e.g. tumblr

```
<script>var __pbpa = true;</script><script>var translated_warning_string = 'Warning: Never enter your Tumblr password unless \u201chttps://www.tumblr.com/login\u201d\x0ais the address in your web browser.\x0a\x0aYou should also see a green \u201cTumblr, Inc.\u201d identification in the address bar.\x0a\x0aSpammers and other bad guys use fake forms to steal passwords.\x0a\x0aTumblr will never ask you to log in from a user\u2019s blog.\x0a\x0aAre you absolutely sure you want to continue?';</script><script type="text/javascript" language="javascript" src="pre_tumblelog.js%3F_v=83e88e0d61213141a74383bf5d31425e"></script>
```

### Alternative script types

* other script types `<script type="text/x-handlebars-template" id="loading_animation"><div class="loading_animation pulsing <%= extra_class %> {{ extra_class }}"><div></div></div></script>`

---

## Grab bag

### What does GPT mean on a web page?

Thanks to the meteoric rise of ChatGPT, I've come to associate the acronym "GPT" with large language models (LLMs) -- it stands for [*Generative Pre-trained Transformer*][gpt_wiki].

So I was quite surprised to see "GPT" crop up on web pages that predate the widespread use of generative AI.
It showed up in HTML attributes like this:

```html
<div id="div-gpt-ad-1481124643331-2">
```

In this context, "GPT" stands for [*Google Publisher Tag*][gpt_google], part of Google's ad infrastructure.
I'm not sure exactly what these tags were doing -- and since I stripped all the ads out of my web archive, they're not doing anything now -- but it was clearly ad-related.

[gpt_wiki]: https://en.wikipedia.org/wiki/Generative_pre-trained_transformer
[gpt_google]: https://developers.google.com/publisher-tag/guides/get-started

### Browsers won't load external `file://` resources from `file://` pages

Because my static archives are saved as plain HTML files on disk, I often open them directly using the `file://` protocol, rather than serving them over HTTP.
This mostly works fine -- but I ran into a few cases where pages behave differently depending on how they're loaded.

One example is the [SVG `<use>` element][svg_use].
Some sites I saved use SVG sprite sheets for social media icons, with markup like:

```xml
<use href="sprite.svg#logo-icon"></use>
```

This works over `http://`, but when loaded via `file://`, it silently fails -- the icons don't show up.

It turns out this is a security restriction.
When a `file://` page tries to load another `file://` resource, modern browsers treat it as a [cross-origin request][cross_origin] and block it.
That wasn't always the case, but today it helps prevent a malicious downloaded HTML file from [snooping around your hard drive][cors_file_security].

At first, all I got was a missing icon.
I could see an error in my browser console, but it was a bit vague -- it just said I couldn't load the file for "security reasons".

Eventually, I dropped this into my dev tools console:

```javascript
fetch("sprite.svg")
  .then(response => console.log("Fetch succeeded:", response))
  .catch(error => console.error("Fetch failed:", error));
```

This gave me a different error message, one that explicitly mentioned cross-origin requesting sharing: *"CORS request not http"*.
This gave me something I could look up, to better understand what's going on.

This is easy to work around -- if I spin up a local web server (like Python's [`http.server`][http.server]), I can open the page over HTTP and everything loads correctly.

[svg_use]: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/use
[cross_origin]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
[cors_file_security]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS/Errors/CORSRequestNotHttp#loading_a_local_file
[http.server]: https://docs.python.org/3/library/http.server.html#module-http.server

### I found a bug in the WebKit developer tools

Safari is my regular browser, and I was using it to preview pages as I saved them to my archive.
While I was archiving one of [Jeffrey Zeldman's posts][zeldman], I was struggling to understand how some of his CSS worked.
I could see the rule in my developer tools, but I couldn't figure out why it was behaving the way it was.

Eventually, I discovered the problem: [a bug in WebKit's developer tools][webkit_283428] was introducing whitespace that changed the meaning of the CSS.

For example, suppose the server sends this minifed CSS rule:

```
body>*:not(.black){color:green;}
```

WebKit's dev tools prettify it like this:

```
body > * :not(.black) {
    color: green;
}
```

But these aren't equivalent!

* The original rule matches [direct children] of `<body>` that don't have the `black` class.
* The prettified version matches any descendant of `<body>` that doesn't have the `black` class and that isn't a direct child.

The CSS renders correctly on the page, but the bug means the Web Inspector can show something subtly wrong.
It's a formatting bug that sent me on a proper wild goose chase.

This bug remains unfixed -- but interestingly, a year later, that particular CSS rule has disappeared from Zeldman's site.
I wonder if it caused any other problems?

[zeldman]: https://zeldman.com/2009/08/05/past-blast/
[webkit_283428]: https://bugs.webkit.org/show_bug.cgi?id=283428
[direct children]: https://developer.mozilla.org/en-US/docs/Web/CSS/Child_combinator
