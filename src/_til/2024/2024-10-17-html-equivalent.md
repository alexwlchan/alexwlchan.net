---
layout: til
title: HTML strings may not be equivalent if you minify them
summary: |
  There's a lot of whitespace in HTML which looks irrelevant at first glance, but may be significant and cause the document to render differently.
date: 2024-10-17 09:54:59 +01:00
tags:
  - html
---
I was working on some HTML templates, and I wanted to test they were creating the right HTML.
In particular, I wanted to write an assertion that the actual HTML and the expected HTML were the same.

The actual HTML was minified, for example:

```html
<ul><li>Hello world</li><li>Hello world</li><li>Hello world</li></ul>
```

This is tricky to read, and I wanted the expected HTML to be prettified, such as:

```html
<ul>
  <li>
    Hello world
  </li>
  <li>
    Hello world
  </li>
  <li>
    Hello world
  </li>
</ul>
```

<style>
  .two_columns {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap:   var(--grid-gap);
  }
</style>

These two strings aren't equal, but I thought they might be equivalent because the whitespace inside the `<li>` tags gets collapsed and they look visually the same:

<blockquote class="two_columns">
  <div>
    <p><strong>minified:</strong></p>
    <ul><li>Hello world</li><li>Hello world</li><li>Hello world</li></ul>
  </div>

  <div>
    <p><strong>prettified:</strong></p>
    <ul class="prettified">
      <li>
        Hello world
      </li>
      <li>
        Hello world
      </li>
      <li>
        Hello world
      </li>
    </ul>
  </div>
</blockquote>

For a while I tried various approaches to parse the HTML so I could treat it as something other than a string, and compare it that way -- e.g. parsing it as a DOM element and using [isEqualNode()](https://developer.mozilla.org/en-US/docs/Web/API/Node/isEqualNode) -- but I couldn't find a way to prove the HTML was equivalent without minifying it.

And then it hit me: I can't prove these two HTML elements are equivalent, because they're not.
They may render the same right now, but that's because my browser is collapsing the whitespace.
But consider what happens if I tell the browser to treat the whitespace as significant:

```
li { white-space: pre; }
```

Now the two lists look different:

<style>
  #significant_whitespace li {
    white-space: pre;
  }
</style>

<blockquote class="two_columns" id="significant_whitespace">
  <div>
    <p><strong>minified:</strong></p>
    <ul><li>Hello world</li><li>Hello world</li><li>Hello world</li></ul>
  </div>

  <div>
    <p><strong>prettified:</strong></p>
    {% raw %}
    <ul class="prettified">
      <li>
        Hello world
      </li>
      <li>
        Hello world
      </li>
      <li>
        Hello world
      </li>
    </ul>
    {% endraw %}
  </div>
</blockquote>

So the whitespace can be significant!

This is one of those things that makes sense now I think about it, but it's helpful to have a working example.

I already knew that `<pre>` is whitespace-sensitive, but that feels like a special snowflake tag.
It occurred to me that this could affect other tags when I remembered that `<pre>`'s special handling of whitespace is really just a CSS rule which is applied by default.

<script>
  /* This is to deal with the fact I have an HTML minifier that runs over
   * this site's output, so I need to unminify the HTML to show the example
   * properly. */
  window.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.prettified').forEach(elem => elem.innerHTML = `<li>\n  Hello world\n</li>\n<li>\n  Hello world\n</li>\n<li>\n  Hello world\n</li>\n`);
  });
</script>