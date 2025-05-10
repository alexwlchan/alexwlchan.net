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
      <ul>
        <li>
          <a href="#html_tags">Interesting HTML tags</a>
          <ul>
            <li><a href="#html_aside">The <code>&lt;aside&gt;</code> element</a></li>
            <li><a href="#html_mark">The <code>&lt;mark&gt;</code> element</a></li>
            <li><a href="#html_section">The <code>&lt;section&gt;</code> element</a></li>
            <li><a href="#html_hgroup">The <code>&lt;hroup&gt;</code> (heading group) element</a></li>
            <li><a href="#html_video">The <code>&lt;video&gt;</code> element</a></li>
            <li><a href="#html_progress">The <code>&lt;progress&gt;</code> indicator element</a></li>
            <li><a href="#html_base">The <code>&lt;base&gt;</code> element</a></li>
          </ul>
        </li>
        <li>
          <a href="#css">Clever corners of CSS</a>
          <ul>
            <li><a href="#css_import">The CSS <code>@import</code> statement</a></li>
            <li><a href="#css_suffix"><code>[attr$=value]</code> is a CSS selector for suffix values</a></li>
            <li><a href="#inset_box_shadows">You can create inner box shadows with <code>inset</code></a></li>
            <li><a href="#css_zoom_in">For images that get bigger, <code>cursor: zoom-in</code> can show a magnifying glass</a></li>
          </ul>
        </li>
        <li>
          <a href="#thoughtful_html">Writing thoughtful HTML</a>
          <ul>
            <li><a href="#html_element_order">What order do elements go in your HTML?</a></li>
            <li><a href="#html_translations">Translated pages with <code>&lt;link rel="alternate"&gt;</code> and <code>hreflang</code></a></li>
            <li><a href="#html_preload">Fetching resources faster with <code>&lt;link rel="preload"&gt;</code></a></li>
            <li><a href="#end_comments">Comments to mark the end of large containers</a></li>
            <li><a href="#css_href">The <code>data-href</code> attribute in <code>&lt;style&gt;</code> tags</a></li>
          </ul>
        </li>
        <li>
          <a href="#quirks">Quirks and relics</a>
          <ul>        
            <li><a href="#gpt">What does GPT stand for in attributes?</a></li>
            <li><a href="#instapaper_ignore">What’s the <code>instapaper_ignore</code> class?</a></li>
            <li><a href="#html_conditional">There are still lots of <code>&lt;!--[if IE]&gt;</code> comments</a></li>
            <li><a href="#js_templates">Templates in <code>&lt;script&gt;</code> tags with a non-standard <code>type</code> attribute</a></li>
            <li><a href="#file_uris">Browsers won’t load external <code>file://</code> resources from <code>file://</code> pages</a></li>
            <li><a href="#webkit_bug">I found a bug in the WebKit developer tools</a></li>
          </ul>
        </li>
      </ul>
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

  .toc ol > li > ul {
    list-style-type: disc;
  }

  .toc ol > li > ul > li > ul {
    list-style-type: circle;
  }

  .toc a:visited {
    color: var(--primary-color);
  }
</style>

---

<h2 id="html_tags">Interesting HTML tags</h2>

I know I've read a list of HTML tags in reference documents (and in [this blog post][weaver] by Patrick Weaver), but there are some tags I'm forgotten, misunderstood, or never seen used in the wild.
Reading thousands of real-world pages gave me a better sense of how these tags are actually used, and when they're useful.

[weaver]: https://www.patrickweaver.net/blog/a-blog-post-with-every-html-element/

<h3 id="html_aside">The <code>&lt;aside&gt;</code> element</h3>

MDN describes [`<aside>`][aside] as "a portion of a document whose content is only indirectly related to the document's main content".
That's probably true, but it's vague enough that I was never quite sure when to use it.
For a while I used `<aside>` for the header on this site, but I eventually swapped it out for `<header>`, which felt more semantically correct.

On other websites, I saw `<aside>` used in the middle of larger articles -- often for things like ads, newsletter sign ups, pull quotes, or links to related articles.
I don't have any of those elements here, but now I have a stronger mental model of where to use `<aside>`.

