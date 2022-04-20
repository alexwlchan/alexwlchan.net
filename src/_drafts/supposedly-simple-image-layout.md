---
layout: post
title: Creating a “simple” three-up image layout in CSS
summary:
tags: css
---

Recently I was working on a new web component: a three-up layout of images, with one on the left and two on the right.
I was looking for something a bit more visually interesting than a scrolling vertical list.
This is the sort of thing I mean:

<figure style="width: 392px;">
  <img src="/images/2022/image_layout.png" style="width: 392px;">
  <figcaption>
    A mockup I made in Keynote.
    These are images of <a href="https://solarsystem.nasa.gov/resources/2500/the-view-from-earth-space-station-jupiter-milky-way/">the Earth’s sky</a>, <a href="https://solarsystem.nasa.gov/resources/803/jupiter-and-io/">Jupiter and Io</a>, and the <a href="https://www.nasa.gov/image-feature/the-station-pictured-from-the-spacex-crew-dragon-6">International Space Station (ISS)</a>, all published by NASA.
    The trail of light in the sky is the ISS captured in a thirteen-second exposure, and the bright dot next to it is Jupiter.
  </figcaption>
</figure>

If you've done a lot of front-end web development, this sort of layout probably seems quite easy -- many websites have much more complex layouts, and this is simple by comparison.

But I don't do much front-end work, and it took a lot of frustration and head-banging to get something I was happy with -- so let's walk through it together.



## Step 1: Get on the grid

Although I don't do much front-end development, I am vaguely aware of [CSS Grid].
I know it's the "new" approach to doing complex layouts, and I've dabbled with it for a few projects.
(I put "new" in air quotes because it's been a thing for years, but I'm only just starting to use it.)

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
There are lots of ways to define these sizes and this may not be optimal, but it makes sense to me.
I did try using the `fr` unit, which is the [fraction of flexible space][fr] -- but I ran into some weird issues when the content of the grid items overflowed, so I have up.

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
    <img src="/sky.jpg">
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
      <img src="/images/2022/sky_thumb.jpg">
    </div>
    <div class="item upper_right">
      <img src="/images/2022/jupiter_thumb.jpg">
    </div>
    <div class="item lower_right">
      <img src="/images/2022/iss_thumb.jpg">
    </div>
  </div>
  <figcaption>
    Edit this example <a href="https://codepen.io/alexwlchan/pen/bGaZpGE">on CodePen</a>.
  </figcaption>
</figure>

So we've got the images in the right place, but they're the wrong sizes -- they've overflowing out of the grid.
How do we make them fit?



## Step 3: Set the width and height of the images

We can fill the space by setting `width` and `height` properties on the image, but it's a bit crude:

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
      <img src="/images/2022/sky_thumb.jpg">
    </div>
    <div class="item upper_right">
      <img src="/images/2022/jupiter_thumb.jpg">
    </div>
    <div class="item lower_right">
      <img src="/images/2022/iss_thumb.jpg">
    </div>
  </div>
  <figcaption>
    Edit this example <a href="https://codepen.io/alexwlchan/pen/LYeaNya">on CodePen</a>.
  </figcaption>
</figure>

This gets us flush edges, but now the images have been distorted -- they've been stretched to fill the container.
(Notice how Jupiter has become much less circular.)

If I was making this layout in a graphics editor, I'd expand the images while maintaining the aspect ratio, then crop them to fit.
Can we achieve that with CSS?



## Step 4: Add the object-fit property

To unbreak the aspect ratio, I discovered a new-to-me CSS property: [object-fit].
This defines how an element (say, an image or video) should be resized to fit into a container.

The default value is `object-fit: fill`, which expands the element to completely fill the container, and stretches the object to fit.
That's what's causing the distorted aspect ratio in the example above.

After experimenting with the other values (I had to try it myself to really understand how they worked), I think the value I want is `object-fit: cover`.
This expands an element while maintaining its aspect ratio, and if it doesn't fit perfectly then extra bits get clipped out -- the edges of the image get cropped.
That's what I'd do if I was making this layout by hand!

