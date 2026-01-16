---
layout: post
date: 2023-01-15 21:46:18 +00:00
title: Beware of transparent backgrounds when using AVIF with ImageMagick 6
summary: You probably want to use version 7.
tags:
  - blogging about blogging
  - images
  - imagemagick
colors:
  css_light: "#333333"
  css_dark:  "#cccccc"
---

One of the things I did over my Christmas break was redo all the image handling on this site.
Mostly I'm catching up on the current "best practices" for images on the web.
I've written a [Jekyll plugin][plugin] which allows me to use an image in a post like so:

```liquid
{% raw %}{%
  picture
  filename="wc_500_error.png"
  alt="An 'Internal Server Error' page."
  width="582"
  class="screenshot"
%}{% endraw %}
```

This creates multiple copies of the image, in different sizes, which are sent to the browser in the [`<picture>` tag][picture] -- so browsers can pick the best size for your device, which often makes pages smaller and faster than they were before.

It also includes image dimensions (width and aspect ratio), so a browser can work out how big an image will appear on the page before it's been loaded.
This reduces layout shift, and combined with the [`loading="lazy"` attribute][lazy] can further save data.

But the big discovery for me was modern image formats like WebP and AVIF, which are much smaller than formats like JPEG and PNG.
WebP is good, AVIF is unbelievably good – literally.
When I first enabled AVIF support, I thought I'd broken something, because a 5x compression ratio over WebP (which is what I'm seeing for some images) seemed impossible.

I had it all tested and working, so imagine my dismay when I opened [my latest post](/2023/upward-assignment/) on my phone and discovered the images were broken:

<style type="x-text/scss">
  #avif_comparison {
    display: grid;
    grid-template-columns: auto auto;
    width: 600px;
    grid-column-gap: var(--grid-gap);

    picture:nth-child(1) img {
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
      grid-row: 1 / 2;
      grid-column: 1 / 2;
    }

    picture:nth-child(2) img {
      border-top-left-radius: 0;
      border-bottom-left-radius: 0;
      grid-row: 1 / 2;
      grid-column: 2 / 2;
    }

    figcaption {
      grid-row: 2 / 2;
      grid-column: 1 / span 2;
    }
  }
</style>

<figure id="avif_comparison">
  {%
    picture
    filename="avif_image_broken.png"
    alt="A web page showing a hand-drawn diagram with some red text, and a black background which makes the diagram impossible to follow."
    width="300"
    class="screenshot"
  %}
  {%
    picture
    filename="avif_image_working.png"
    alt="The same web page, but now the diagram has a transparent background and shows through the white of the underlying page. The diagram is now legible."
    width="300"
    class="screenshot"
  %}
  <figcaption>
    Left: a screenshot taken in Safari on iOS 16, loading the AVIF image.
    Right: a screenshot taken with the original PNG image.
  </figcaption>
</figure>

I found the bug pretty quickly: I'd inadvertently downgraded from ImageMagick 7 to ImageMagick 6, and when you create an AVIF image in ImageMagick&nbsp;6, it replaces transparent backgrounds with black ones.
Oops.
I hadn't noticed because my desktop browser doesn't have AVIF support yet; it was loading the WebP image, which looked fine.

I've upgraded back to ImageMagick 7 using the [IMEI installer scripts][imei], which seems to resolve the problem.
I've also added a check for similar issues in future.

You can tell if an image has transparent pixels using the [`%[opaque]` format specifier][opaque]:

```console
$ identify -format '%[opaque]' image_with_transparency.png
False

$ identify -format '%[opaque]' image_without_transparency.png
True
```

Note that this tells you if an image has all-opaque pixels, so `False` means the image is transparent, and `True` means it isn't.

I've added this to my Jekyll plugin: after it creates a new size/format of image, it checks to see if transparency has been lost in the conversion process.
If it finds a blatted background, it will raise an error for me to investigate.

This is the downside of creating lots of image sizes/formats -- even a few images in a post can spiral into dozens of derivatives, more than I can check by hand.
I think I've fixed the issues now, but if you spot any more broken images, please do [let me know](mailto:alex@alexwlchan.net).

> **Update, 22 December 2024:** I had an email from Paulo Paracatu, who tells me this has been fixed in ImageMagick 6.9.12-68 with commit [cc4e5a6](https://github.com/ImageMagick/ImageMagick6/commit/cc4e5a6383961c03d340e0237feedfff83f9af0b).
> I haven't been able to verify this myself, but it sounds like good news for anybody who has to use ImageMagick 6.

[responsive images]: https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images
[picture]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture
[plugin]: https://github.com/alexwlchan/alexwlchan.net/blob/live/src/_plugins/tag_picture.rb
[lazy]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-loading
[imei]: https://github.com/SoftCreatR/imei
[opaque]: https://imagemagick.org/script/escape.php