I saw a couple of sites using the [`<ins>` (inserted text) element][ins] for ads, but I think `<aside>` is a better semantic fit.

[aside]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/aside
[ins]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/ins

<h3 id="html_mark">The <code>&lt;mark&gt;</code> element</h3>

The [`<mark> element`][mark] highlights text, typically with a yellow background.
It's useful for drawing visual attention to a phrase, and I suspect it's helpful or screen readers and parsing tools as well.

I saw it used in Medium to show reader highlights, and I've started using it in code samples when I want to call out specific lines.

[mark]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/mark

<h3 id="html_section">The <code>&lt;section&gt;</code> element</h3>

The [`<section>` tag][section] is a useful way to group content on a page -- more meaningful than a generic `<div>`.
I'd forgotten about it, although I use similar tags like `<article>` and `<main>`.
Seeing it used across different sites reminded me it exists, and I've since added it to a few projects.

[section]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/section

<h3 id="html_hgroup">The <code>&lt;hroup&gt;</code> (heading group) element</h3>

The [`<hgroup>` tag][hgroup] is for grouping a heading with related metadata -- like a title and a publication date:

```html
<hgroup>
    <h1>All about web bookmarking</h1>
    <p>Posted 16 March 2025</p>
</hgroup>
```

This is another tag I'd forgotten, which I've started using on this site.

[hgroup]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/hgroup

<h3 id="html_video">The <code>&lt;video&gt;</code> element</h3>

The [`<video>` tag][video] is used to embed videos in a web page.
It's a tag I've used for a long time -- I still remember reading Kroc Camen's article [Video is for Everybody][everybody] in 2010, back when Flash was still the dominant way to watch video on the(typing) (keyboard clacking)  web.

While building my web archive, I replaced a lot of custom video players with `<video>` elements and local copies of the videos.
One mistake I kept making was forgetting to close the tag, or trying to make it self-closing:

```html
<!-- this is wrong -->
<video controls src="videos/Big_Buck_Bunny.mp4"/>
```

It looks like `<img>`, which is self-closing, but `<video>` can have child elements, you have to explicitly close it with `</video>`.

[video]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video
[everybody]: https://camendesign.com/code/video_for_everybody

<h3 id="html_progress">The <code>&lt;progress&gt;</code> indicator element</h3>

The [`<progress>` element][progress] shows a progress indicator.
I saw it on a number of sites that specialise in longer articles -- they used a progress bar to show you how far you'd read.

<style>
  #progress_example {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-column-gap: 1em;
    align-items: center;
  }

  @media screen and (max-width: 750px) {
    #progress_example {
      grid-template-columns: auto;
      padding-bottom: 1em;
    }
  }
</style>

<blockquote id="progress_example">
  <div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nt">&lt;label</span> <span class="na">for=</span><span class="s">"file"</span><span class="nt">&gt;</span>Progress:<span class="nt">&lt;/label&gt;</span>
<span class="nt">&lt;progress</span> <span class="na">id=</span><span class="s">"file"</span> <span class="na">max=</span><span class="s">"100"</span> <span class="na">value=</span><span class="s">"70"</span><span class="nt">&gt;</span>70%<span class="nt">&lt;/progress&gt;</span></code></pre></div></div>

  <div>
    <label for="file">File progress:</label>
    <progress id="file" max="100" value="70">70%</progress>
  </div>
</blockquote>

I don't have a use for it right now, but I like the idea of getting OS-native progress bars in HTML -- no custom JavaScript or CSS required.

[progress]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/progress

<h3 id="html_base">The <code>&lt;base&gt;</code> element</h3>

The [`<base>` element][base] specifies the base URL to use for any relative URLs in a document.
For example, in this document:

```html
<base href="https://example.com/">

<img src="/pictures/cat.jpg">
```

The image will be loaded from `https://example.com/pictures/cat.jpg`.
I didn't see `<base>` very often, but it's a good reminder that it exists.

[base]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/base



---



<h2 id="css">Clever corners of CSS</h2>

<h3 id="css_import">The CSS <code>@import</code> statement</h3>