Let's add that CSS rule:

```css
.grid img {
  object-fit: cover;
}
```

<div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; grid-gap: 10px; width: 400px; margin-left: auto; margin-right: auto;">
  <div style="grid-column: 1 / 2; grid-row: 1 / span 2;">
    <img src="/images/2022/sky_thumb.jpg" style="max-width: none; width: 100%; height: 100%; object-fit: cover;">
  </div>

  <div style="grid-column: 2 / 2; grid-row: 1 / 2;">
    <img src="/images/2022/jupiter_thumb.jpg" style="max-width: none; width: 100%; height: 100%; object-fit: cover;">
  </div>

  <div style="grid-column: 2 / 2; grid-row: 2 / 2;">
    <img src="/images/2022/iss_thumb.jpg" style="max-width: none; width: 100%; height: 100%; object-fit: cover;">
  </div>
</div>

Now the edges of the images are being cropped out (for example, we can't see the solar panels on the ISS), but they're no longer being distorted.

[object-fit]: https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit

<div style="width: 100%; padding-top: 33%; position:relative; max-width: 800px;">
  <div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; grid-gap: 10px; width: 400px; margin-left: auto; margin-right: auto; position: absolute; top:0;left:0;bottom:0;right:0; height: 100%;">
    <div style="grid-column: 1 / 2; grid-row: 1 / span 2;">
      <img src="/images/2022/sky_thumb.jpg" style="max-width: none; width: 100%; height: 100%; object-fit: cover;">
    </div>

    <div style="grid-column: 2 / 2; grid-row: 1 / 2;">
      <img src="/images/2022/jupiter_thumb.jpg" style="max-width: none; width: 100%; height: 100%; object-fit: cover;">
    </div>

    <div style="grid-column: 2 / 2; grid-row: 2 / 2;">
      <img src="/images/2022/iss_thumb.jpg" style="max-width: none; width: 100%; height: 100%; object-fit: cover;">
    </div>
  </div>
</div>

?category=planets_jupiter



<ol>

  <li>
    Super squished, add the cover:
  <li>
    Now add an aspect ratio

    <div style="width: 100%; padding-top: 33%; position:relative; max-width: 800px;">

      <div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; grid-gap: 10px; position: absolute; top:0;left:0;bottom:0;right:0; height: 100%;">
        <div style="grid-column: 1 / 2; grid-row: 1 / span 2; background: red;">
          <img src="./6185949404_3e247d2ec1_o.jpg" style="width: 100%; height: 100%; object-fit: cover;">
        </div>

        <div style="grid-column: 2 / 2; grid-row: 1 / 2; background: green;">
          <img src="./6185949404_3e247d2ec1_o.jpg" style="width: 100%; height: 100%; object-fit: cover;">
        </div>

        <div style="grid-column: 2 / 2; grid-row: 2 / 2; background: blue;">
          <img src="./6185949404_3e247d2ec1_o.jpg" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
      </div>

    </div>

    aaaa

  </li>

  <!-- <li>



<div class="container" style="background-color: green; width: 100%; padding-top: 50%; position:relative; max-width: 800px;">
  <div style="display: grid; grid-template-columns: calc(65% - 5px) calc(35% - 5px); grid-template-rows: repeat(2, 25vw - 5px); grid-gap: 10px; border: 2px solid blue; position: absolute; top:0;left:0;bottom:0;right:0;">

    <a href="./6185949404_3e247d2ec1_o.jpg" style="grid-column: 1 / 2; grid-row: 1 / span 2;">
      <img src="./6185949404_3e247d2ec1_o.jpg" style="width: 100%; height: 100%; object-fit: cover">
    </a>

    <a href="./6171517470_6abcf7ea9c_o.jpg" style="grid-column: 2 / 2; grid-row: 1 / 2; background: green;">
      <img src="./6171517470_6abcf7ea9c_o.jpg" style="width: 100%; height: 100%; object-fit: cover; display: block;">
    </a>

    <a href="./6170979921_a575aec60b_o.jpg" style="grid-column: 2 / 2; grid-row: 2 / 2; background: yellow;">
      <img src="./6170979921_a575aec60b_o.jpg" style="width: 100%; height: 100%; object-fit: cover; display: block;">
    </a>
  </div>
</div>




<!--<style>
  *,
  *::after,
  *::before {
    margin: 0;
    padding: 0;
    box-sizing: inherit;
  }

  html {
    box-sizing: border-box;
    font-size: 62.5%;
  }

  body {
    font-family: "Nunito", sans-serif;
    color: #333;
    font-weight: 300;
    line-height: 1.6;
  }

  .container {
    width: 60%;
    margin: 2rem auto;
  }

  .gallery {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    grid-template-rows: repeat(8, 5vw);
    grid-gap: 1.5rem;
  }

  .gallery__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .gallery__item--1 {
    grid-column-start: 1;
    grid-column-end: 3;
    grid-row-start: 1;
    grid-row-end: 3;

    /** Alternative Syntax **/
    /* grid-column: 1 / span 2;  */
    /* grid-row: 1 / span 2; */
  }

  .gallery__item--2 {
    grid-column-start: 3;
    grid-column-end: 5;
    grid-row-start: 1;
    grid-row-end: 3;

    /** Alternative Syntax **/
    /* grid-column: 3 / span 2;  */
    /* grid-row: 1 / span 2; */
  }

  .gallery__item--3 {
    grid-column-start: 5;
    grid-column-end: 9;
    grid-row-start: 1;
    grid-row-end: 6;

    /** Alternative Syntax **/
    /* grid-column: 5 / span 4;
    grid-row: 1 / span 5; */
  }

  .gallery__item--4 {
    grid-column-start: 1;
    grid-column-end: 5;
    grid-row-start: 3;
    grid-row-end: 6;

    /** Alternative Syntax **/
    /* grid-column: 1 / span 4;  */
    /* grid-row: 3 / span 3; */
  }

/*  .gallery__item--5 {
    grid-column-start: 1;
    grid-column-end: 5;
    grid-row-start: 6;
    grid-row-end: 9;

    /** Alternative Syntax **/
    /* grid-column: 1 / span 4; */
    /* grid-row: 6 / span 3; */
  }

  .gallery__item--6 {
    grid-column-start: 5;
    grid-column-end: 9;
    grid-row-start: 6;
    grid-row-end: 9;

    /** Alternative Syntax **/
    /* grid-column: 5 / span 4; */
    /* grid-row: 6 / span 3; */
  }*/
