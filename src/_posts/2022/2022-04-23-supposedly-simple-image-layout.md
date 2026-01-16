---
layout: post
date: 2022-04-23 23:03:46 +00:00
title: Creating a “simple” three-up image layout in CSS
summary: A step-by-step breakdown of how I made a one-left, two-right layout for my images.
tags:
  - css
  - web development
colors:
  index_light: "#4b536e"
  index_dark:  "#a7a7af"
---

I've been toying with a new layout for an upcoming post: a three-up display of images, with one big image on the left and two smaller images on the right.
I wanted something a bit more visually interesting than a scrolling vertical list.
This is the sort of thing I mean:

<style>
  /* Make sure the grids don't overflow on mobile layout */
  .grid1, .grid2, .grid3, .grid4, .grid5 {
    max-width: 100%;
  }
</style>

<figure style="width: 392px;">
  {%
    picture
    filename="image_layout.png"
    alt="The image layout I've described, with a picture of a starry sky (left), the planet Jupiter half in shadow with a moon in front of it (upper right), and the International Space Station floating above the Earth."
    width="392"
  %}
  <figcaption>
    A mockup I made in Keynote.
    These are images of <a href="https://solarsystem.nasa.gov/resources/2500/the-view-from-earth-space-station-jupiter-milky-way/">the Earth’s sky</a>, <a href="https://solarsystem.nasa.gov/resources/803/jupiter-and-io/">Jupiter and Io</a>, and the <a href="https://www.nasa.gov/image-feature/the-station-pictured-from-the-spacex-crew-dragon-6">International Space Station (ISS)</a>, all published by NASA.
    The trail of light in the sky is the ISS captured in a thirteen-second exposure, and the bright dot next to it is Jupiter.
  </figcaption>
</figure>

If you've done a lot of front-end web development, this sort of thing probably seems quite easy -- I've seen websites with much more complex layouts.

But I don't do much front-end work, so I wasn't sure how to go about this.
It took a lot of experimentation and research to get something I was happy with -- so let's walk through it together.



## Step 1: Get on the grid

Although I don't do much front-end development, I am vaguely aware of [CSS Grid].
I know it's the "new" approach to doing complex layouts, and I've dabbled with it for a few projects.
(I put "new" in air quotes because it's been around for years, but I'm only just starting to use it.)

Here's a simple three-cell grid using divs:

```html
<div class="grid">
  <div class="item left">left grid item</div>
  <div class="item upper_right">upper right grid item</div>
  <div class="item lower_right">lower right grid item</div>
</div>
```

and the CSS that matches it:

```css
.grid {
  display: grid;
  grid-template-columns: calc(66% - 5px) calc(34% - 5px);
  grid-template-rows:    calc(50% - 5px) calc(50% - 5px);
  grid-gap: 10px;
}

.grid .left_image {
  grid-column: 1 / 2;
  grid-row: 1 / span 2;
  /* equivalent to:
  grid-row-start: 1;
  grid-row-end: 2;
  */
}

.grid .right_upper_image {
  grid-column: 2 / 2;
  grid-row: 1 / 2;
}

.grid .right_lower_image {
  grid-column: 2 / 2;
  grid-row: 2 / 2;
}
```

The `display: grid;` property switches the div into grid mode, and the `-template-columns` and `-template-rows` properties tell the grid how tall/wide the columns and rows should be.

I'm using percentages of the width/height of the overall grid, then subtracting 5&nbsp;pixels to account for the grid spacing.
I want the rows to be equal height, and the first column to be twice as wide as the second.
There are lots of ways to define these sizes and this may not be optimal, but it makes sense to me.
I did try using the `fr` unit, which is the [fraction of flexible space][fr] -- but I ran into some weird issues when the content of the grid items overflowed, so I gave up.

The `grid-row` and `grid-column` properties on individual items tell them where to sit in the grid.
For the item on the left-hand side, the `1 / span 2` value tells it to start in row 1 and fill 2 rows.

This is what it looks like.
I've added some background colours so the different items stand out:

<style>
  .grid1 {
    display: grid;
    grid-template-columns: calc(66% - 5px) calc(34% - 5px);
    grid-template-rows:    calc(50% - 5px) calc(50% - 5px);
    grid-gap: 10px;
  }

  .grid1 .left {
    grid-column: 1 / 2;
    grid-row: 1 / span 2;
  }

  .grid1 .upper_right {
    grid-column: 2 / 2;
    grid-row: 1 / 2;
  }

  .grid1 .lower_right {
    grid-column: 2 / 2;
    grid-row: 2 / 2;
  }

  /** These values don't define the grid layout,
    * but they make it easier to follow what's going on. */
  .grid1 {
    width: 300px;
    margin-left:  auto;
    margin-right: auto
  }

  .grid1 .left {
    background: #00a1ff;
    color: white;
  }

  .grid1 .upper_right {
    background: #ed220d;
    color: white;
  }

  .grid1 .lower_right {
    background: #60d937;
    color: white;
  }
