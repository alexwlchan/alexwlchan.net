---
layout: post
date: 2026-01-14 08:38:52 +00:00
title: The Good, the Bad, and the Gutters
summary: A step-by-step guide to a movie poster grid that uses CSS Grid, text-wrap balanced titles, and dynamic hover states.
tags:
  - css
index:
  feature: true
colors:
  css_light: "#911e31"
  css_dark:  "#d64f71"
---
I've been organising my local movie collection recently, and converting it into [a static site][static-sites].
I want the homepage to be a scrolling grid of movie posters, where I can click on any poster and start watching the movie.
Here's a screenshot of the design:

<!--
  npx playwright screenshot -b webkit --viewport-size '1520,830' file:///Users/alexwlchan/repos/alexwlchan.net/src/_files/2026/movie-poster-css/demo7-final.html /Users/alexwlchan/repos/alexwlchan.net/src/_images/2026/movie-poster-hero.png
-->

{%
  picture
  filename="movie-poster-hero.png"
  width="750"
  alt="A grid of portrait-sized posters for made-up movies. There are two rows of six posters, and each poster is the same height. The posters line up horiozntally, and below each poster is the title of the movie."
  class="screenshot dark_aware"
  link_to="original"
%}

This scrolling grid of posters is something I'd like to reuse for other media collections -- books, comics, and TV shows.

I wrote an initial implementation with [CSS grid layout][mdn-css-grid], but over time I found rough edges and bugs.
I kept adding rules and properties to "fix" the layout, but these piecemeal changes introduced new bugs and conflicts, and eventually I no longer understood the page as a whole.
This gradual degradation often happens when I write CSS, and when I no longer understand how the page works, it's time to reset and start again.

To help me understand how this layout works, I'm going to step through it and explain how I built the new version of the page.

{% table_of_contents %}

## Step 1: Write the unstyled HTML

This is a list of movies, so I use an [unordered list `<ul>`][mdn-ul].
Each list item is pretty basic, with just an image and a title.
I wrap them both in a [`<figure>` element][mdn-figure] -- I don't think that's strictly necessary, but it feels semantically correct to group the image and title together. 

```html
<ul id="movies">
  <li>
    <a href="#">
      <figure>
        <img src="apollo-13px.png">
        <figcaption>Apollo 13px</figcaption>
      </figure>
    </a>
  </li>
  <li>
    <a href="#">
      <figure>
        <img src="breakpoint-at-tiffanys.png">
        <figcaption>Breakpoint at Tiffany’s</figcaption>
      </figure>
    </a>
  </li>
  ...
</ul>
```

I did wonder if this should be an [ordered list][mdn-ol], because the list is ordered alphabetically, but I decided against it because the numbering isn't important.

Having a particular item be #1 is meaningful in a ranked list (the 100 best movies) or a sequence of steps (a cooking recipe), but there's less significance to #1 in an alphabetical list.
If I get a new movie that goes at the top of the list, it doesn't matter that the previous #1 has moved to #2.

This is an unstyled HTML page, so it looks pretty rough:

<!-- npx playwright screenshot -b webkit --viewport-size '1520,920' file:///Users/alexwlchan/repos/alexwlchan.net/src/_files/2026/movie-poster-css/demo1-markup.html /Users/alexwlchan/repos/alexwlchan.net/src/_images/2026/mp-css-demo1-markup.png -->

{%
  picture
  filename="mp-css-demo1-markup.png"
  width="750"
  class="screenshot dark_aware"
  link_to="/files/2026/movie-poster-css/demo1-markup.html"
  alt="A web page which is mostly dominated by a poster for ‘Apollo 13px’, with a bullet point vaguely visible on the left. The title of the movie is visible in small blue, underlined text below the image. The spacing looks weird."
%}

## Step 2: Add a CSS grid layout

Next, let's get the items arranged in a grid.
This is a textbook use case for [CSS grid layout][mdn-css-grid].

I start by resetting some default styles: removing the bullet point and whitespace from the list, and the whitespace around the figure.

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {
  list-style-type: none;
  padding: 0;
  margin:  0;
  
  figure {
    margin: 0;
  }
}
{% endcode %}

Then I create a grid that creates columns which are 200px wide, as many columns as will fit on the screen.
The column width was an arbitrary choice and caused some layout issues -- I'll explain how to choose this properly in the next step.

```css
#movies {
  display: grid;
  grid-template-columns: repeat(auto-fill, 200px);
  column-gap: 1em;
  row-gap:    2em;
}
```

By default, browsers show images at their original size, which means they overlap each other.
For now, clamp the width of the images to the columns, so they don't overlap:

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {
  img {
    width: 100%;
  }
}
{% endcode %}