</style>


<div class="container">
  <div class="gallery">
    <a href="./6170979921_a575aec60b_o.jpg" class="gallery__item gallery__item--1">
      <img src="6170979921_a575aec60b_o.jpg" alt="Gallery image 1" class="gallery__img">
    </a>
    <a href="./6170979921_a575aec60b_o.jpg" class="gallery__item gallery__item--2">
        <img src="6170979921_a575aec60b_o.jpg" alt="Gallery image 2" class="gallery__img">
    </a>
    <a href="./6170979921_a575aec60b_o.jpg" class="gallery__item gallery__item--3">
        <img src="6170979921_a575aec60b_o.jpg" alt="Gallery image 3" class="gallery__img">
    </a>
    <a href="./6170979921_a575aec60b_o.jpg" class="gallery__item gallery__item--4">
        <img src="6170979921_a575aec60b_o.jpg" alt="Gallery image 4" class="gallery__img">
    </a>
    <!-- <a href="./6170979921_a575aec60b_o.jpg" class="gallery__item gallery__item--5">
        <img src="6170979921_a575aec60b_o.jpg" alt="Gallery image 5" class="gallery__img">
    </a> -->
    <!-- <a href="./6170979921_a575aec60b_o.jpg" class="gallery__item gallery__item--6">
        <img src="6170979921_a575aec60b_o.jpg" alt="Gallery image 6" class="gallery__img">
</a> -->
  </div>
</div> --> -->