CSS has `@import` statements, which allow one stylesheet to load another:

```css
@import "fonts.css";
```
I've used `@import` statement in Sass, but I didn't realise it's now a feature of vanilla CSS now -- and one that's widely used.
My CSS is small enough that I bundle it into a single file for serving over HTTP (the CSS for this website is only 13KB), but I've started using `@import` for static websites I load from my local filesystem.

One feature I'd like -- although I don't think CSS supports it yet -- is conditional imports based on selectors.
That is, only load a stylesheet if a particular element or class is used on the page.

You can already do conditional imports based on a media query ("only load these styles on a narrow screen") and something similar for selectors would be useful too -- for example, "only load these styles if a particular class is visible".
I have some longer rules that aren't needed on every page, like styles for syntax highlighting, and it would be nice to load them only when required.





<h3 id="css_suffix"><code>[attr$=value]</code> is a CSS selector for suffix values</h3>

While reading the [Home Sweet Homepage][hsh], I found a CSS selector I didn't recognise:

```css
img[src$="page01/image2.png"] {
  left: 713px;
  top:  902px;
}
```

This `$=` syntax is a bit of CSS that selects elements whose `src` attribute ends with `page01/image2.png`.
It's one of a several [attribute selectors] that I hadn't seen before -- you can also match exact values, prefixes, or words in space-separated lists.
You can also control whether you want case-sensitive or -insensitive matching.

[hsh]: https://sailorhg.com/home_sweet_homepage/
[attribute selectors]: https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors#attrvalue_5





<h3 id="inset_box_shadows">You can create inner box shadows with <code>inset</code></h3>

Here's a link style from an old copy of the *Entertainment Weekly* website:

<style>
  #underline_example {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-column-gap: 1em;
    align-items: center;
  }

  #underline_example div:nth-child(2) {
    text-align: center;
  }

  @media screen and (max-width: 600px) {
    #underline_example {
      grid-template-columns: auto;
      padding-bottom: 1em;
    }

    #underline_example div:nth-child(2) {
      text-align: left;
    }
  }
</style>

<blockquote id="underline_example">
  <div class="language-css highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nt">a</span> <span class="p">{</span> <span class="nl">box-shadow</span><span class="p">:</span> <span class="nb">inset</span> <span class="m">0</span> <span class="m">-6px</span> <span class="m">0</span> <span class="m">#b0e3fb</span><span class="p">;</span> <span class="p">}</span></code></pre></div></div>

  <div>
    <span style="box-shadow: inset 0 -6px 0 #b0e3fb;">
      A link on EW.com
    </span>
  </div>
</blockquote>

The [`inset` keyword][inset] was new to me: it draws the shadow *inside* the box, rather than outside.
In this case, they're setting `offset-x=0`, `offset-y=-6px` and `blur-radius=0` to create a solid stripe that appears behind the link text -- like a highlighter running underneath it.

If you want something that looks more shadow-like, here are two boxes that show what the inner/outer shadow looks like with a blur radius:

<style>
  #shadow_examples {
    display: grid;
    grid-template-columns: repeat(2, auto);
    grid-gap: 1em;
  }

  #shadow_examples > div {
    width: 150px;
    padding: 0.25em;
    text-align: center;
    display: inline-block;
    margin: 0 auto;
    background: var(--background-color);
  }
</style>

<div id="shadow_examples">
  <div style="box-shadow: inset 0 0 10px var(--primary-color);">
    inner shadow
  </div>
  <div style="box-shadow: 0 0 10px var(--primary-color);">
    outer shadow
  </div>
</div>

I don't have an immediate use for this, but I like the effect, and the subtle sense of depth it creates.

[inset]: https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow#inset

<h3 id="css_zoom_in">For images that get bigger, <code>cursor: zoom-in</code> can show a magnifying glass</h3>

On gallery websites, I often saw this CSS rule used for images that link to a larger version:

```css
cursor: zoom-in;
```

Instead of using `cursor: pointer;` (the typical hand icon for links), this shows a magnifying glass icon -- a subtle cue that clicking will zoom or expand the image.

