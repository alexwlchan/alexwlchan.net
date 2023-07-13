---
layout: post
title: "My custom &lt;picture&gt; plugin for Jekyll"
summary:
tags: web-development jekyll blogging-about-blogging
colors:
  index_light: "#d62b56"
  index_dark:  "#fd96af"
---

About seven months ago, I did a complete rewrite of how I handle images on this site.
It's working well and nothing seems to have broken, so I thought it might be good to explain what I'm doing.

For readers: I want images to load quickly and look good.
That means looking sharp on high-resolution displays, but without forcing everyone to download massive images.

For me: I want images to be easy to manage.
It should be easy for me to add images to a post, and to customise them if I want to do something special.

One way to achieve this is with vector images, i.e. SVGs.
Those are great for simple diagrams and drawings, but they don't work for photographs and screenshots.

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

This expands into a larger chunk of HTML, which refers to nine different variants of the image:

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
    style="aspect-ratio: 3 / 4; "
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
Another approach would be to use a dedicated image CDN and create these derivative images at request time (e.g. [imgix] or [Netlify Large Media]), but I'm already doing custom steps in my Jekyll build and it was easier to extend that mechanism than add a new service.

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
[WebP] and AVIF

[WebP]: https://en.wikipedia.org/wiki/WebP
[AVIF]: https://en.wikipedia.org/wiki/AVIF

---

I wrote a custom Jekyll plugin



* use an image cdn?
  * no learning
  * another build step – already have jekyll
  * money!!!

* get picture
* get dimensions (e.g. 1024 × 768)
* create sizes of image at 1x, 2x, 3x, 4x e.g. 300px wide => 300px, 600px, 900px versions
  - use <picture> and <source>
  - fall back to <img> at 1x
* create versions in AVIF, WebP -- good compression! almost too good. not gr9 for v small images
* queued in jekyll build process because slow
* passthru other attributes
* doesn't require alt text

<picture> <source srcset="/images/profile_green_500w.avif 500w, /images/profile_green_640w.avif 640w, /images/profile_green_1x.avif 750w, /images/profile_green_1000w.avif 1000w, /images/profile_green_1250w.avif 1250w, /images/profile_green_2x.avif 1500w, /images/profile_green_3x.avif 2250w" sizes="(max-width: 750px) 100vw, 750px" type="image/avif"> <source srcset="/images/profile_green_500w.webp 500w, /images/profile_green_640w.webp 640w, /images/profile_green_1x.webp 750w, /images/profile_green_1000w.webp 1000w, /images/profile_green_1250w.webp 1250w, /images/profile_green_2x.webp 1500w, /images/profile_green_3x.webp 2250w" sizes="(max-width: 750px) 100vw, 750px" type="image/webp"> <source srcset="/images/profile_green_500w.jpg 500w, /images/profile_green_640w.jpg 640w, /images/profile_green_1x.jpg 750w, /images/profile_green_1000w.jpg 1000w, /images/profile_green_1250w.jpg 1250w, /images/profile_green_2x.jpg 1500w, /images/profile_green_3x.jpg 2250w" sizes="(max-width: 750px) 100vw, 750px" type="image/jpeg"> <img src="/images/profile_green_1x.jpg" alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants." class="rounded_corners" width="750" style="aspect-ratio: 4 / 3; "> </picture>