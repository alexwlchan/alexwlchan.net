---
layout: post
date: 2023-07-15 06:46:12 +00:00
title: "My custom &lt;picture&gt; plugin for Jekyll"
summary: How I make images that load quickly and look good for readers, and which are easy for me to manage.
tags:
  - web development
  - jekyll
  - blogging about blogging
colors:
  css_light: "#df1b4a"
  css_dark:  "#fd96af"
---

About seven months ago, I did a complete rewrite of how I handle images on this site.
It's working well and nothing seems to have broken, so I thought it might be good to explain what I'm doing.

For readers: I want images to load quickly and look good.
That means looking sharp on high-resolution displays, but without forcing everyone to download massive images.

For me: I want images to be easy to manage.
It should be easy for me to add images to a post, and to customise them if I want to do something special.

One way to achieve this is with vector images – SVGs.
Those are great for simple diagrams and drawings, and I use them plenty, but they don't work for photographs and screenshots.

For bitmap images, I wrote a [custom Jekyll plugin][plugin].
Usually my original image is a JPEG or a PNG.
I save it in `_images`, and then I include my custom `{% raw %}{% picture %}{% endraw %}` tag in the Markdown source:

```{% raw %}
{%
  picture
  filename="IMG_9016.jpg"
  width="750"
  class="photo"
  alt="A collection of hot pink flowers, nestled among some dark green leaves in a greenhouse."
%}
{% endraw %}```

This expands into a larger chunk of HTML, which refers to several different variants of the image:

```html
<picture>
  <source
    srcset="/images/2023/IMG_9016_1x.avif 750w,
            /images/2023/IMG_9016_2x.avif 1500w,
            /images/2023/IMG_9016_3x.avif 2250w"
    sizes="(max-width: 750px) 100vw, 750px"
    type="image/avif"
  >
  <source
    srcset="/images/2023/IMG_9016_1x.webp 750w,
            /images/2023/IMG_9016_2x.webp 1500w,
            /images/2023/IMG_9016_3x.webp 2250w"
    sizes="(max-width: 750px) 100vw, 750px"
    type="image/webp"
  >
  <source
    srcset="/images/2023/IMG_9016_1x.jpg 750w,
            /images/2023/IMG_9016_2x.jpg 1500w,
            /images/2023/IMG_9016_3x.jpg 2250w"
    sizes="(max-width: 750px) 100vw, 750px"
    type="image/jpeg"
  >
  <img
    src="/images/2023/IMG_9016_1x.jpg"
    width="750"
    style="aspect-ratio: 3 / 4;"
    class="photo"
    alt="A collection of hot pink flowers, nestled among some dark green leaves in a greenhouse."
  >
</picture>
```

Let's unpack what's going on.

[plugin]: https://github.com/alexwlchan/alexwlchan.net/blob/5cd88f9a34c5197f7d41b21dda3e8c81dc00d9b9/src/_plugins/tag_picture.rb

---

## Getting the path to the image file

My `_images` directory is organised into per-year folders:

```
.
└─ _images/
    ├─ 2022/
    │   ├─ acme_corporation.jpg
    │   ├─ alarm_console.png
    │   ├─ alfred_search.png
    │   └─ ...164 other files
    └─ 2023/
        ├─ amazon-cheetah-listing.jpg
        ├─ avif_image_broken.png
        ├─ bedroom_layout.png
        └─ ...53 other files
```

Organising files per-year matches the URL structure of individual posts (`/:year/:slug`), and helps keep the folder just a bit more manageable.
I have ~1300 images, and throwing them all in a single folder would get unwieldy.
In this example, the original file is `_images/2023/IMG_9016.jpg`.

How does the plugin find an image in this directory structure?

I pass a `filename` attribute to the `{% raw %}{% picture %}{% endraw %}` tag, which tells you the name of the image file, but notice that I don't pass a year anywhere.

That's because my plugin can work it out automatically -- when Jekyll renders a [custom liquid tag][tag_plugin] on a page, it passes the page as a context variable.
That means each instance of my picture tag knows which article it's in, and it can get the article's publication date.
Then it can construct the path to the original image.

```ruby
module Jekyll
  class PictureTag < Liquid::Tag
    def render(context)
      article = context.registers[:page]
      date = article['date']
      year = date.year

      path = "_images/#{year}/#{filename}"
      …
```

I use this technique in a couple of plugins -- it allows me to organise my files without too much hassle when using them.

[tag_plugin]: https://jekyllrb.com/docs/plugins/tags/

---

## Getting different sizes of the image

I pass a `width` attribute to my `{% raw %}{% picture %}{% endraw %}` tag -- this tells the plugin how wide the image will appear on the page.
This mimics the [HTML attribute of the same name][width_attribute].

I get the dimensions of the original image using the [rszr gem]:

```ruby
require 'rszr'

image = Rszr::Image.load(source_path)
puts image.width
```

Then I use ImageMagick to create multiple derivative images, at different widths for different screen pixel densities -- 1x, 2x, or 3x.
I don't create derivatives that are wider than the original image; that would be wasteful.

```ruby
widths_to_create =
  (1..3)
    .map { |pixel_density| pixel_density * visible_width }
    .filter { |w| w <= image.width }
```

For example, if the original file is 250px wide, and I want to show the image at 100px wide, then the plugin would create a 1x image (100px) and a 2x image (200px) but not a 3x image (because 300px is wider than the original image).

This resizing happens as part of the Jekyll build process.
An alternative would be to use a proper image CDN and create these derivative images at request time (e.g. [imgix] or [Netlify Large Media]), but I'm already doing custom steps in my Jekyll build and it was easier to extend that mechanism than add a new service.
It also makes it easier to work with images in a local Jekyll server.