</style>

<figure style="width: 300px;">
  <div class="grid1">
    <div class="item left">left grid item</div>
    <div class="item upper_right">upper right grid item</div>
    <div class="item lower_right">lower right grid item</div>
  </div>
  <figcaption>
    Edit this example <a href="https://codepen.io/alexwlchan/pen/abEMdgY">on CodePen</a>.
  </figcaption>
</figure>

This looks a bit like what I want!

At this point I could use the `background-image` property on the divs to get images into the layout, and call it a day -- but I don't like that approach.
Among other reasons, there's no way to specify alt text on background images, and screen readers [will ignore them][access_concerns].
Maybe I could hack something into a div, but it feels like swimming against the tide.
I wanted to find a way to use `<img>` tags, because they're more semantically appropriate and they're more accessible.

[CSS Grid]: https://en.wikipedia.org/wiki/CSS_grid_layout
[fr]: https://www.w3.org/TR/css-grid-1/#fr-unit
[access_concerns]: https://developer.mozilla.org/en-US/docs/Web/CSS/background-image#accessibility_concerns




## Step 2: Adding images to the grid

Let's start by just dropping the images into the grid, and see what happens:

```html
<div class="grid">
  <div class="item left">
    <img src="/night_sky.jpg">
  </div>
  <div class="item upper_right">
    <img src="/jupiter.jpg">
  </div>
  <div class="item lower_right">
    <img src="/iss.jpg">
  </div>
</div>
```

<style>
  .grid2 {
    display: grid;
    grid-template-columns: calc(66% - 5px) calc(34% - 5px);
    grid-template-rows: calc(50% - 5px) calc(50% - 5px);
    grid-gap: 10px;
  }

  .grid2 .left {
    grid-column: 1 / 2;
    grid-row: 1 / span 2;
  }

  .grid2 .upper_right {
    grid-column: 2 / 2;
    grid-row: 1 / 2;
  }

  .grid2 .lower_right {
    grid-column: 2 / 2;
    grid-row: 2 / 2;
  }

  /** These values don't define the grid layout,
    * but they make it easier to follow what's going on. */
  .grid2 {
    width: 400px;
    margin-left: auto;
    margin-right: auto;
  }

  .grid2 .left {
    background: #00a1ff;
  }

  .grid2 .upper_right {
    background: #ed220d;
  }

  .grid2 .lower_right {
    background: #60d937;
  }

  /** This removes the CSS properties for images I set in my site's CSS. */
  .grid2 img {
    max-width: none;
    margin-left:  0;
    margin-right: 0;
  }
</style>

<figure style="width: 400px;">
  <div class="grid2">
    <div class="item left">
      {%
        picture
        filename="sky.jpg"
        alt="A starry night sky, with a tree in silhouette in the foreground. In the background is a bright white streak, next to a bright white dot that stands out from the other stars."
        width="250"
      %}
    </div>
    <div class="item upper_right">
      {%
        picture
        filename="jupiter.jpg"
        alt="The planet Jupiter, but with only the left-hand side of the planet visible; the other half is hidden in shadow. A smaller moon is passing in front of it, also partially in shadow."
        width="113"
      %}
    </div>
    <div class="item lower_right">
      {%
        picture
        filename="iss.jpg"
        alt="The International Space Station, a collection of silver tubes and panels, floating in space above the Earth."
        width="113"
      %}
    </div>
  </div>
  <figcaption>
    Edit this example <a href="https://codepen.io/alexwlchan/pen/bGaZpGE">on CodePen</a>.
  </figcaption>
</figure>

This gets the images in the right place, but they're the wrong sizes -- they've overflowing out of the grid.
How do we make them fit?

(As a sidebar: I vaguely wonder if there's a way to make the images the grid items and bypass a layer of `<div>`s, but I haven't found anything that works.)



## Step 3: Set the width and height of the images

We can tell the images to completely fill the grid items by setting `width` and `height` properties, but it's a bit crude:

```css
.grid .item img {
  width:  100%;
  height: 100%;
}
```

<style>
  .grid3 {
    display: grid;
    grid-template-columns: calc(66% - 5px) calc(34% - 5px);
    grid-template-rows: calc(50% - 5px) calc(50% - 5px);
    grid-gap: 10px;
  }

  .grid3 .left {
    grid-column: 1 / 2;
    grid-row: 1 / span 2;
  }

  .grid3 .upper_right {
    grid-column: 2 / 2;
    grid-row: 1 / 2;
  }

  .grid3 .lower_right {
    grid-column: 2 / 2;
    grid-row: 2 / 2;
  }

  .grid3 .item img {
    width:  100%;
    height: 100%;
  }

  /** These values don't define the grid layout,
    * but they make it easier to follow what's going on. */
  .grid3 {
    width: 400px;
    margin-left: auto;
    margin-right: auto;
  }

  /** This removes the CSS properties for images I set in my site's CSS. */
  .grid3 img {
    max-width: none;
    margin-left:  0;
    margin-right: 0;
  }
