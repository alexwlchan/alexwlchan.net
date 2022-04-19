---
layout: post
title: Creating a “simple” three-up image layout in CSS
summary:
tags: css
---

Recently I was working on a new web component: a three-up layout of images, with one on the left and two on the right.
I was looking for something a bit more visually interesting than a scrolling vertical list.
This is the sort of thing I mean:

<img src="/images/2022/image_layout.png" style="width: 344px;">

If you've done a lot of front-end web development, this sort of layout probably seems quite simple -- many websites have far more complex layouts.
You might already know how you'd do it.
But I don't do much front-end work, and it took quite a bit of frustration and head-banging to get this working -- so let's walk through it together.



## Step 1: Get on the grid

Although I do much front-end development, I am vaguely aware of [CSS Grid].
I know it's the "new" approach to doing complex layouts, and I've dabbled with it for a few projects.
(I put "new" in air quotes because it's been a thing for many years, but I'm only just starting to understand it.)

Here's a simple three-cell grid using divs:

```html
<div class="grid">
  <div class="left_image">left grid item</div>
  <div class="right_upper_image">right upper grid item</div>
  <div class="right_lower_image">right lower grid item</div>
</div>
```

and the CSS that matches it:

```css
.grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
  grid-gap: 5px;
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

The `display: grid;` property switches us into grid mode, and the `-template-columns` and `-template-rows` properties tell the grid how tall/wide the columns and rows should be.

The unit here is `fr`, which is the [fraction of flexible space][fr].
You can define fixed sizes for rows and columns, and then divide up the remaining space proportionally -- or as I'm doing here, you can divide up all the space proportionally.
I want two columns and two rows, where the first column is twice as wide as the second, and the rows are equal height.

The `grid-row` and `grid-column` properties on individual items tell them where to sit in the grid.
For the item on the left-hand side, the `1 / span 2` value tells it to start in row 1 and fill 2 rows.

This is what it looks like.
I've added some background colours so the different items stand out:

<div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; grid-gap: 10px; width: 300px; margin-left: auto; margin-right: auto;">
  <div style="grid-column: 1 / 2; grid-row: 1 / span 2; background: #00A1ff; color: white;">
    left grid item
  </div>

  <div style="grid-column: 2 / 2; grid-row: 1 / 2; background: #ed220d; color: white;">
    right upper grid item
  </div>

  <div style="grid-column: 2 / 2; grid-row: 2 / 2; background: #60d937; color: white;">
    right lower grid item
  </div>
</div>

This looks a bit like what I want!




## Step 2: Adding images to the grid

Let's drop some images into the grid in place of the text:

```html
<div class="grid">
  <div class="left_image">
    <img src="/sky.jpg">
  </div>
  <div class="right_upper_image">
    <img src="/jupiter.jpg">
  </div>
  <div class="right_lower_image">
    <img src="/iss.jpg">
  </div>