With these styles, the grid fills up from the left and stops as soon as it runs out of room for a full 200px column.
It looks a bit like an unfinished game of Tetris -- there's an awkward gap on the right-hand side of the window that makes the page feel off-balance.

<!-- $ npx playwright screenshot -b webkit --viewport-size '1520,750' file:///Users/alexwlchan/repos/alexwlchan.net/src/_files/2026/movie-poster-css/demo2-grid-no-space-evenly.html /Users/alexwlchan/repos/alexwlchan.net/src/_images/2026/mp-css-demo2-grid-no-space-evenly.png -->

{%
  picture
  filename="mp-css-demo2-grid-no-space-evenly.png"
  width="750"
  class="screenshot dark_aware"
  link_to="/files/2026/movie-poster-css/demo2-grid-no-space-evenly.html"
  alt="A grid of movie posters on a white background, two rows of six posters. All the posters are pushed to the left of the screen, with a big white gap on the right-hand side."
%}

We can space the columns more evenly by adding a [`justify-content` property][mdn-justify-content] which tells the browser to create equal spacing between each of them, including on the left and right-hand side:

```css
#movies {
  justify-content: space-evenly;
}
```

With just ten CSS properties, the page looks a lot closer to the desired result:

<!-- npx playwright screenshot -b webkit --viewport-size '1520,750' file:///Users/alexwlchan/repos/alexwlchan.net/src/_files/2026/movie-poster-css/demo2-grid.html /Users/alexwlchan/repos/alexwlchan.net/src/_images/2026/mp-css-demo2-grid.png -->

{%
  picture
  filename="mp-css-demo2-grid.png"
  width="750"
  class="screenshot dark_aware"
  link_to="/files/2026/movie-poster-css/demo2-grid.html"
  alt="A grid of movie posters on a white background, two rows of six posters. Below each poster is a blue link with the title of the movie. Every poster is the same width, but some are different heights."
%}

After this step, what stands out here is the inconsistent heights, especially the text beneath the posters.
The mismatched height of *The Empire Strikes Block* is obvious, but the posters for *The Devil Wears Padding* and *vh for Vendetta* are also slightly shorter than their neighbours.
Let's fix that next.

## Step 3: Choosing the correct column size

Although movie posters are always portrait orientation, the aspect ratio can vary.
Because my first grid fixes the width, some posters will be a different height to others.

I prefer to have the posters be fixed height and allow varied widths, so all the text is on the same level.
Let's replace the width rule on images:

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {
  img {
    height: 300px;
  }
}
{% endcode %}

This causes an issue with my columns, because now some of the posters are wider than 200px, and overflow into their neighbour.
I need to pick a column size which is wide enough to allow all of my posters at this fixed height.
I can calculate the displayed width of a single poster:

<math display="block">
  <mtext>display width</mtext>
  <mo>=</mo>
  <mi>300px</mi>
  <mo>×</mo>
  <mfrac>
    <mtext>poster width</mtext>
    <mtext>poster height</mtext>
  </mfrac>
</math>

Then I pick the largest display width in my collection, so even the widest poster has enough room to breathe without overlapping its neighbour.

In my case, the largest poster is 225px wide when it's shown at 300px tall, so I change my column rule to match:

```css
#movies {
  grid-template-columns: repeat(auto-fill, 225px);
}
```

If I ever change the height of the posters or get a wider poster, I'll need to adjust this widths.
If I was adding movies too fast for that to be sustainable, I'd look at using something like [`object-fit: cover`][mdn-object-fit-cover] to clip anything that was extra wide.
I've skipped that here because I don't need it, and I like seeing the whole poster.

If you have big columns or small devices, you need some extra CSS to make columns and images shrink when they're wider than the device, but I can ignore that here.
A 225px column is narrower than my iPhone, which is the smallest device I'll use this for.
(I did try writing that CSS, and I quickly got stuck.
I'll come back to it if it's ever an issue, but I don't need it today.)

Now the posters which are narrower than the column are flush left with the edge of the column, whereas I'd really like them to be centred inside the column.
I cam fix this with one more rule:

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {
  li {
    text-align: center;
  }
}
{% endcode %}

This is a more subtle transformation from the previous step -- nothing's radically different, but all the posters line up neatly in a way they didn't before.

<!-- npx playwright screenshot -b webkit --viewport-size '1520,750' file:///Users/alexwlchan/repos/alexwlchan.net/src/_files/2026/movie-poster-css/demo3-geometry.html /Users/alexwlchan/repos/alexwlchan.net/src/_images/2026/mp-css-demo3-geometry.png -->

{%
  picture
  filename="mp-css-demo3-geometry.png"
  width="750"
  class="screenshot dark_aware"
  link_to="/files/2026/movie-poster-css/demo3-geometry.html"
  alt="A grid of movie posters on a white background, but now each poster is the same height and the text under each poster is centre-aligned."
%}

Swapping fixed width for fixed height means there's now an inconsistent amount of horizontal space between posters -- but I find that less noticeable.
You can't get a fixed space in both directions unless all your posters have the same aspect ratio, which would mean clipping or stretching.
I'd rather have the slightly inconsistent gaps.

The white background and blue underlined text are still giving "unstyled HTML page" vibes, so let's tidy up the colours.

## Step 4: Invert the colours with a dark background

The next set of rules change the page to white text on a dark background.
I use a dark grey, so I can distinguish the posters which often use black:

<!-- lang="nested_css" -->
{% code lang="css" %}
body {
  background: #222;
  font-family: -apple-system, sans-serif;
}

#movies {
  a {
    color: white;
    text-decoration: none;
  }
}
{% endcode %}

