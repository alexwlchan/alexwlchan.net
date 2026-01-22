---
layout: post
date: 2024-01-07 21:11:31 +00:00
title: The best way to tell a website your age
summary: Using SVG animations to create a fun and exciting new input UI.
tags:
  - code crimes
  - drawing things
  - svg
index:
  exclude: true
---
There's a growing number of countries creating laws that require age verification laws to access certain content online.
Now children can be protected from adult content like well-organised spreadsheets, YouTube videos about kitchen appliances, and websites that sell you socks.
These laws are a brilliant idea that will definitely fix everything.

However, there is one point of contention: how should websites ask for your age?

I've done some thinking, and I've come up with a proposal.
We all know the best way to tell somebody's age is to count the candles on their birthday cake, so I've built a cake-based interface.

<style type="x-text/scss">
  #cakeInput {
    --width: calc(
      100vw
      - 3 * var(--default-padding)
      - env(safe-area-inset-left)
      - env(safe-area-inset-right)
      - 2 * var(--border-width)
    );

    /* Imagine we want a layout like this, where W is the full width of
     * the window, T is the text, and C is the cake.
     *
     *      WWWWWWWWWWWW|WWWWWWWWWWWW
     *          TTTTTTTT|TTTTTTTT
     *       CCCCCCCCCCC|CCCCCCCCCCC
     *
     * By default, the cake will be aligned flush left with the text:
     *
     *      WWWWWWWWWWWW|WWWWWWWWWWWW
     *          TTTTTTTT|TTTTTTTT
     *          CCCCCCCCCCC|CCCCCCCCCCC
     *
     * But we want it pushing against the left-hand side of the window.
     * Then we work out the margin we need to push it left by by taking
     * the difference of half the width of the cake, and half the width
     * of the text.
     *
     *      WWWWWWWWWWWW|WWWWWWWWWWWW
     *          TTTTTTTT|TTTTTTTT
     *          ^^^^^^^^
     *           = 50%
     *
     *       CCCCCCCCCCC|CCCCCCCCCCC
     *       ^^^^^^^^^^^
     *        = width / 2
     *
     */

    width: var(--width);
    margin-left:  calc(-1 * (var(--width) / 2 - 50%));
    background: #ff00d022;
    border: var(--border-width) solid #ff00d0;
    border-radius: 10px;
    text-align: center;
    font-family: 'Comic Sans MS', 'Comic Sans', sans-serif;
    color: #ff00d0;
    padding-bottom: 1em;
    padding-left: var(--default-padding);
    overflow: scroll;

    display: inline-block;

    h1 {
      color: #ff00d0;
    }

    @media screen and (max-width: calc(var(--max-width) + var(--default-padding) * 2)) {
      margin-left:  0;
      margin-right: 0;
    }

    button {
      background: #ff00d0;
      color: white;
      font-size: 1.2em;
      border-radius: 10px;
      padding: 3px 10px;
      border: 3px solid #ff00d0;
      font-family: 'Comic Sans MS', 'Comic Sans', sans-serif;
    }

    button:active {
      translate: 0 3px;
    }
  }
</style>

<p id="reducedMotionWarning">
  (If these animations are distracting, you can <a onclick="script:toggleAllAnimations()" style="cursor: pointer; text-decoration: underline" data-proofer-ignore>toggle them off/on</a>.)
</p>

<div id="cakeInput">
  <h1>&lt;input type="age"&gt;</h1>

  {%
    inline_svg
    filename="animated-birthday-cake.svg"
    id="animated-birthday-cake"
    alt="An animated illustration of a pink birthday cake. The cake has two layers and candles on top. As you watch, the cake gets wider and the number of candles increases."
  %}

  <h3 id="age">
  </h3>

  <button onclick="script:document.querySelector('svg').pauseAnimations();">
    That’s my age!
  </button>

  <button onclick="script:restartAnimation();">
    That’s wrong, try again!
  </button>

  <noscript>
    (Please enable JavaScript for this to work properly!)
  </noscript>
</div>

