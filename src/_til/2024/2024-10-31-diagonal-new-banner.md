---
layout: til
title: Drawing a diagonal banner over the corner of an image
date: 2024-10-31 15:26:21 +00:00
tags:
  - css
---
I wanted to draw a diagonal banner over the corner of an image, to show the word "new".
I've seen this in other places (like Apple's online store) but I hadn't made my own version of this effect.

<div class="wrapper" style="margin-left: auto; margin-right: auto;">
  <div class="banner">NEW</div>
  <img src="/images/2024/pexels-johndetochka-9140591.jpg" alt="An old computer, which is definitely not ‘new’ in any sense.">
</div>

<style>
  .wrapper {
    width: 300px;

    position: relative;
    overflow: hidden;
  }

  .banner {
    position: absolute;

    transform: rotate(45deg);

    right:   -52px;
    top:      22px;
    padding: 10px 60px;

    font-size: 2em;

    background: var(--primary-color-light);
    color:      white;

    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }
</style>

The trick is to create a wrapper element that contains both the image and the banner, with `overflow: hidden` that hides the banner when it reaches the edge.
Then you use an inner banner element with `absolute` positioning.

Here's the code:

```html
<div class="wrapper">
  <div class="banner">NEW</div>
  <img src="computer.jpg">
</div>
```

```css
.wrapper {
  position: relative;
  overflow: hidden;
}

.banner {
  position: absolute;

  transform: rotate(45deg);

  right:   -35px;
  top:      22px;
  padding: 2px 50px;

  background: red;
  color:      white;

  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}
```

I don't fully understand the margin/padding values yet, and I get what I want by tweaking them until I get something that looks right.

If you want the banner to exceed beyond the bounds of the image, you can add some padding to the wrapper element.
Here's what that looks like:

<div class="wrapper_outer" style="margin-left: auto; margin-right: auto;">
  <div class="banner">NEW</div>
  <img src="/images/2024/pexels-johndetochka-9140591.jpg" alt="An old computer, which is definitely not ‘new’ in any sense.">
</div>

<style>
  .wrapper_outer {
    padding: 5px;
    width: 310px;

    position: relative;
    overflow: hidden;
  }
</style>

And here's the updated CSS:

```css
.wrapper {
  padding: 5px;

  position: relative;
  overflow: hidden;
}
```