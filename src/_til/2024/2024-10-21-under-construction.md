---
layout: til
title: Making an "under construction" element in pure CSS
summary: |
  Using a `repeating-linear-gradient` as the `border` gets you something that looks a bit like hazard tape.
date: 2024-10-21 16:38:57 +01:00
tags:
  - css
colors:
  css_light: "#806c00"
  css_dark:  "#ffd700"
---
I was building a prototype app today, and I wanted a way to add "notes" to the design -- a way to tell people I knew something was broken or unfinished, and give some idea of what it would look like in the final version.

I thought it'd be neat to add notes that look like the ’90s "under construction" GIFs, so I set out to recreate that effect in CSS.

This is what I came up with:

```css
.under_construction {
  --yellow:       255, 215, 0;  /* CSS gold */

  background: rgba(var(--yellow), 0.2);

  border-left-width: 10px;
  border-left-style: solid;
  border-image: repeating-linear-gradient(
    45deg,
    black,
    black              5px,
    rgb(var(--yellow)) 5px,
    rgb(var(--yellow)) 10px
  ) 10;
}
```

<style>
  .under_construction {
    --yellow:       255, 215, 0;

    background: rgba(var(--yellow), 0.2);

    border: none;

    border-left-width: 10px;
    border-left-style: solid;
    border-image: repeating-linear-gradient(
      45deg,
      black,
      black              5px,
      rgb(var(--yellow)) 5px,
      rgb(var(--yellow)) 10px
    ) 10;
  }
</style>

Here's what it looks like:

<blockquote class="under_construction">
  <p>
    This widget won’t work until we reverse the polarity of the neutron flow.
  </p>
</blockquote>

I don't really understand the relationsip between the `border-width` and the values in `repeating-linear-gradient` -- although I've created a couple of striped patterns like this, I'm still experimenting each time.
I just tweak the values until they look right.

It feels like there's a lot of powerful stuff I can do with that function, if I sit down and take the time to learn it properly.

I couldn't work out how to add rounded corners to the hazard tape -- it seems like `border-radius` and `border-image` don't play nicely together. 🤷‍♀️
