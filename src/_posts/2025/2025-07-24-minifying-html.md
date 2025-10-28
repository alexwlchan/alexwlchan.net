---
layout: post
date: 2025-07-24 21:59:10 +0000
title: Minifying HTML on my Jekyll website
summary: I compare three different approaches to minifying HTML.
tags:
  - html
  - blogging about blogging
  - jekyll
---
I minify all the HTML on this website -- removing unnecessary whitespace, tidying up attributes, optimising HTML entities, and so on.
This makes each page smaller, and theoretically the website should be slightly faster.

I'm not going to pretend this step is justified by the numbers.
My pages are already pretty small pre-minification, and it only reduces the average page size by about 4%.
In June, minification probably saved less than MiB of bandwidth.

But I do it anyway.
I minify HTML because I like tinkering with the website, and I enjoy finding ways to make it that little bit faster or more efficient.
I recently changed the way I'm minifying HTML, and I thought this would be a good time to compare the three approaches I've used and share a few things I learned about HTML along the way.

I build this website using [Jekyll](https://jekyllrb.com), so I've looked for Jekyll or Ruby-based solutions.

{% table_of_contents %}

<h2 id="layout">Approach #1: <a href="http://jch.penibelst.de/">Compress HTML in Jekyll</a>, by Anatol Broder</h2>

This is a Jekyll layout that compresses HTML.
It's a single HTML file written in pure [Liquid](https://shopify.github.io/liquid/) (the templating language used by Jekyll).

First you save the HTML file to `_layouts/compress.html`, then reference it in your highest-level layout.
For example, in `_layouts/default.html` you might write:

```html
---
layout: compress
---

<html>
{% raw %}{{ content }}{% endraw %}
</html>
```

Because it's a single HTML file, it's easy to install and doesn't require any plugins.
This is useful if you're running in an environment where plugins are restricted or disallowed (which I think includes [GitHub Pages](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll#plugins), although I'm not 100% sure).

The downside is that the single HTML file can be tricky to debug, it only minifies HTML (not CSS or JavaScript), and there's no easy way to cache the output.

<h2 id="htmlcompressor">Approach #2: The <a href="https://github.com/paolochiodi/htmlcompressor/">htmlcompressor gem</a>, by Paolo Chiodi</h2>