</div>
```

This is what that looks like -- the images are in the right place, but they don't fit properly.
Because the aspect ratios of the images are all different and the browser tries to display the entire image, there's a lot of empty space around them -- I want their edges to line up.

<div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; grid-gap: 10px; width: 576px; margin-left: auto; margin-right: auto;">
  <div style="grid-column: 1 / 2; grid-row: 1 / span 2; background: #00A1ff; color: white;">
    <img src="/images/2022/sky_thumb.jpg" style="max-width: none;">
  </div>

  <div style="grid-column: 2 / 2; grid-row: 1 / 2; background: #ed220d; color: white;">
    <img src="/images/2022/jupiter_thumb.jpg" style="max-width: none;">
  </div>

  <div style="grid-column: 2 / 2; grid-row: 2 / 2; background: #60d937; color: white;">
    <img src="/images/2022/iss_thumb.jpg" style="max-width: none;">
  </div>
</div>

Notice that the two right-hand images are the same height -- this is CSS Grid giving me two equal-height rows.

(These are images of [the Earth's sky][sky], [Jupiter and Io][jupiter], and the [International Space Station (ISS)][iss], all published by NASA.
The trail of light in the sky is the ISS captured in a thirteen-second exposure, and the bright light next to it is Jupiter.)

[CSS Grid]: https://en.wikipedia.org/wiki/CSS_grid_layout
[fr]: https://www.w3.org/TR/css-grid-1/#fr-unit
[sky]: https://solarsystem.nasa.gov/resources/2500/the-view-from-earth-space-station-jupiter-milky-way/
[jupiter]: https://solarsystem.nasa.gov/resources/803/jupiter-and-io/?category=planets_jupiter
[iss]: https://www.nasa.gov/image-feature/the-station-pictured-from-the-spacex-crew-dragon-6



## Step 3: Set the width and height of the images

By setting the `width` and `height` properties on the images, we can expand the images to fill the empty space.

```css
.grid img {
  width: 100%;
  height: 100%;
}
```

<div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; grid-gap: 10px; width: 400px; margin-left: auto; margin-right: auto;">
  <div style="grid-column: 1 / 2; grid-row: 1 / span 2;">
    <img src="/images/2022/sky_thumb.jpg" style="max-width: none; width: 100%; height: 100%;">
  </div>

  <div style="grid-column: 2 / 2; grid-row: 1 / 2;">
    <img src="/images/2022/jupiter_thumb.jpg" style="max-width: none; width: 100%; height: 100%;">
  </div>

  <div style="grid-column: 2 / 2; grid-row: 2 / 2;">
    <img src="/images/2022/iss_thumb.jpg" style="max-width: none; width: 100%; height: 100%;">
  </div>
</div>

This gets us flush edges, but now the images are horribly distorted -- they've been stretched to fill the container.
If I was making this layout in a graphics editor, I'd expand the images while maintaining the aspect ratio, then crop them to fit.
Can we achieve that with CSS?



## Step 4: Add the object-fit property

To unbreak the aspect ratio, I discovered a new-to-me CSS property: [object-fit].
This defines how an element (say, an image or video) should be resized to fit into a container.

The default value is `object-fit: fill`, which expands the element to completely fill the container, and stretches the object to fit.
That's causing the distorted aspect ratio in the example above.

After experimenting with the other values (I had to try it myself to really understand how they worked), I think the value I want is `object-fit: cover`.
This expands an element while maintaining its aspect ratio, and if it doesn't fit perfectly then extra bits get clipped out -- the edges of the image get cropped.

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

[object-fit]: https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit



?category=planets_jupiter



<ol>

  <li>
    Super squished, add the cover:

    <div style="max-width: 800px;">

      <div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; grid-gap: 10px; border: 4px solid blue;">
        <div style="grid-column: 1 / 2; grid-row: 1 / span 2; background: red;">
          <img src="./6185949404_3e247d2ec1_o.jpg" style="width: 100%; height: 100%; object-fit: contain;">
        </div>

        <div style="grid-column: 2 / 2; grid-row: 1 / 2; background: green;">
          <img src="./6185949404_3e247d2ec1_o.jpg" style="width: 100%; height: 100%; object-fit: contain;">
        </div>

        <div style="grid-column: 2 / 2; grid-row: 2 / 2; background: blue;">
          <img src="./6185949404_3e247d2ec1_o.jpg" style="width: 100%; height: 100%; object-fit: contain;">
        </div>
      </div>

    </div>

    <div style="max-width: 800px;">

      <div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: 1fr 1fr; grid-gap: 10px; border: 4px solid blue;">
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

  </li>

  <li>
    Now add an aspect ratio

    <div style="width: 100%; padding-top: 33%; position:relative; max-width: 800px;">

      <div style="display: grid; grid-template-columns: 2fr 1fr; grid-template-rows: calc(50% - 5px) calc(50% - 5px); grid-gap: 10px; position: absolute; top:0;left:0;bottom:0;right:0; height: 100%;">
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