</style>

<figure style="width: 400px;">
  <div class="grid3">
    <div class="item left">
      {%
        picture
        filename="sky.jpg"
        alt="A starry night sky."
        width="250"
      %}
    </div>
    <div class="item upper_right">
      {%
        picture
        filename="jupiter.jpg"
        alt="Jupiter and Io."
        width="113"
      %}
    </div>
    <div class="item lower_right">
      {%
        picture
        filename="iss.jpg"
        alt="The International Space Station."
        width="113"
      %}
    </div>
  </div>
  <figcaption>
    Edit this example <a href="https://codepen.io/alexwlchan/pen/LYeaNya">on CodePen</a>.
  </figcaption>
</figure>

The percentage values are relative to the containing element -- in this case, the grid items that were coloured red/green/blue.
This gets us flush edges, but now the images have been distorted -- they've been stretched to fill the container.
(Notice how Jupiter has become much less circular.)

If I was making this layout in a graphics editor, I'd expand the images while maintaining the aspect ratio, then crop them to fit.
Can we achieve that with CSS?



## Step 4: Add the object-fit property

To unbreak the aspect ratio, I discovered a new-to-me CSS property: [object-fit].
This defines how an element (say, an image or video) should be resized to fit into a container.

The default value is `object-fit: fill`, which expands the element to completely fill the container, and stretches the object to fit, ignoring the original aspect ratio.
That's what's causing the distortion in the example above.

After experimenting with the other values (I had to try it myself to really understand how they worked), I think the value I want is `object-fit: cover`.
This expands an element while maintaining its aspect ratio, and if it doesn't fit perfectly then extra bits get clipped out -- the edges of the image get cropped.
That's what I'd do if I was making this layout by hand!

Let's add that CSS rule:

```css
.grid .item img {
  object-fit: cover;
}
```

<style>
  .grid4 {
    display: grid;
    grid-template-columns: calc(66% - 5px) calc(34% - 5px);
    grid-template-rows: calc(50% - 5px) calc(50% - 5px);
    grid-gap: 10px;
  }

  .grid4 .left {
    grid-column: 1 / 2;
    grid-row: 1 / span 2;
  }

  .grid4 .upper_right {
    grid-column: 2 / 2;
    grid-row: 1 / 2;
  }

  .grid4 .lower_right {
    grid-column: 2 / 2;
    grid-row: 2 / 2;
  }

  .grid4 .item img {
    width:  100%;
    height: 100%;
    object-fit: cover;
  }

  /** These values don't define the grid layout,
    * but they make it easier to follow what's going on. */
  .grid4 {
    width: 400px;
    margin-left: auto;
    margin-right: auto;
  }

  /** This removes the CSS properties for images I set in my site's CSS. */
  .grid4 img {
    max-width: none;
    margin-left:  0;
    margin-right: 0;
  }
</style>

<figure style="width: 400px;">
  <div class="grid4">
    <div class="item left">
      {%
        picture
        filename="sky.jpg"
        alt="A starry night sky."
        width="250"
      %}
    </div>
    <div class="item upper_right">
      {%
        picture
        filename="jupiter.jpg"
        alt="Jupiter and Io."
        width="113"
      %}
    </div>
    <div class="item lower_right">
      {%
        picture
        filename="iss.jpg"
        alt="The International Space Station."
        width="113"
      %}
    </div>
  </div>
  <figcaption>
    Edit this example <a href="https://codepen.io/alexwlchan/pen/eYyXZer">on CodePen</a>.
  </figcaption>
</figure>

