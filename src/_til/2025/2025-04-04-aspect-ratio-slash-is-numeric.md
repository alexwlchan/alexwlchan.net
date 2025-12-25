---
layout: til
title: How do you write ratios in the `aspect-ratio` property?
summary: When you define an aspect ratio as `x/y`, you can only use numbers for `x` and `y`.
date: 2025-04-04 06:57:36 +0100
tags:
  - css
---
I've been using the [`aspect-ratio` CSS property][aspect-ratio], and I often use it with `--width` and `--height` properties that I define based on the dimensions of the image I'm displayed, but I've been a bit confused about when I need to use `calc()` to compute the ratio.

[aspect-ratio]: https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio



## You can define `aspect-ratio` as a ratio of two numbers

I want to be able to define a `--width` and `--height` property, and calculate the aspect ratio in CSS.
For example:

```css
img {
  --width: 1600;
  --height: 900;
  aspect-ratio: var(--width) / var(--height);         /* ✅ */
}
```

This works, because `aspect-ratio` can take a [`<ratio>` data type][ratio], which is two numbers separated by a slash, or a single number with no slash.

Examples are `16/9`, `4/3`, or `1.5`.
And here's the important bit: **you can only have a ratio of two numbers**.

[ratio]: https://developer.mozilla.org/en-US/docs/Web/CSS/ratio



## You can't define `aspect-ratio` as a ratio of two dimensions

Sometimes I write my `--width` and `--height` properties with units, because I'm going to use them with units elsewhere.
Then I'd write something like:

```css
img {
  --width: 1600px;
  --height: 900px;
  aspect-ratio: var(--width) / var(--height);         /* ❌ */
}
```

This doesn't work, because it's a ratio of two dimensions, not two numbers.

Now I write this TIL, I think I probably shouldn't be adding units to these properties -- it makes them more unwieldy to use later.



## You can `calc()` to get a ratio of two dimensions… sometimes

Here's a clever idea I had: what if I pass my ratio to the [`calc()` function][calc] to get a number?

```css
img {
  --width: 1600px;
  --height: 900px;
  aspect-ratio: calc(var(--width) / var(--height));  /* ⚠️ */
}
```

The units cancel out, and I should be left with a nuber.

This works… sometimes.

In Safari 18.2 on my work laptop, this gets me a numeric aspect ratio.
In Safari 18.1 on my home computer, this rule is ignored and I get `aspect-ratio: auto`.
Why are they different?

I looked in the [Safari 18.2 Release Notes][release_notes], and I found this item:

> Updated `calc()` to the most recent web standard, including support for dividing by numbers with additional units. (134446246)

And this is why I've found this whole affair so confusing -- I've been working in browsers that look the same but have subtly different behaviour, so I "learn" what works on one and then that knowledge falls over when I go to the other.

[calc]: https://developer.mozilla.org/en-US/docs/Web/CSS/calc
[release_notes]: https://developer.apple.com/documentation/safari-release-notes/safari-18_2-release-notes



## What I'll do from now on

I'll define my `--width` and `--height` properties as numbers, without dimensions.
When I need to add a dimension, I can [do that with `calc()`](https://stackoverflow.com/a/50019567/1558022):

```css
width: calc(var(--width) * 1px);
```

I'll define my `aspect-ratio` as a ratio of those two numbers, without wrapping it in `calc()` or getting units involved.