<script>
  function restartAnimation() {
    const currentSvg = document.querySelector('svg#animated-birthday-cake');

    const newSvg = currentSvg.cloneNode(true);  /* deep = true */

    currentSvg.after(newSvg);
    currentSvg.remove();
  }

  function getCurrentAge() {
    const width = getComputedStyle(document.querySelector('svg#animated-birthday-cake'))['width'];
    const pixels = Number(width.replace(/px/, ''));

    const candleCount = Math.floor((pixels - 50) / 2 / 10) - 2;

    document.querySelector("#age").innerHTML =
      candleCount <= 1
        ? "You were only just born!"
        : `You are ${candleCount} years old!`;
  }

  function toggleAllAnimations() {
    document.querySelectorAll("svg").forEach(svg => svg.pauseAnimations());
  }

  window.onload = function() {
    const isReduced =
      window.matchMedia(`(prefers-reduced-motion: reduce)`) === true |
      window.matchMedia(`(prefers-reduced-motion: reduce)`).matches === true;

    if (!!isReduced) {
      toggleAllAnimations();
      document.querySelector("#reducedMotionWarning").innerHTML = "(You have the “prefers reduced motion” setting, so I’ve disabled the animations. If you want to see them, you can <a onclick=\"script:toggleAllAnimations()\" style=\"cursor: pointer; text-decoration: underline;\">toggle them on/off</a>.)"
    }

    window.setInterval(getCurrentAge, 10);
  }
</script>

Let me answer some FAQs, and then I'll explain how it works:

**Why can't we just use `<input type="number">`?**
As many people are fond of saying, age is a state of mind, not a number.

**Will this input UI work on all devices?**
This is definitely on the wide side, but I tried it on the 52′ DiamondVision Ultra Mega Display where I do all my web development, and it fits just fine on there.
I'm sure that's all the testing we need, and nobody would ever have a smaller display where this design doesn't work.

**Can I license this UI to use in my apps?**
You certainly can!
Just send your mail-order form to me at the Institute of Good Ideas, Potassium Plaza, Rainy England.

**What's on your roadmap for V2?**
Adding a tinny MP3 of "Happy birthday" that autoplays at maximum volume whenever this UI is on screen.

I think we can all agree that this is a brilliant idea, and I'm sure all the major browsers will implement it within weeks.
I look forward to getting my cheques in the post.

[trunarla]: https://www.instagram.com/mewtru/

---

## How it works

The cake is drawn entirely using SVG animations, which I haven't used before.
I'm quite pleased with how well it works, and how close I was able to get to my original idea.
I know there are quite a few ways to do animation on the web; I wanted to experiment with the [SVG `<animate>` tag][animate].

The basic idea of the `<animate>` tag is that you can tell it different values that an attribute of an element can take over time.
For example, here I'm animating a rectangle by increasing the `width` it from 0 to 100, and then decreasing it back to 0 again:

```xml
<rect width="10" height="10" fill="black">
  <animate
    attributeName="width"
    values="0;100;0"
    dur="20s"
    repeatCount="5"
  />
</rect>
```

which looks like:

<figure>
  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 10" width="100%">
    <rect width="100" height="100" fill="black">
      <animate
        attributeName="width"
        values="0;100;0"
        dur="20s"
        repeatCount="indefinite"
      />
    </rect>
  </svg>
</figure>

It's pretty flexible – you can animate multiple properties on the same element; you can change non-numeric attributes like `fill` or `stroke`; you have a lot of control over how the animation behaves.
I did some brief experiments with simple shapes, enough to get a sense of how I could use it.

Now I knew how to animate attributes on SVG, I made a small icon of a static birthday cake.
There are plenty of existing icons like this on the web, but I made my own so I could keep the shapes simple – most icon sets are just a giant `<path>` exported from a drawing app, which I'd have to unpick.
Animating that would be harder than just creating my own icon.

I started with a little pencil-drawn sketch to work out the rough geometry, then I wrote the SVG by hand.
I still find it vaguely relaxing to create pictures from code.
This is what I came up with:

