---
layout: post
title: An unexpected lesson in CSS stack contexts
summary: While trying to add some simple overlay labels, I stumbled into a sharp edge of a complex CSS feature called "stack contexts".
tags:
  - css
  - blogging about blogging
---
I made a small tweak to the site this week -- I've added "new" banners to articles I've written recently, and any post marked as "new" will always appear on the homepage.
Previously, the homepage was just a random selection of six articles I've written, from any time.

{%
  picture
  filename="new_banners.png"
  width="600"
%}

Last year I [made some changes][not_all_equal] to de-emphasise sorting by date, and while I stand by that decision, I think I went too far.
Nobody comes to my site asking *"what did Alex write on a specific date"*, but there are people who come to the site asking *"what did Alex write recently"*.
I'd made it more difficult to find my newest writing, and I want to fix that.

This should have been a simple change, but it became a lesson about the inner workings of CSS.

[not_all_equal]: /2024/not-all-posts/

## Absolute positioning and my first attempt

<style>
  @media screen and (min-width: 600px) {
    .worked_example {
      display: grid;
      grid-template-columns: 1fr 200px;
      grid-column-gap: 1.5em;
    }

    .explanation p:first-child {
      margin-top: 0;
    }

    .explanation pre:last-child,
    .explanation figure.highlight:last-child {
      margin-bottom: 0;
    }
  }

  @media screen and (max-width: 600px) {
    .container {
      width: 200px;
      margin: 0 auto;
    }
  }

  #wrapper2 .banner,
  #wrapper3 .banner,
  #wrapper4 .banner,
  #wrapper5 .banner {
    position: absolute;
  }

  #wrapper3.container,
  #wrapper4.container,
  #wrapper5.container {
    position: relative;
  }

  #wrapper3 .banner {
    transform: rotate(45deg);
    right:     16px;
    top:       20px;
  }
</style>

I started with some code I wrote [last year][til].
Let's step through it in detail.

<div class="worked_example">
  <div class="explanation">
    <p>
      First, create a container that includes both the image and the banner.
    </p>
    {% highlight html %}<div class="container">
  <div class="banner">NEW</div>
  <img src="computer.jpg">
</div>{% endhighlight %}
    <p>
      Notice how they appear as two separate elements – they both have separate space in the layout.
      Giving every element its own space is the default behaviour in HTML.
    </p>
  </div>
  <div class="container" id="wrapper1" style="width:200px;">
    <div class="banner">NEW</div>
    <img src="/images/2024/pexels-johndetochka-9140591.jpg" alt="" class="dark_aware">
  </div>

  <div class="explanation">
    <p>
      I can add a CSS rule that makes the text appear on top of the image:
    </p>
    {% highlight css %}.banner {
  position: absolute;
}{% endhighlight %}
    <p>
      This enables <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Positioning#absolute_positioning">absolute positioning</a>, which removes the text from the normal document flow and allows it to be placed anywhee on the page.
      Now it sits alone, and it doesn't affect the layout of other elements on the page – in particular, the image no longer has to leave space for the text.
    </p>
  </div>
  <div class="container" id="wrapper2" style="width:200px;">
    <div class="banner">NEW</div>
    <img src="/images/2024/pexels-johndetochka-9140591.jpg" alt="" class="dark_aware">
  </div>

  <div class="explanation">
    <p>
      Right now the text is in the top left corner of the image, but we can add some more CSS rules to make it appear diagonally in the top right-hand corner:
    </p>
    {% highlight css %}
.container {
  position: relative;
}

.banner {
  transform: rotate(45deg);
  right:     16px;
  top:       20px;
}{% endhighlight %}
  </div>
  <div class="container" id="wrapper3" style="width:200px;">
    <div class="banner">NEW</div>
    <img src="/images/2024/pexels-johndetochka-9140591.jpg" alt="" class="dark_aware">
  </div>
</div>