Now the edges of the images are being cropped out (for example, we can't see the solar panels on the ISS), but they're no longer being distorted.
Hopefully there's nothing important in the edges, but there's an [object-position] property that lets me choose exactly how to fit the image into the crop if the default isn't quite right.

When I have large images in a post, I usually embed a smaller thumbnail which links to the full resolution image.
That's another reason not to worry too much about cropping around the edges -- if somebody really wants to see all the detail, they can follow the link.

This is pretty close to what I want; the last thing I want to tweak is the overall aspect ratio.

[object-fit]: https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit
[object-position]: https://developer.mozilla.org/en-US/docs/Web/CSS/object-position



## Step 5: Setting the aspect ratio

The last time I looked at setting an aspect ratio in CSS, there were weird tricks with padding and positioning that I didn't really understand.
I was expecting to use this work to learn about that properly, and really wrap my head around it -- but it turns out, I don't need to.

There's another CSS property called [aspect-ratio] which lets you set a preferred aspect ratio for a container.
If you add this property, you can change the size of the overall grid; for example:

```css
.grid {
  aspect-ratio: 16 / 9;
}
```

<style>
  .grid5 {
    aspect-ratio: 16 / 9;

    display: grid;
    grid-template-columns: calc(66% - 5px) calc(34% - 5px);
    grid-template-rows: calc(50% - 5px) calc(50% - 5px);
    grid-gap: 10px;
  }

  .grid5 .left {
    grid-column: 1 / 2;
    grid-row: 1 / span 2;
  }

  .grid5 .upper_right {
    grid-column: 2 / 2;
    grid-row: 1 / 2;
  }

  .grid5 .lower_right {
    grid-column: 2 / 2;
    grid-row: 2 / 2;
  }

  .grid5 .item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /** These values don't define the grid layout,
    * but they make it easier to follow what's going on. */
  .grid5 {
    width: 400px;
    margin-left: auto;
    margin-right: auto;
  }
</style>

<figure style="width: 400px;">
  <div class="grid5">
    <div class="item left">
      {%
        picture
        filename="sky.jpg"
        alt="A starry night sky."
        width="250"
      %}
    </div>
    <div class="item upper_right">
      {%
        picture
        filename="jupiter.jpg"
        alt="Jupiter and Io."
        width="113"
      %}
    </div>
    <div class="item lower_right">
      {%
        picture
        filename="iss.jpg"
        alt="The International Space Station."
        width="113"
      %}
    </div>
  </div>
  <figcaption>
    Edit this example <a href="https://codepen.io/alexwlchan/pen/xxpBrvR">on CodePen</a>.
  </figcaption>
</figure>

This is a new-ish property that only started appearing in browsers about a year or so ago, and I don't have a good sense for when it's safe to adopt new CSS.
[Can I use][can_i_use_ar] says it's supported by about 84% of users, which feels a bit low -- and [skimming Twitter][twitter] shows mixed opinions on whether it's safe to use, or whether you still need a fallback.

Because this is only for my blog posts, I'm going to save myself a padding palaver and use aspect-ratio.
If I was working on a larger website with more visitors, I might make a different decision.

[twitter]: https://twitter.com/search?q=css%20aspect-ratio
[aspect-ratio]: https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio
[can_i_use_ar]: https://caniuse.com/mdn-css_properties_aspect-ratio




## Putting it all together

This is what my new component looks like:

```html
<div class="grid">
  <div class="item left">
    <img src="/night_sky.jpg">
  </div>
  <div class="item upper_right">
    <img src="/jupiter.jpg">
  </div>
  <div class="item lower_right">
    <img src="/iss.jpg">
  </div>
</div>
```

```css
.grid {
  display: grid;
  grid-template-columns: calc(66% - 5px) calc(34% - 5px);
  grid-template-rows:    calc(50% - 5px) calc(50% - 5px);
  grid-gap: 10px;
  aspect-ratio: 16 / 9;
}

.grid .left {
  grid-column: 1 / 2;
  grid-row:    1 / span 2;
}

.grid .upper_right {
  grid-column: 2 / 2;
  grid-row:    1 / 2;
}

.grid .lower_right {
  grid-column: 2 / 2;
  grid-row:    2 / 2;
}

.grid .item img {
  width:  100%;
  height: 100%;
  object-fit: cover;
}
```

<figure style="width: 400px;">
  <div class="grid5">
    <div class="item left">
      {%
        picture
        filename="sky.jpg"
        alt="A starry night sky."
        width="250"
      %}
    </div>
    <div class="item upper_right">
      {%
        picture
        filename="jupiter.jpg"
        alt="Jupiter and Io."
        width="113"
      %}
    </div>
    <div class="item lower_right">
      {%
        picture
        filename="iss.jpg"
        alt="The International Space Station."
        width="113"
      %}
    </div>
  </div>
</figure>

I have an image layout that does what I want, and more importantly, that I understand.
I know how it works, and I'll know how to change it if I want to tweak something later.
There are lots of snippets that I could have mindlessly copied, but I know how this works.

This step-by-step breakdown is pretty close to how I actually built the layout.
I created an empty HTML file and started writing.
Every time I made progress, I copied the file and started working on the copy -- so I could try new things without losing what I'd already achieved.
I've removed a few dead ends and tidied up the examples, but otherwise the post is pretty close to those original files.

Writing it all out in this post helped cement my understanding -- although I [struggled] to get it working, now I've written detailed explanations I think I'll be able to remember it.

It's been a long time since you could "View Source" on a web page and reliably get comprehensible HTML, but I've always liked that idea and tried to preserve it on this site.
These layouts will let me keep doing that.

[struggled]: https://jvns.ca/blog/2021/05/24/blog-about-what-you-ve-struggled-with/