To tell the browser about these different sizes, I use the HTML `picture` and `source` tags, the latter with an `srcset` attribute:

```html
<picture>
  …
  <source
    srcset="/images/2023/IMG_9016_1x.jpg 750w,
            /images/2023/IMG_9016_2x.jpg 1500w,
            /images/2023/IMG_9016_3x.jpg 2250w"
    sizes="(max-width: 750px) 100vw, 750px"
    type="image/jpeg"
  >
  <img
    src="/images/2023/IMG_9016_1x.jpg"
    width="750"
    …
  >
</picture>
```

In this example, the `srcset` attribute tells the browser that there are three different widths of image available, and where to find them.
The `sizes` attribute tells it which size to use at different screen widths.
If the screen is less than 750px wide, then the image fills the entire screen (`100vw`), otherwise the image is 750px wide.
That's not always exactly right -- sometimes margins mean it's slightly wrong -- but it's close enough.

This is enough information for the browser to decide the best size to load.
It knows your screen pixel density and the width of the window, so it can choose an image which (1) will look sharp and crisp on your display and (2) doesn't include lots of unnecessary pixels.

If your browser doesn't support `<picture>` and `<source>`, I include the 1x size in the `<img>` tag.
I figure that if your browser is that old, it's unlikely you're using a high pixel density display.

[width_attribute]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#width
[rszr gem]: https://github.com/mtgrosser/rszr
[imgix]: https://imgix.com
[Netlify Large Media]: https://www.netlify.com/products/large-media/

---

## Getting different formats of the image

JPEG and PNG are fine, but they're a bit long in the tooth – there are newer image formats that look the same but with smaller files.
[WebP] and [AVIF] are modern image formats that are much smaller, which means faster loading images for you and a cheaper bandwidth bill for me.

Alongside the different sizes of image, I'm using ImageMagick to create variants in WebP and AVIF.
These get presented as alternative `<source>` entries in the `<picture>` tag, for example:

```html
<picture>
  <source
    srcset="/images/2023/IMG_9016_1x.avif 750w,
            /images/2023/IMG_9016_2x.avif 1500w,
            /images/2023/IMG_9016_3x.avif 2250w"
    sizes="(max-width: 750px) 100vw, 750px"
    type="image/avif"
  >
  <source
    …
    type="image/webp"
  >
  <source
    …
    type="image/jpeg"
  >
  …
</picture>
```

Not every browser supports WebP and AVIF, which is why I'm providing all three variants.
Your browser knows which formats it supports, and will choose appropriately.

The compression is pretty remarkable: the WebP images are about half the size of the originals, but the AVIF images are one sixth!
When I first enabled AVIF support, I thought something was broken -- the files were so small, it looked wrong to me.

(It turns out [something was broken][transparency], but it was nothing to do with file sizes.)

[WebP]: https://en.wikipedia.org/wiki/WebP
[AVIF]: https://en.wikipedia.org/wiki/AVIF
[transparency]: /2023/check-for-transparency/

---

## Providing explicit dimensions for all my images

Because I have the image dimensions from rszr, I can calculate the aspect ratio of the image and insert it [as a property][ar_property] on the `<img>` tag:

```html
<img
  src="/images/2023/IMG_9016_1x.jpg"
  width="750"
  style="aspect-ratio: 3 / 4;"
  …
>
```

Combined with the `width`, this allows a browser to completely calculate the area an image will take up the page -- before it loads the image.
This means it can lay out the page immediately, leave the right amount of space for the image, and it won't have to rearrange the page later.
The fancy term for this is ["Cumulative Layout Shift"][cls], and too much of it can be distracting -- setting these two attributes reduces it to zero.

[ar_property]: https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio
[cls]: https://web.dev/optimize-cls/

---

## Passing through other attributes to the &lt;img&gt;

Aside from the `filename` attribute, all the attributes on the `{% raw %}{% picture %}{% endraw %}` get passed directly to the underlying `<img>` tag.
I use this for includes things like alt text, CSS classes and inline styles.
It looks exactly like the HTML might look.

This gives me a bunch of flexibility for tweaking the behaviour of images on a per-post basis.
I get the benefits of the different sizes and image formats, and it all looks like familiar HTML.

The plugin is doing a bit of work to parse the attributes, and combine them with any attributes that it's adding (for example, appending the `aspect-ratio` property to any inline styles), but this is largely invisible when I'm just writing a post.

One of the attributes I use most often is [`loading="lazy"`][lazy], which gets me browser-native lazy loading of images.
This improves performance on pages with lots of images, and it's easy for browsers to work out which images to load – they know exactly where each image will go thanks to the `width` and `aspect-ratio` properties.

[lazy]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#loading

---

When the web was young, images were much simpler. You’d upload your JPEG file to your web server, add an `<IMG>` tag to your HTML page, and you were done.
That still works (including the uppercase HTML tags), but there’s a lot more we can do now.

Building this plugin has been one of the more complex bits of front-end web development I've done for this site.
Creating the various images with ImageMagick was fairly straightforward, but setting up the `srcset` and `sizes` attributes so browsers would pick the right image was much harder.
I think it behaves correctly now, and adding images to new posts is pretty seamless – but it took a while to get there.

This was a great way for me to learn how images work in the modern web, but it's hard to recommend my "write it from scratch" approach.
There are lots of existing libraries and tools that make it easy for you to use images on your website, without all the work I had to do first.

I'm the only person who works on this website, and I'm doing it for fun.
I can make very different choices than if I was working on a commercial site managed by a large team.
I enjoyed writing this plugin, and I'm pleased with my snazzy new images, and for me that's all that matters.