<style type="x-text/scss">
  #two_columns {
    display: grid;
    grid-template-columns: 2fr 1fr;
    grid-gap: var(--grid-gap);
    align-items: center;
  }
</style>

<figure id="two_columns">
  {%
    picture
    filename="hand-drawn-cake.jpg"
    width="750"
    alt="A sketch of some rectangles that loosely resemble a birthday cake, handwritten in a notebook with a few arrows to show various measurements."
  %}
  {%
    inline_svg
    filename="birthday-cake.svg"
    alt="A black-and-white icon of a birthday cake. The cake has two layers and five candles on top."
  %}
</figure>

Most of this is fairly vanilla SVG, using stuff I've written about before.
The candle flames and the curving line are both using [SVG masks], and the curves are drawn as a collection of [circular arcs].

The one interesting bit is the rounded corners on the two layers of cake, where only the top two corners are rounded.
You can set the corner radius of an SVG `<rect>` with the [`rx` attribute][rx], and you get the same curve on all four corners -- unlike the CSS [`border-radius` property][border-radius], which allows you to pick different radii for each corner.

To get curves on just two corners, I overlapped two rectangles – one with and without rounded corners.

<figure>
  {%
    inline_svg
    filename="round-rect.svg"
    alt="You can combine a rectangle with square corners and a pill shape to get a rectangle with two rounded corners on top."
  %}
</figure>

Because I'm only doing a solid fill, I'm rendering the two rectangles directly in the image -- but if I wanted a more complex fill, I could use this to create as a mask that I applied to another shape.

Once I had my basic icon, I created an extended version that has several hundred candles on it.
This is what the cake looks like when it's fully complete:

<figure class="wide_img">
  {%
    inline_svg
    filename="big-birthday-cake.svg"
    style="width: 100%;"
    alt="A black-and-white illustration of an extremely wide birthday cake."
  %}
</figure>

This has something like 200 candles on it; in hindsight I was way off my estimate of how old the oldest humans are.
According to Wikipedia, the [oldest humans] are closer to 120 years old.

I then sprinkled `<animate>` elements everywhere to make different parts of the cake appear at different times.
For the plate and the two cake layers, I'm animating the `width` attributes, so they gradually get bigger.

For the candles, I'm applying a mask which has an animated `width` attribute, so it gradually allows more and more of the candles to be seen.
That animation uses [`calcMode="discrete"`][calcMode], which causes it to do a distinct step at each tick, rather than a smooth animation between the two.
This means that you only ever see whole candles, rather than half-candles in the middle of the animation.

Finally, I added an animation to the `viewBox` attribute of the overall SVG – this means the width of the SVG increases as more candles become visible.
This allows me to get the current state of the animation in JavaScript:

```javascript
getComputedStyle(document.querySelector('svg'))['width']
// 158px
```

I know how far apart the candles are spaced, so I can use this to work out how many are visible at any given time.
There are other ways to inspect the state of an in-progress SVG animation; tying it to the geometry was the easiest in this case.

If you'd like to learn more, I encourage you to read <a href="https://github.com/alexwlchan/alexwlchan.net/blob/main/src/_images/2024/animated-birthday-cake.svg">the SVG file</a>.
It's a bit repetitive in parts, but overall I think it's fairly readable.

---

I learn a lot from doing mini-projects like this, and more than I would by just reading the documentation.
I didn't plan to work on this, but this particular idea – "animate a birthday cake" – sunk its teeth into my [hyperfocus] a few days ago, and I've been thinking about it ever since.
Posting this article will let me call the project "done" and move on to other things.

Animation is one of those topics that's always been just beyond what I can do – I knew that SVG animation is a thing, but I'd never actually tried it.
Now I have!

[animate]: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animate
[SVG masks]: /2021/inner-outer-strokes-svg/
[circular arcs]: /2022/circle-party/
[rx]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/rx
[border-radius]: https://developer.mozilla.org/en-US/docs/Web/CSS/border-radius
[oldest humans]: https://en.wikipedia.org/wiki/Oldest_people
[calcMode]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/calcMode
[hyperfocus]: /2023/hyperfocus-and-hobbies/
