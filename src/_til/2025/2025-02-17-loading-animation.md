---
layout: til
title: Create an animated placeholder box with CSS
date: 2025-02-17 18:34:04 -05:00
tags:
  - css
---
I wanted to create an animated placeholder box with CSS -- that is, a box with a pulsating animation that indicates something should be filled in here later.

I worked out how to do this: create a gradient background that's larger than the element, then use `@keyframes` to animate the background moving.

Here's a minimal example:

```html
<style>
  /* This gives an animated "loading" bar we can use before text loads in */
  .loading {
    --light-grey: #ccc;
    --dark-grey:  #999;

    background: repeating-linear-gradient(
      to right,
      var(--light-grey) 0%,
      var(--dark-grey) 50%,
      var(--light-grey) 100%
    );
    background-size: 200% auto;
    background-position: 0 100%;
    animation: loading 2s infinite;
    animation-fill-mode: forwards;
    animation-timing-function: linear;
  }

  @keyframes loading {
    0%   { background-position: 0 0; }
    100% { background-position: -200% 0; }
  }
</style>

<div class="loading" style="width: 300px; height: 100px;"></div>
```

and this is what it looks like:

<style>
  /* This gives an animated "loading" bar we can use before text loads in */
  .loading {
    --light-grey: #ccc;
    --dark-grey:  #999;

    background: repeating-linear-gradient(
      to right,
      var(--light-grey) 0%,
      var(--dark-grey) 50%,
      var(--light-grey) 100%
    );
    background-size: 200% auto;
    background-position: 0 100%;
    animation: loading 2s infinite;
    animation-fill-mode: forwards;
    animation-timing-function: linear;
  }

  @keyframes loading {
    0%   { background-position: 0 0; }
    100% { background-position: -200% 0; }
  }
</style>

<div class="loading" style="width: 300px; height: 100px;"></div>