The [htmlcompressor gem](https://github.com/paolochiodi/htmlcompressor/) is a Ruby port of [Google's Java-based HtmlCompressor](https://code.google.com/archive/p/htmlcompressor/).
The README describes it as an "alpha version", but in my usage it was very stable and it has a simple API.

I start by changing my `compress.html` layout to pass the page content to a `compress_html` filter:

```html
---
---

{% raw %}{{ content | compress_html }}{% endraw %}
```

This filter is defined as [a custom plugin](https://jekyllrb.com/docs/plugins/filters/); I save the following code in `_plugins/compress_html.rb`:

{% code lang="ruby" names="0:run_compress_html 1:html 3:options 4:compressor 12:Jekyll 13:CompressHtmlFilter 14:compress_html 15:html 16:cache" %}
def run_compress_html(html)
  require 'htmlcompressor'

  options = {
    remove_intertag_spaces: true
  }
  compressor = HtmlCompressor::Compressor.new(options)
  compressor.compress(html)
end

module Jekyll
  module CompressHtmlFilter
    def compress_html(html)
      cache = Jekyll::Cache.new('CompressHtml')

      cache.getset(html) do
        run_compress_html(html)
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::CompressHtmlFilter)
{% endcode %}

I mostly stick with the default options; the only extra rule I enabled was to remove inter-tag spaces.
Consider the following example:

```html
<p>hello world</p> <p>my name is Alex</p>
```

By default, htmlcompressor will leave the space between the closing `</p>` and the opening `<p>` as-is.
Enabling `remove_intertag_spaces` makes it a bit more aggressive, and it removes that space.

I'm using the [Jekyll cache](/2024/jekyll-caching/) to save the results of the compression -- most pages don't change from build-to-build, and it's faster to cache the results than recompress the HTML each time.

The gem seems abandoned -- the last push to GitHub was in 2017.

<h2 id="minifyhtml">Approach #3: The <a href="https://github.com/wilsonzlin/minify-html">minify-html library</a>, by Wilson Lin</h2>

This is a Rust-based HTML minifier, with bindings for a variety of languages, including Ruby, Python, and Node.
It's very fast, and even more aggressive than other minifiers.

I use it in a very similar way to `htmlcompressor`.
I call the same `compress_html` filter in `_layouts/compress.html`, and then my `run_compress_html` in `_plugins/compress_html.rb` is a bit different:

{% code lang="ruby" names="0:run_compress_html 1:html 3:options" %}
def run_compress_html(html)
  require 'minify_html'

  options = {
    keep_html_and_head_opening_tags: true,
    keep_closing_tags: true,
    minify_css: true,
    minify_js: true
  }

  minify_html(html, options)
end
{% endcode %}

This is a much more aggressive minifier.
For example, it turns out that the `<html>` and `<head>` elements are optional in an HTML5 document, so this minifier removes them if it can.
I've disabled this behaviour, because I'm old-fashioned and I like my pages to have `<html>` and `<head>` tags.

This library also allows minifying inline CSS and JavaScript, which is a nice bonus.
That has some rough edges though: there's [an open issue with JS minification](https://github.com/wilsonzlin/minify-html/issues/242), and I had to tweak several of my if-else statements to work with the minifier.
Activity on the GitHub repository is sporadic, so I don't know if that will get fixed any time soon.

<h2 id="verify">Minify, but verify</h2>

After I minify HTML, but before I publish the site, I run [HTML-Proofer to validate my HTML](/2019/checking-jekyll-sites-with-htmlproofer/).

I'm not sure this has ever caught an issue introduced by a minifer, but it gives me peace of mind that these tools aren't mangling my HTML.
(It has caught plenty of issues caused by my mistakes!)

<h2 id="comparison">Comparing the three approaches</h2>

<style>
  table#sizes {
    width: 100%;
    border: var(--border-width) var(--border-style) var(--block-border-color);
    border-radius: var(--border-radius);
    background-color: var(--block-background);
    padding: var(--default-padding);
  }

  table#sizes tr:not(:last-of-type) > th,
  table#sizes tr:not(:last-of-type) > td {
    border-bottom: 2px solid var(--block-border-color);
  }

  table#sizes td:not(:first-child) {
    text-align: center;
  }

  table#sizes tr > td:nth-child(2) {
    padding-left: 1em;
  }
</style>

There are two key metrics for HTML minifiers:

*   **Speed:** this is a dead heat.
    When I built the site with a warm cache, it takes about 2.5s whatever minifier I'm using.
    The `htmlcompressor` gem and `minify-html` library are much slower if I have a cold cache, but that's only a few extra seconds and it's rare for me to build the site that way.

*   **File size:** the Ruby and Rust-based minifiers achieve slightly better minification, because they're more aggressive in what they trim.
    For example, they're smarter about removing unnecessary spaces and quoting around attribute values.

    Here's the average page size after minification:

    <table id="sizes">
      <tr>
        <th>Approach</th>
        <th>Average HTML page size</th>
      </tr>
      <tr>
        <td>Without minification</td>
        <td title="15,306 bytes">14.9 KiB</td>
      </tr>
      <tr>
        <td>Compress HTML in Jekyll 3.2.0</td>
        <td title="14,617 bytes">14.3 KiB</td>
      </tr>
      <tr>
        <td>htmlcompressor 0.4.0</td>
        <td title="14,383 bytes">14.0 KiB</td>
      </tr>
      <tr>
        <td>minify-html 0.16.4</td>
        <td title="13,844 bytes">13.5 KiB</td>
      </tr>
    </table>

I'm currently using minify-html.
This is partly because it gets slightly smaller page sizes, and partly because it has bindings in other languages.
This website is my only major project that uses Ruby, and so I'm always keen to find things I can share in my other non-Ruby projects.
If minify-html works for me (and it is so far), I can imagine using it elsewhere.