Let's also make the text bigger, and add a bit of spacing between it and the image.
And when the title and image are more spaced apart, let's increase the row spacing even more, so it's always clear which title goes with which poster:

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {
  grid-row-gap: 3em;
  
  figcaption {
    font-size:  1.5em;
    margin-top: 0.4em;
  }
}
{% endcode %}

The movie title is a good opportunity to use [`text-wrap: balance`][mdn-text-wrap].
This tells the browser to balance the length of each line, which can make the text look a bit nicer.
You'll get several lines of roughly the same length, rather than one or more long lines and a short line.
For example, it changes *"The Empire Strikes // Block"* to the more balanced *"The Empire // Strikes Block"*.

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {  
  figcaption {
    text-wrap: balance;
  }
}
{% endcode %}

Here's what the page looks like now, which is pretty close to the final result:

<!-- npx playwright screenshot -b webkit --viewport-size '1520,830' file:///Users/alexwlchan/repos/alexwlchan.net/src/_files/2026/movie-poster-css/demo4-cosmetic.html /Users/alexwlchan/repos/alexwlchan.net/src/_images/2026/mp-css-demo4-cosmetic.png -->

{%
  picture
  filename="mp-css-demo4-cosmetic.png"
  width="750"
  class="screenshot dark_aware"
  link_to="/files/2026/movie-poster-css/demo4-cosmetic.html"
  alt="A grid of movie posters on a dark grey background, and now the text under each poster is larger and white."
%}

What's left is a couple of dynamic elements -- hover states for individual posters, and placeholders while images are loading.

## Step 5: Add a border/underline on hover

As I'm mousing around the grid, I like to add a hover style that shows me which movie is currently selected -- [a coloured border][hover-border] around the poster, and a text underline on the title.

First, I use my [dominant_colours tool][dominant_colours] to get a suitable tint colour for use with this background:

<style>
  #dominant_colours_example .go {
    background: #222;
    color: #ecd3ab;
  }
</style>

<!-- console?prompt=$ -->

<div id="dominant_colours_example">
{% code lang="console" %}
$ dominant_colours gridiator.png --best-against-bg '#222'
▇ #ecd3ab
{% endcode %}
</div>

Then I add this to my markup as a CSS variable:

```html
<ul id="movies">
  ...
  <li style="--tint-colour: #ecd3ab">
    <a href="#">
      <figure>
        <img src="gridiator.png">
        <figcaption>Gridiator</figcaption>
      </figure>
    </a>
  </li>
  ...
</ul>
```

Finally, I can add some hover styles that use this new variable:

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {
  a:hover {
    figcaption {
      text-decoration-line: underline;
      text-decoration-thickness: 3px;
    }
  
    img {
      outline: 3px solid var(--tint-colour);
    }
  }
}
{% endcode %}

I've added the `text-decoration` styles directly on the `figcaption` rather than the `a`, because browsers are inconsistent about whether those properties are inherited from parent elements.

I used `outline` instead of `border` so the 3px width doesn't move the image when the style is applied.

Here's what the page looks like when I hover over *Breakpoint at Tiffany's*:

<!--
  npx playwright screenshot -b webkit --viewport-size '1520,830' file:///Users/alexwlchan/repos/alexwlchan.net/src/_files/2026/movie-poster-css/demo5-hover-styles.html /Users/alexwlchan/repos/alexwlchan.net/src/_images/2026/mp-css-demo5-hover-styles.png
-->

{%
  picture
  filename="mp-css-demo5-hover-styles.png"
  width="750"
  class="screenshot dark_aware"
  link_to="/files/2026/movie-poster-css/demo5-hover-styles.html"
  alt="A grid of movie posters on a dark grey background, and one of the posters has a pink outline and the title is underlined."
%}

We're almost there!

## Step 6: Add placeholder colours