I chose the `transform`, `right`, and `top` values by tweaking until I got something that looked right.
They move the banner to the right place on the image.

The relative position of the container element is vital.
The absolutely positioned banner still needs a reference point, and it uses the closest ancestor with an explicit <code>position</code> – or if it doesn’t find one, the root <code>&lt;html&gt;</code> element.
Setting `position: relative;` means the `top` and `right` are measured against the sides of the container, not the entire HTML document.

This is a CSS feature called <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Positioning#positioning_contexts">positioning context</a>, which I’d never heard of until I started writing this blog post.
I’d been copying the <code>position: relative;</code> line without really understanding what it did, or why it was necessary.

(What made this particularly confusing to me is that adding `position: absolute` to the banner makes it *seem* like it's positioned inside the image -- until you set <code>top</code> or <code>right</code>, and then it jumps to the edge of the entire page.
This is because an absolutely positioned element takes its initial position from where it would be in the normal flow, and doesn't look for a positioned ancestor until you set an offset.)

<style>
  #wrapper5.container {
    overflow: hidden;
  }

  #wrapper4 .banner,
  #wrapper5 .banner {
    background: red;
    color:      white;

    right:   -34px;
    top:     18px;
    padding: 2px 50px;

    transform: rotate(45deg);
  }
</style>

<div class="worked_example">
  <div class="explanation">
    <p>
      Finally, let's apply a colour to make this banner easier to read – the text is disappearing into the image.
    </p>
    {% highlight css %}.banner {
  background: red;
  color:      white;

  right:   -34px;
  top:     18px;
  padding: 2px 50px;
}{% endhighlight %}
    <p>
      The padding means the banner covers the whole corner, not just the tight rectangle around the word "NEW".
      I had to adjust the position offsets to get the text in the right place.
    </p>
  </div>
  <div class="container" id="wrapper4" style="width:200px;">
    <div class="banner">NEW</div>
    <img src="/images/2024/pexels-johndetochka-9140591.jpg" alt="" class="dark_aware">
  </div>

  <div class="explanation">
    <p>
      Let’s clip the edges off the banner, so it fits within the image:
    </p>
    {% highlight css %}.container {
  overflow: hidden;
}{% endhighlight %}
    <p id="final_para">
      This is the banner effect I’m looking for – the text is clear and prominent on the image.
      I’ve added a <code>box-shadow</code> on my homepage to make it stand out further, but cosmetic details like that aren’t important for the rest of this post.
    </p>
  </div>
  <div class="container" id="wrapper5" style="width:200px;">
    <div class="banner">NEW</div>
    <img src="/images/2024/pexels-johndetochka-9140591.jpg" alt="" class="dark_aware">
  </div>
</div>

<style>
  @media screen and (min-width: 600px) {
    #final_para {
      margin-bottom: 0;
    }
  }
</style>

As a reminder, here's the HTML:

```html
<div class="container">
  <div class="banner">NEW</div>
  <img src="computer.jpg">
</div>
```

Here's the complete CSS:

```css
.container {
  position: relative;
  overflow: hidden;
}

.banner {
  position: absolute;

  background: red;
  color:      white;

  transform: rotate(45deg);

  right:   -34px;
  top:     18px;
  padding: 2px 50px;
}
```

It's only nine CSS rules, but it contains a surprising amount of complexity.
I had this CSS and I knew it worked, but I didn't really understand it -- and especially the way absolute positioning worked -- until I wrote this post.

This worked when I tested it, and then I deployed it on this site, and I found a bug.