Here's a quick comparison:

<table>
  <tr>
    <td style="cursor: default; padding-right: 0.5em;">
      <picture>
        <source srcset="/images/2025/bookmarks/default.dark.gif" type="image/gif" media="(prefers-color-scheme: dark)">
        <source srcset="/images/2025/bookmarks/default.gif" type="image/gif" media="(prefers-color-scheme: light)">
        <img src="/images/2025/bookmarks/default.gif" alt="A small icon of an arrow">
      </picture>
    </td>
    <td>
      the <code>default</code> cursor is typically an arrow
    </td>
  </tr>
  <tr>
    <td style="cursor: pointer; padding-right: 0.5em;">
      <picture>
        <source srcset="/images/2025/bookmarks/pointer.dark.gif" type="image/gif" media="(prefers-color-scheme: dark)">
        <source srcset="/images/2025/bookmarks/pointer.gif" type="image/gif" media="(prefers-color-scheme: light)">
        <img src="/images/2025/bookmarks/pointer.gif" alt="A small icon of a hand with a raised pointer finger">
      </picture>
    </td>
    <td>
      the <code>pointer</code> cursor is typically a hand, used to indicate links
    </td>
  </tr>
  <tr>
    <td style="cursor: zoom-in; padding-right: 0.5em;">
      <picture>
        <source srcset="/images/2025/bookmarks/zoom-in.dark.gif" type="image/gif" media="(prefers-color-scheme: dark)">
        <source srcset="/images/2025/bookmarks/zoom-in.gif" type="image/gif" media="(prefers-color-scheme: light)">
        <img src="/images/2025/bookmarks/zoom-in.gif" alt="A small icon of a magnifying sign with a plus symbol">
      </picture>
    </td>
    <td>
      the <code>zoom-in</code> cursor is a magnifying glass with a plus sign, suggesting “click to enlarge”
    </td>
  </tr>
</table>

I knew about the [`cursor` property][cursor], but I'd never thought to use it that way.
It's a nice touch, and I want to remember it for the next time I build a gallery.

[cursor]: https://developer.mozilla.org/en-US/docs/Web/CSS/cursor



---



<h2 id="thoughtful_html">Writing thoughtful HTML</h2>

<h3 id="html_element_order">What order do elements go in your HTML?</h3>

My web pages follow a simple one column design: a header at the top, content in the middle, a footer at the bottom.
I mirror that order in my HTML, because it feels like the natural structure.

I'd never thought about how to order the HTML elements in more complex layouts, when there isn't such a clear visual flow.
For example, many websites have a sidebar that sits alongside the main content.
Which comes first in the HTML?

I don't have a firm answers, but reading how other people structure their HTML got me thinking.
I noticed several pages that put the sidebar at the very end of the HTML, then used CSS to position it visually alongside the content.
That way, the main content appears earlier in the HTML file, which means it can load and become readable sooner.

It's something I want to think more carefully about next time I'm building a more complex page.





<h3 id="html_translations">Translated pages with <code>&lt;link rel="alternate"&gt;</code> and <code>hreflang</code></h3>

I saw a few web pages with translated versions, and they used `<link>` tags with [`rel="alternate">` and an `hreflang` attribute][hreflang] to point to those translations.
Here's an example from [a Panic article][gdc], which is available in both US English and Japanese:

```html
<link rel="alternate" hreflang="en-us" href="https://blog.panic.com/firewatch-demo-day-at-gdc/">
<link rel="alternate" hreflang="ja"    href="https://blog.panic.com/ja/firewatch-demo-day-at-gdc-j/">
```

This seems to be for the benefit of search engines and other automated tools, not web browsers.
If your web browser is configured to prefer Japanese, you'd see a link to the Japanese version in search results -- but if you open the English URL directly, you won't be redirected.

This makes sense to me -- translations can differ in content, and some information might only be available in one language.
It would be annoying if you couldn't choose which version you wanted.

Panic's article includes a third `<link rel="alternate">` tag:

```html
<link rel="alternate" hreflang="x-default" href="https://blog.panic.com/firewatch-demo-day-at-gdc/">
```

