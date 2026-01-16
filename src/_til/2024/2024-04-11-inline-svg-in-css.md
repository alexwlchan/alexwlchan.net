---
layout: til
date: 2024-04-11 18:28:43 +01:00
title: How to embed an inline SVG in a CSS rule
summary: |
  Modern browsers allow you to embed the SVG almost as-is, with just a couple of characters that need escaping – no base64 required!
tags:
  - css
  - svg
---
As part of redesigning this site, I was moving some of my small SVGs out of external files and inlining them in CSS rules.
In my head, the way you do this is by base64-encoding the SVG and shoving it in a `url()` function, for example:

```css
background-image: url('data:image/svg+xml;base64,PD94…')
```

Encoding all your SVGs with base64 has a couple of drawbacks: it's impossible to read the SVG in the web inspector tools, and it's a fairly inefficient encoding, making all the files a third or so bigger.

Fortunately the web has moved on since the last time I did this!
You can now embed the SVG in close-to-unmodified form:

```css
background-image: url("data:image/svg+xml;charset=UTF-8,<svg xmlns=%22http:/…");
```

The tricky part is encoding the SVG correctly -- if the SVG can't be read properly, you get a blank space in place of your image.
The two characters that caused me a lot of hassle were double quote (`"` &rarr; `%22`) and the octothorpe in hex colours (`#` &rarr; `%23`).

But I got it working eventually, and now I have inline SVGs in CSS which are both readable and fairly efficiently encoded.

## Working example

Here's an example of how I'm using it in the site redesign, to replace `<hr>` elements with a line of orange squares:

```html
<style>
  hr {
    width: 100px;
    height: 5px;
    border: 0;
    background-image: url('data:image/svg+xml;charset=UTF-8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 25 5%22 width=%2225px%22 height=%225px%22><rect width=%225%22 height=%225%22 fill=%22%23ff9900%22/></svg>');
    background-size:   contain;
    background-repeat: repeat-x;
  }
</style>

<p>Hello world</p>

<hr>

<p>Goodbye world</p>
```