(The photo I used in the examples is from [Viktorya Sergeeva on Pexels](https://www.pexels.com/photo/a-person-using-an-old-computer-9140591/).)

[til]: /til/2024/diagonal-new-banner/





## Dark mode, filters, and stacking contexts

I added dark mode support to this site a couple of years ago -- the background changes from white to black, the text colour flips, and a few other changes.
I'm a light mode person, but I know a lot of people prefer dark mode and it was a fun bit of CSS work, so it's there.

The code I described above breaks if you're using this site in dark mode.

What.

I started poking around in my browser's developer tools, and I could see that the banner was being rendered, but it was *under* the image instead of on top of it.
All of my positioning code that worked in light mode was breaking in dark mode.
I was baffled.

<style>
  #dark_mode_wtf {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 5px;
  }
</style>

<figure style="width: calc(620px)">
  <div id="dark_mode_wtf">
    {%
      picture
      filename="dark_mode_wtf1.png"
      width="200"
      class="screenshot dark_aware"
      style="border-top-right-radius: 0; border-bottom-right-radius: 0;"
    %}
    {%
      picture
      filename="dark_mode_wtf2.png"
      width="200"
      class="screenshot dark_aware"
      style="border-radius: 0;"
    %}
    {%
      picture
      filename="dark_mode_wtf3.png"
      width="200"
      class="screenshot dark_aware"
      style="border-top-left-radius: 0; border-bottom-left-radius: 0;"
    %}
  </div>
  <figcaption>
    The same component in light mode, dark mode, and using the web inspector to highlight the banner in dark mode.
    Like a goth ninja in a cave at midnight, you can't see the banner.
  </figcaption>
</figure>

I discovered that by adding a [`z-index`][z_index] to the banner, I could make it appear again.
My vague understanding was that `z-index` affects the layering of images on the page, and elements with a higher `z-index` will appear above an element with a lower `z-index`.
So I had a fix, but it felt hacky because I didn't understand why it worked.
I wanted to go deeper.

I had no idea what would cause this behaviour, but I knew it was an issue with my CSS.
I could see the issue if I tried my code in this site, but not if I copied it to a standalone HTML file.
(Before you keep reading, you might ask yourself whether you know what's causing this issue.
If you do, congratulations, you know CSS better than I do!)

To find the issue, I created a local branch of the site, and I started deleting CSS until I could no longer reproduce the issue.
I eventually tracked it down to the following rule:

```css
@media (prefers-color-scheme: dark) {
  /* see https://web.dev/articles/prefers-color-scheme#re-colorize_and_darken_photographic_images */
  img:not([src*='.svg']):not(.dark_aware) {
    filter: grayscale(10%);
  }
}
```

This rule will apply a slight darkening to any images when dark mode is enabled -- unless they're an SVG, or I've added the `dark_aware` class that means an image look okay in dark mode.
This is a suggestion from Thomas Steiner, from [an article][steiner] with a lot of useful advice about supporting dark mode.
When this rule is present, the banner vanishes.
When I delete it, the banner looks fine.

**Eventually I found the answer: I'd misunderstood a web feature called the [stacking context]**.
This is a way of thinking about HTML elements in three dimensions, where there's a z-axis that affects which elements appear above or below each other.
There are a number of rules that affect where elements appear in the stacking context -- `z-index` is one (which seems obvious), and `filter` is another (which is less obvious).

In light mode, the banner and the image are both part of the same stacking context.
This means that both elements can be rendered together, and the positioning rules are applied together -- so the banner appears on top of the image.

**In dark mode, my `filter` rule creates a new stacking context.**
A `filter` property is one of several things that can create a new stacking context, and it means the image and the banner will be rendered separately.
Browsers render elements in DOM order, and because the banner appears before the image in the HTML, the banner is rendered first, then the image is rendered separately and covers it up.

The correct fix is not to set a `z-index`, but swap the order of DOM elements so the banner is rendered after the image:

```html
<div class="container">
  <img src="computer.jpg">
  <div class="banner">NEW</div>
</div>
```

This is the code I'm using now, and now the banner looks correct in dark mode.

[steiner]: https://web.dev/articles/prefers-color-scheme#re-colorize-and-darken-photographic-images
[z_index]: https://developer.mozilla.org/en-US/docs/Web/CSS/z-index
[stacking context]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Stacking_context

---

A lot of CSS feels like "try it until it works"