This [`x-default` value][x-default] is a fallback, used when there's no better match for the user's language.
For example, if you used a French search engine, you'd be directed to this URL because there isn't a French translation.

Almost every website I've worked has been English-only, so internationalisation is a part of the web I know very little about.

[hreflang]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel#values
[gdc]: https://blog.panic.com/firewatch-demo-day-at-gdc/
[x-default]: https://developers.google.com/search/blog/2013/04/x-default-hreflang-for-international-pages





<h3 id="html_preload">Fetching resources faster with <code>&lt;link rel="preload"&gt;</code></h3>

I saw a lot of websites that with `<link rel="preload">` tags in their `<head>`.
This tells the browser about resources that will be needed soon, so it should start fetching them immediately.

Here's an example from this site:

```html
<link rel="preload" href="https://alexwlchan.net/theme/white-waves-transparent.png" as="image" type="image/png"/>
```

That image is used as a background texture in my CSS file.
Normally, the browser would have to download and parse the CSS before it even knows about the image -- which means a delay before it starts loading it.
By preloading the image, the browser can begin downloading the image in parallel with the CSS file, so it's already in progress when the browser reads the CSS.

The difference is probably imperceptible on a fast connection, but it is a performance improvement -- and as long as you scope the preloads correctly, there's little downside. (You just don't want to preload resources that aren't used).

I saw some sites use [DNS prefetching], which is a similar idea.
The `rel="dns-prefetch"` attribute tells the browser about domains it'll fetch resources from soon, so it should begin DNS resolution early.
The most common example was websites using Google Fonts:

```html
<link rel="dns-prefetch" href="https://fonts.googleapis.com/" />
```

I only added `preload` tags to my site [a few weeks ago][flash].
I'd seen them in other web pages, but I didn't appreciate the value until I wrote one of my own.

[flash]: /2025/fix-dark-mode/
[DNS prefetching]: https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/dns-prefetch





<h3 id="end_comments">Comments to mark the end of large containers</h3>

I saw a lot of websites (mostly WordPress) that used HTML comments to mark the end of containers with a lot of content.
For example:

```html
<div id="primary">
  <main id="main">
    …
  </main><!-- #main -->
</div><!-- #primary -->
```

These comments made the HTML much easier to read -- I could see exactly where each component started and ended.

I like this idea, and I'm tempted to use it in my more complex projects.
I can imagine this being especially helpful in template files, where HTML is mixed with template markup in a way that might confuse [code folding], or make the structure harder to follow.

[code folding]: https://en.wikipedia.org/wiki/Code_folding




<h3 id="css_href">The <code>data-href</code> attribute in <code>&lt;style&gt;</code> tags</h3>

Here's a similar idea: I saw a number of sites set a `data-href` attribute on their `<style>` tags, as a way to indicate the source of the CSS.
Something like:

```html
<style data-href="https://example.com/style.css">{% comment %}</style>{% endcomment %}
```

It's a neat idea that I imagine could be useful for developers working on that web page.





---





<h2 id="quirks">Quirks and relics</h2>

<h3 id="gpt">What does GPT stand for in attributes?</h3>

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





<h3 id="instapaper_ignore">What’s the <code>instapaper_ignore</code> class?</h3>

I found some pages that use the `instapaper_ignore` CSS class to hide certain content.
Here's an example from an [Atlantic article][torching] I saved in 2017:

```html
<aside class="pullquote instapaper_ignore">
  Somewhere at Google there is a database containing 25 million books and nobody is allowed to read them.
</aside>
```

Instapaper is a "read later" service -- you save an article that looks interesting, and later you can read it in the Instapaper app.
It includes a text parser that extract the article's text, stripping away junk or clutter.

The `instapaper_ignore` class is a way for publishers to control what that parser includes.
From [a blog post in 2010][instapaper_ignore]:

> Additionally, the Instapaper text parser will support some standard CSS class names to instruct it:
>
> * `instapaper_body`: This element is the body container.
> * `instapaper_ignore`: These elements, when inside the body container, should be removed from the text parser’s output.

