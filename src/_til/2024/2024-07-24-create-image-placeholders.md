---
layout: til
title: Create solid-colour image placeholders to show before an image loads
date: 2024-07-24 22:39:41 +0100
tags:
  - images
  - css
---
A fairly common pattern I use in my web pages is to have a solid colour placeholder that shows where the image will appear, and which is replaced by the image when it loads.

I like this because it avoids weird gaps in the web page before the image loads, and is minimally intrusive.
(As opposed to low-resolution versions of the image, which I find slightly jarring.)

Here's a recent example from the Commons Explorer, which shows how the page looks before and after an image loads:

{%
  picture
  filename="image_placeholders.png"
  alt="Screenshot of two images side-by-side. On the left, the area where the image should be is a large purple region. On the right, the image has loaded and there's a black-and-white of a man on a windswept mountain with several dogs."
  width="600"
  class="screenshot"
%}

This is the HTML and CSS I use to achieve this effect:

```html
<div class="thumbnail_wrapper">
  <img src="…">
</div>
```

```css
--width:  …;
--height: …;
--color:  …;

.thumbnail_wrapper {
  aspect-ratio: calc(var(--width) / var(--height));
  background:   var(--color);
}

.thumbnail_wrapper img {
  width: 100%;
  display: block;
}
```

The `thumbnail_wrapper` div is set to the right size with the `aspect-ratio` property, and then I add the solid colour background.

The `img` is set to fill the container div, and `display: block` is to avoid any space between the bottom of the image and the bottom of the div -- by default, an `img` element is `display: inline`, which adds a small gap as part of the line height.

**Note:** If your `--width` and `--height` are pure numeric values (e.g. `--width: 1024`) then you can remove the `calc()`.
If they specify a dimension (e.g. `--width: 1024px`) then you need the `calc()`.