As my movie collection grows, I want to [lazy load][mdn-lazy-loading] my images so I don't try to load them all immediately, especially posters that aren't scrolled into view.
But then if I scroll and I'm on a slow connection, it can take a few seconds for the image to load, and until then the page has a hole.
I like having solid colour placeholders which get replaced by the image when it loads.

First I have to insert a wrapper `<div>` which I'm going to colour, and a CSS variable with the aspect ratio of the poster so I can size it correctly:

```html
<ul id="movies">
  ...
  <li style="--tint-colour: #ecd3ab; --aspect-ratio: 510 / 768">
    <a href="#">
      <figure>
        <div class="wrapper">
          <img src="gridiator.png" loading="lazy">
        </div>
        <figcaption>Gridiator</figcaption>
      </figure>
    </a>
  </li>
  ...
</ul>
```

We can add a coloured background to this wrapper and make it the right size:

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {
  img, .wrapper {
    height: 300px;
    aspect-ratio: var(--aspect-ratio);
  }
  
  .wrapper {
    background: var(--tint-colour);
  }
}
{% endcode %}

But a `<div>` is a `block` element by default, so it isn't centred properly -- it sticks to the left-hand side of the column, and doesn't line up with the text.
We could add `margin: 0 auto;` to move it to the middle, but that duplicates the `text-align: center;` property we wrote earlier.
Instead, I prefer to make the wrapper an `inline-block`, so it follows the existing text alignment rule:

<!-- lang="nested_css" -->
{% code lang="css" %}
#movies {
  .wrapper {
    display: inline-block;
  }
}
{% endcode %}

Here's what the page looks like when some of the images have yet to load:

<!--
npx playwright screenshot -b webkit --viewport-size '1520,830' file:///Users/alexwlchan/repos/alexwlchan.net/src/_files/2026/movie-poster-css/demo6-placeholders.html /Users/alexwlchan/repos/alexwlchan.net/src/_images/2026/mp-css-demo6-placeholders.png
-->

{%
  picture
  filename="mp-css-demo6-placeholders.png"
  width="750"
  class="screenshot dark_aware"
  link_to="/files/2026/movie-poster-css/demo6-placeholders.html"
  alt="A grid of movie posters on a dark grey background, where three of the posters are solid colour rectangles where the images haven’t yet loaded."
%}

And we're done!

## The final page

There's a [demo page][demo] where you can try this design and see how it works in practice.

Here's what the HTML markup looks like:

```html
<ul id="movies">
  <li style="--tint-colour: #dbdfde; --aspect-ratio: 510 / 768">
    <a href="#">
      <figure>
        <div class="wrapper">
          <img src="apollo-13px.png" loading="lazy">
        </div>
        <figcaption>Apollo 13px</figcaption>
      </figure>
    </a>
  </li>
  ...
</ul>
```

and here's the complete CSS:

<!-- lang="nested_css" -->
{% code lang="css" %}
body {
  background: #222;
  font-family: -apple-system, sans-serif;
}

#movies {
  list-style-type: none;
  padding: 0;
  margin:  0;
  
  display: grid;
  grid-template-columns: repeat(auto-fill, 225px);
  column-gap: 1em;
  row-gap:    3em;

  justify-content: space-evenly;

  figure {
    margin: 0;
  }
  
  li {
    text-align: center;
  }
  
  a {
    color: white;
    text-decoration: none;
  }
  
  figcaption {
    font-size:  1.5em;
    margin-top: 0.4em;
    text-wrap: balance;
  }
  
  a:hover, a#tiffanys {
    figcaption {
      text-decoration-line: underline;
      text-decoration-thickness: 3px;
    }
    
    img {
      outline: 3px solid var(--tint-colour);
    }
  }
  
  img, .wrapper {
    height: 300px;
    aspect-ratio: var(--aspect-ratio);
  }

  .wrapper {
    background: var(--tint-colour);
    display: inline-block;
  }
}
{% endcode %}

I'm really happy with the result -- not just the final page, but how well I understand it.
CSS can be tricky to reason about, and writing this step-by-step guide has solidified my mental model.

I learnt a few new details while checking references, like the `outline` property for hover states, the way `text-decoration` isn't meant to inherit, and the fact that `column-gap` and `row-gap` have replaced the older `grid-` prefixed versions.

This layout is working well enough for now, but more importantly, I'm confident I could tweak it if I want to make changes later.

[demo]: /files/2026/movie-poster-css/demo7-final.html
[dominant_colours]: /2021/dominant-colours/
[hover-border]: /2024/hover-states/
[mdn-css-grid]: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
[mdn-figure]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/figure
[mdn-justify-content]: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/justify-content
[mdn-lazy-loading]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img#loading
[mdn-object-fit-cover]: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/object-fit#cover
[mdn-ol]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/ol
[mdn-text-wrap]: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap
[mdn-ul]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/ul
[static-sites]: /2024/static-websites/