In this example, the element is a pull quote -- a repeated line from the article, styled to stand out.
On the full web page, it works.
But in the unstyled Instapaper view, it would just look like a duplicate sentence.
It makes sense that the Atlantic wouldn't want it to appear in that context.

Only a handful of pages I've saved ever used `instapaper_ignore`, and even fewer are still using it today.
I don't even know if Instapaper's parser still looks atfor it

This stood out to me because I was an avid Instapaper user for many years.
I deleted my Instapaper account years ago, and I don't hear much about "read later" apps these days -- but then I stumble across a quiet little relic like this, buried in the HTML.

[torching]: https://www.theatlantic.com/technology/archive/2017/04/the-tragedy-of-google-books/523320/
[instapaper_ignore]: https://blog.instapaper.com/post/730281947





<h3 id="html_conditional">There are still lots of <code>&lt;!--[if IE]&gt;</code> comments</h3>

Old versions of Internet Explorer supported [conditional comments], which allowed developers to add IE-specific behaviour to their pages.
Internet Explorer would render the contents of the comment as HTML, while other browsers ignored it.
This was a common workaround for deficiencies in IE, when pages needed specific markup or styles to render correctly.

Here's an example, where the developer adds an IE-specific style to fix a layout issue:

```html
<!--[if IE]>
  <style>
    /* old IE unsupported flexbox fixes */
    .greedy-nav .site-title {
      padding-right: 3em;
    }
  </style>
<![endif]-->
```

Developers could also target specific versions of IE:

```html
<!--[if lte IE 7]><link rel="stylesheet" href="/css/ie.css"><![endif]-->
```

Some websites even used conditional comments to display warnings and encourage users to upgrade, like this message which that's still present on [the RedMonk website](https://redmonk.com) today:

```html
<!--[if IE]>
  <div class="alert alert-warning">
    You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.
  </div>
<![endif]-->
```

This syntax was already disappearing by the time I started building websites -- support for conditional comments was removed in Internet Explorer 10, released in 2012, the same year that Google Chrome became the most-used browser worldwide.
I've never written one of these comments, and they were a reminder of how much harder it used to be to make websites.

Like the `instapaper_ignore` class, these comments are a relic of an earlier web.
Most websites have removed them, but they live on in web archives -- and in the memories of developers who had to make things work in IE, one way or another.

[conditional comments]: https://en.wikipedia.org/wiki/Conditional_comment



<h3 id="js_templates">Templates in <code>&lt;script&gt;</code> tags with a non-standard <code>type</code> attribute</h3>

I came across a few pages using `<script>` tags with a `type` attribute that I didn't recognise.
Here's a simple example:

```html
<script type="text/x-handlebars-template" id="loading_animation">
  <div class="loading_animation pulsing <%= extra_class %> {{ extra_class }}"><div></div></div>
</script>
```

Browsers ignore `<script>` tags [an unrecognised `type`][script_unknown_type] -- they don't run them, and they don't render their contents.
Developers used this as a way to [include HTML templates][old_template] in their pages, which JavaScript could extract and use later.

This trick was so widespread that HTML introduced a dedicated [`<template>` tag][template] element for the same purpose.
It's been in all the major browsers for years, but there are still instances of this old technique floating around the web.

[script_unknown_type]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script/type#any_other_value
[old_template]: https://stackoverflow.com/a/4912608/1558022
[template]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/template





<h3 id="file_uris">Browsers won’t load external <code>file://</code> resources from <code>file://</code> pages</h3>

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





<h3 id="webkit_bug">I found a bug in the WebKit developer tools</h3>

Safari is my regular browser, and I was using it to preview pages as I saved them to my archive.
While I was archiving one of [Jeffrey Zeldman's posts][zeldman], I was struggling to understand how some of his CSS worked.
I could see the rule in my developer tools, but I couldn't figure out why it was behaving the way it was.

Eventually, I discovered the problem: [a bug in WebKit's developer tools][webkit_283428] was introducing whitespace that changed the meaning of the CSS.

For example, suppose the server sends this minifed CSS rule:

```css
body>*:not(.black){color:green;}
```

WebKit's dev tools prettify it like this:

```css
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
