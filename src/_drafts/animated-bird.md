---
layout: post
title: The new bird animation on Swift.org
summary: Trying
tags:
  - drawing things
  - web development
  - reading code
---
On Wednesday, the Swift.org website [got a redesign][redesign].
I don't write much Swift at the moment, but I glanced at the new website to see what's up and OOH!

There's a shiny animation with the bird logo:

<style>
  .light-video, .dark-video {
    aspect-ratio: 1652 / 1080;
    width: 100%;
  }

  .dark-video {
    display: none;
  }

  @media (prefers-color-scheme: dark) {
    .dark-video {
      display: block;
    }

    .light-video {
      display: none;
    }
  }
</style>

<figure>
  <video
    controls
    class="light-video"
    poster="/images/2025/swift_bird_light.jpg"
    src="/images/2025/swift_bird_light.mp4"></video>
  <video
    controls
    class="dark-video"
    poster="/images/2025/swift_bird_dark.jpg"
    src="/images/2025/swift_bird_dark.mp4"
    data-norss></video>
  <figcaption>
    Anybody who’s been out for a walk with me in the last month has watched me be transfixed by <a href="https://buttondown.com/alexwlchan/archive/may-2025-fluffy-birds-and-fancy-bookmarks/">cute and fluffy birds</a>, and now I get to bring that energy to my blog.
  </figcaption>
</figure>

I was curious how the animation worked.
I thought maybe it was an autoplaying video with no controls, but no, it's much cooler than that!
The animation is implemented entirely in code -- there are a few images, but all the dynamic parts all use JavaScript and the HTML5 canvas element.

I've never done anything with animation, so I started reading the code to understand how it works.
I'm not going to walk through it in detail, but I do want to show you some of what I learnt.

All the code from the Swift.org website is [open source on GitHub](https://github.com/swiftlang/swift-org-website/), and the JavaScript file that implements this animation was written by three engineers: [Federico Bucchi](https://github.com/federicobucchi), [Jesse Borden](https://github.com/jesseaborden), and [Nicholas Krambousanos](https://github.com/nkrambo).

[redesign]: https://www.swift.org/blog/redesigned-swift-org-is-now-live/




## Using a mask to gradually reveal the image

Most of the animation is made up of five "swoop" images, which look like strokes of a paintbrush.
These were clearly made by an artist in a design app like Photoshop.

<figure style="display: grid; grid-template-columns: repeat(3, 1fr); grid-gap: 1em;">
  <img src="/images/2025/orange-swoop-top.png" alt="" style="aspect-ratio: 1220 / 911;">
  <img src="/images/2025/purple-swoop.png" alt="" style="aspect-ratio: 1116 / 961;">
  <img src="/images/2025/orange-swoop-bottom.png" alt="" style="aspect-ratio: 1220 / 911;">
</figure>

These images are gradually revealed, so it looks like somebody actually painting with a brush.
This is more complex than a simple horizontal wipe, the sort of animation you might do in PowerPoint.
Notice how, for example, the purple swoop doubles back on itself -- if you did a simple left-to-right wipe, it would start as two separate swoops before joining into one.
It would look very strange!

Each swoop is animated in the same way, so let's focus on the purple one, just because it's the most visually interesting.

The technique is similar to something I've described on this blog before -- the animation is [applying a mask][masking] to the underlying image, and the mask gradually expands to show more and more of the image.
In particular, the mask matches the general shape of the brush stroke, so as it expands, it reveals more of the image.

The best way to explain this is with a quick demo: as you drag the slider back and forth, you can see the mask include more or less of the brush stroke, and that's reflected in the final image.

<style>
  #demo {
    display: grid;
    grid-template-columns: 1fr 20px 1fr 20px 1fr;
    grid-gap: 10px;
    align-items: center;
  }

  #demo > .cell > *:not(.label) {
    background: var(--background-color-light);
    border: 1px solid var(--body-text-light);
    text-align: center;
    display: block;
  }

  #demo > .cell .label {
    text-align: center;
    margin-top: 8px;
  }

  #demo .operator {
    text-align: center;
    font-size: 1.5em;
    margin-bottom: 1.5em;
  }

  #demo canvas {
    width: 100%;
  }
</style>

<script>
  async function loadImage(url) {
    const el = new Image()
    return new Promise((resolve, reject) => {
      el.onload = () => resolve(el)
      el.onerror = (err) => reject(err)
      el.src = url
    })
  }

  const swoop = {
    path: 'M-34 860C-34 860 42 912 102 854C162 796 98 658 50 556C2 454 18 48 142 88C272 130 290 678 432 682C574 686 434 102 794 90C1009 83 1028 280 1028 280',
    pathLength: 2776,
    lineWidth: 210,
    debugColor: 'purple',
    image: null,
    pathInstance: null,
  };

  function setMaskProgress(progress) {
    const canvas = document.querySelector('#plain-swoop');

    const ctx = canvas.getContext('2d');
    ctx.lineWidth = swoop.lineWidth * 1.1;
    ctx.lineCap = 'round';

    const pathInstance = new Path2D(swoop.path);

    ctx.strokeStyle = 'black';
    ctx.stroke(pathInstance);

    ctx.lineWidth = swoop.lineWidth;

    ctx.setLineDash([swoop.pathLength])
    ctx.lineDashOffset = swoop.pathLength * (1 - progress)
    ctx.strokeStyle = '#ddd';
    ctx.stroke(pathInstance);
  }

  function setResultProgress(progress) {
    const canvas = document.querySelector('#purple-swoop');

    const ctx = canvas.getContext('2d');
    ctx.lineWidth = swoop.lineWidth;
    ctx.lineCap = 'round';

    ctx.setLineDash([swoop.pathLength])
    ctx.lineDashOffset = swoop.pathLength

    const pathInstance = new Path2D(swoop.path);

    // Clear canvas before next draw
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    // Progress line dash offset
    ctx.lineDashOffset = swoop.pathLength * (1 - progress)
    // Draw stroke
    ctx.stroke(pathInstance)
    // Source-in will allow us to only draw as far as the stroke
    ctx.globalCompositeOperation = 'source-in'
    ctx.drawImage(swoop.image, 0, 0)
    // Reset to default for our next stroke paint
    ctx.globalCompositeOperation = 'source-out';
  }

  window.addEventListener("DOMContentLoaded", async function() {
    const image = await loadImage("/images/2025/purple-swoop.png");
    swoop.image = image;

    const pathInstance = new Path2D(swoop.path);
    swoop.pathInstance = pathInstance;

    setMaskProgress(0.5);
    setResultProgress(0.5);
  })

  function redrawDemo(value) {
    setMaskProgress(value);
    setResultProgress(value);
  }
</script>

<blockquote style="
  --body-text:          var(--body-text-light);
  --primary-color:      var(--primary-color-light);
  --accent-grey:        var(--accent-grey-light);
  --block-border-color: var(--block-border-color-light);
  --block-background:   var(--block-background-light);
  color: var(--body-text-light);
  padding: 1em;">
  <div id="demo">
    <div class="cell">
      <img src="/images/2025/purple-swoop.png" alt="" style="aspect-ratio: 1116 / 961;">
      <div class="label">original image</div>
    </div>
    <div class="operator">+</div>
    <div class="cell">
      <canvas id="plain-swoop" width="1116" height="961"></canvas>
      <div class="label">mask</div>
    </div>
    <div class="operator">=</div>
    <div class="cell">
      <canvas id="purple-swoop" width="1116" height="961"></canvas>
      <div class="label">final image</div>
    </div>
  </div>

  <div style="text-align: center; margin-top: 1em;">
    <em>animation progress:</em><br/>
    <input type="range" min="0" max="1" value="0.5" step="0.01" oninput="redrawDemo(this.value)" style="width: 300px; max-width: 100%; margin-top: 5px">
  </div>
</blockquote>

We can break this down into a couple of steps:

*   Take a curved path, and only draw part of it (drawing the mask)
*   Combine the partially-draw path with the original image (applying the mask)
*   Gradually increasing the amount of the path that we draw (animating the path)
*   Starting the animation when the page loads

Let's go through each of these in turn.

[masking]: /2021/inner-outer-strokes-svg/








---
---
---
---
---
--------

<blockquote class="toc">
  <h3>Table of contents</h3>

  <ul>
    <li><a href="#where">Where should I be looking?</a></li>
    <li>
      <a href="#mutationobserver">The animation is triggered by a <code>MutationObserver</code></a>
      <ul>
        <li><a href="#domcontentloaded">What about the <code>DOMContentLoaded</code> event?</a></li>
      </ul>
    </li>
    <li>
      <a href="#dashoffset">Making a path gradually appear by setting <code>lineDashOffset</code></a>
    </li>
  </ul>
</blockquote>







<style>
  .toc {
    background: var(--background-color);
    border-color: var(--primary-color);
  }

  .toc h3 {
    color: var(--body-text);
  }

  .toc ol > li:not(:last-child) {
    margin-bottom: 1em;
  }

  .toc ol > li > ul {
    list-style-type: disc;
  }

  .toc ol > li > ul > li > ul {
    list-style-type: circle;
  }

  .toc a:visited {
    color: var(--primary-color);
  }
</style>

---

<h2 id="where">Where should I be looking?</h2>

I started by poking around in the development tools in my browser, and I quickly found some images named "swoop" that are part of the animation:

{%
  picture
  filename="swoop.png"
  width="600"
  class="screenshot"
  alt="Screenshot of my web inspector showing an image of an orange swoop, which looks a bit like an orange painted brush stroke"
%}

I searched for the word "swoop" in the source code, and I found a collection of [`canvas` elements][canvas], one for each component of the animation:

{% annotatedhighlight
  lang="html"
  start_line="7"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/index.md?plain=1#L7"
%}
<div class="animation-container">
    <canvas id="purple-swoop" width="1248" height="1116"></canvas> <canvas id="purple-swoop" width="1248" height="1116"></canvas>
    <canvas id="white-swoop-1" width="1248" height="1116"></canvas>
    <canvas id="orange-swoop-top" width="1248" height="1116"></canvas>
    <canvas id="orange-swoop-bottom" width="1248" height="1116"></canvas>
    <canvas id="white-swoop-2" width="1248" height="1116"></canvas>
    <canvas id="bird" width="1248" height="1116"></canvas>
</div>
{% endannotatedhighlight %}

Then I found a file `hero.js` which is referencing these `canvas` elements and the associated images, in an array called `heroSwoops`:

{% annotatedhighlight
  lang="javascript"
  start_line="21"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L21-L34"
%}
const heroSwoops = [
  {
    canvas: document.querySelector('#purple-swoop'),
    path: 'M-34 860C-34 860 42 912 102 854C162 796 98 658 50 556C2 454 18 48 142 88C272 130 290 678 432 682C574 686 434 102 794 90C1009 83 1028 280 1028 280',
    pathLength: 2776,
    anchorPoints: [558, 480.5],
    position: [558, 640.5],
    imagePath: '/assets/images/landing-page/hero/purple-swoop.png',
    lineWidth: 210,
    debugColor: 'purple',
    image: null,
    state: { progress: offScreenDelta },
  },
  …
{% endannotatedhighlight %}

The most interesting variable here is what looks like an SVG [`path` attribute][svg_path].
I can't read this natively, but I can plug it into Mathieu Dutour's excellent [SVG Path Visualizer tool][pathviz] and it looks very similar to the purple swoop image:

<style>
  #swoop_comparison {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 1em;
  }

  @media screen and (max-width: 500px) {
    #swoop_comparison {
      grid-template-columns: auto;
    }
  }
</style>

<figure id="swoop_comparison">
  <img src="/images/2025/purple-swoop.png" alt="A purple brush stroke that goes up and down several times in a fancy swoop">
  {%
    picture
    filename="svg_pathviz.png"
    width="500"
    class="screenshot"
    alt="Screenshot of the path visualizer, with a breakdown of how the path works and an annotated swoop that matches the purple swoop."
  %}
</figure>

I don't know what this file does yet, but most of `hero.js` is a function called `heroAnimation`.
That sounds promising!
I did a quick skim, and it has code for loading images, and something to do with HTML canvas -- presumably that's manipulating the canvas elements I found in the HTML.

Then I saved the HTML, images, and `hero.js` locally.
When I tried to load the site, I got an error about an undefined variable `anime`, coming from this line:

{% annotatedhighlight
  lang="javascript"
  start_line="177"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L177-L179"
%}
const tl = anime.createTimeline({
  defaults: { duration: DURATION, ease: 'in(1.8)' },
})
{% endannotatedhighlight %}

To get past this error, I also needed to save a file `anime.js`, which is a copy of Julian Garnier's [Anime.js library][anime_js].

These are the files I ended up saving locally:

```
{root}
 ├─ swift.html
 ├─ static/
 │   ├─ anime.iife.min.js       (vendored copy of Anime.js
 │   ├─ application.css         (styles for the page)
 │   ├─ color-scheme-toggle.js  (controls light/dark mode)
 │   ├─ hero.js                 (has the heroAnimation() function)
 │   └─ noise.png               (background texture)
 └─ images/
     ├─ bird.png
     ├─ orange-swoop-bottom.png
     ├─ orange-swoop-top.png
     ├─ purple-swoop.png
     ├─ white-swoop-1.png
     └─ white-swoop-2.png
```

This gave a [static copy of the site][zip] which I could hack on locally, add my own debugging code, and generally try to pick apart.
If you want to step through the animation in detail, this gives you a self-contained example you can play with.

[canvas]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas
[anime_js]: https://animejs.com
[zip]: /files/2025/swift_animation.zip



---



<h2 id="mutationobserver">The animation is triggered by a <code>MutationObserver</code></h2>

In the `hero.js` file, there's a function `heroAnimation`.
I don't know what it does yet, but that must be what actually runs the animation.
When I open the page in my browser, I can see the animation starts shortly afterward, but what's calling the `heroAnimation` function?

Looking for `heroAnimation`, I found it being called at the end of `hero.js`:

{% annotatedhighlight
  lang="javascript"
  start_line="282"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L282-L294" %}
// Start animation when container is mounted
const observer = new MutationObserver(() => {
  const animContainer = document.querySelector('.animation-container')
  if (animContainer) {
    observer.disconnect()
    heroAnimation(animContainer)
  }
})

observer.observe(document.documentElement, {
  childList: true,
  subtree: true,
})
{% endannotatedhighlight %}

This is all new to me; I've never seen `MutationObserver` before.
But I can guess what it means from the name, and the [MDN documentation][MutationObserver] confirms my guess:

> The `MutationObserver` interface provides the ability to watch for changes being made to the DOM tree.

When this code calls `observer.observe()`, it starts watching for elements made to `document.documentElement` -- which in practice, any changes to the DOM of the entire page -- and when it sees a change, it runs the callback function.

That callback starts by looking for an element with the `animation-container` class, which is the collection of canvas elements I found earlier.
If it finds a matching element, it stops the observer and starts the hero animation.
This means the animation will only be started once, the first time the container appears on the page.

Although I've never used MutationObserver, it feels vaguely familiar.
It reminds me of React and Next.js, which would push changes to the DOM whenever the input changes.
This feels like the inversion of that: where React watches for changes in the input, a MutationObserver watches for changes in the DOM.

[MutationObserver]: https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver

<h3 id="domcontentloaded">What about the <code>DOMContentLoaded</code> event?</h3>

Because the animation starts when the page loads, I was expecting something like:

```javascript
document.addEventListener("DOMContentLoaded", heroAnimation)
```

I don't think there's much difference in this particular case, but I can see that `MutationObserver` is much more flexible for the general case.
You can target a more precise element than "the entire document", and you can look for changes beyond just the initial load.

I suspect the `MutationObserver` approach may also be slightly faster -- I added a bit of console logging, and I can see the `MutationObserver` callback is called three times when loading the Swift.org homepage.
If the animation container exists on the first call, you can start the animation immediately, rather than waiting for the rest of the DOM to load.
I'm not sure if that's a perceptible difference though, except for very large and complex web pages.



---


<style>
/*  canvas {
    border: var(--border-width) var(--border-style) var(--block-border-color);
    border-radius: var(--border-radius);
    background-color: var(--block-background);
    width: calc(100% - 6px);
    margin: 0 auto;
  }*/

  pre:has( + canvas) {
    border-bottom-left-radius:  0;
    border-bottom-right-radius: 0;
    margin-bottom: 5px;
  }

  pre + canvas {
    border-top-left-radius:  0;
    border-top-right-radius: 0;
  }
</style>



<h2 id="animating">Animating the painted strokes</h2>



<h3 id="dashoffset">Making a path gradually appear by setting <code>lineDashOffset</code></h3>

If you draw a stroke in an HTML5 canvas, it appears as a solid line.

```javascript
const canvas = document.querySelector('#zigzag');
const ctx = canvas.getContext('2d');

ctx.lineWidth = 10;

const path = new Path2D("M0,25 500,25");
ctx.stroke(path);
```

<canvas id="zigzag" width="500" height="50"></canvas>

You can set a line dash pattern with the [`setLineDash()` function](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/setLineDash).
You pass an array of values, which specify the alternating length of lines and gaps.
Here are three examples:

```javascript
const path1 = new Path2D("M0,25 500,25");
ctx.setLineDash([50]);
ctx.stroke(path1);

const path2 = new Path2D("M0,50 500,50");
ctx.setLineDash([60, 30]);
ctx.stroke(path2);

const path3 = new Path2D("M0,75 500,75");
ctx.setLineDash([40, 30, 20, 10]);
ctx.stroke(path3);
```

<canvas id="linedash" width="500" height="100"></canvas>

You can apply a line dash to any path -- I'm using straight lines for simplicity, but you can also apply it to more complex paths:

```javascript
const path = new Path2D(
  "M 20,50 " +
  "Q 70,0 120,50 Q 170,100 220,50 " +
  "Q 270,0 320,50 Q 370,100 420,50 " +
  "Q 470,0 520,50 Q 570,100 620,50"
);
ctx.setLineDash([25]);
ctx.stroke(path);
```

<canvas id="curvedash" width="500" height="100"></canvas>


<script>
  window.addEventListener("DOMContentLoaded", function() {
    const bodyText =
      window
        .getComputedStyle(document.body)
        .getPropertyValue('--body-text');

    const canvas = document.querySelector('#zigzag');
    const ctx = canvas.getContext('2d');

    ctx.lineWidth = 10;
    ctx.strokeStyle = bodyText;

    const pathInstance = new Path2D("M0,25 500,25");
    ctx.stroke(pathInstance);
  })

  window.addEventListener("DOMContentLoaded", function() {
    const bodyText =
      window
        .getComputedStyle(document.body)
        .getPropertyValue('--body-text');

    const canvas = document.querySelector('#linedash');
    const ctx = canvas.getContext('2d');

    ctx.lineWidth = 10;
    ctx.strokeStyle = bodyText;

    const pathInstance1 = new Path2D("M0,25 500,25");
    ctx.setLineDash([50]);
    ctx.stroke(pathInstance1);

    const pathInstance2 = new Path2D("M0,50 500,50");
    ctx.setLineDash([60, 30]);
    ctx.stroke(pathInstance2);

    const pathInstance3 = new Path2D("M0,75 500,75");
    ctx.setLineDash([40, 30, 20, 10]);
    ctx.stroke(pathInstance3);
  })

  window.addEventListener("DOMContentLoaded", function() {
    const bodyText =
      window
        .getComputedStyle(document.body)
        .getPropertyValue('--body-text');

    const canvas = document.querySelector('#curvedash');
    const ctx = canvas.getContext('2d');

    ctx.lineWidth = 10;
    ctx.strokeStyle = bodyText;

    const pathInstance = new Path2D(
      "M 20,50 " +
      "Q 70,0 120,50 Q 170,100 220,50 " +
      "Q 270,0 320,50 Q 370,100 420,50 " +
      "Q 470,0 520,50 Q 570,100 620,50"
    );
    ctx.setLineDash([25]);
    ctx.stroke(pathInstance);
  })
</script>








{% comment %}

---

<h2 id="heroanimation">What's happening in <code>heroAnimation()</code>?</h2>

This function is doing a bunch of stuff, and now I can see it being called when the page loads.
What's it actually doing?

<h3 id="initvar">Setting up the initial variables</h3>

The first chunk of the function is just setting up some variables.

{% annotatedhighlight
  lang="javascript"
  start_line="2"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L2-L4" %}
const isReduceMotionEnabled = window.matchMedia(
  '(prefers-reduced-motion: reduce)',
).matches
{% endannotatedhighlight %}

This detects whether the user has the ["prefer reduced motion" preference][prefers-reduced-motion], and is used later to disable the animation if so.
If you set this preference, the bird never animates, it just appears.

This is an important accessibility feature, and I wish more sites paid attention to it.

[prefers-reduced-motion]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion

{% annotatedhighlight
  lang="javascript"
  start_line="5"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L5-L6" %}
const urlParams = new URLSearchParams(location.search)
const hasDebugParam = urlParams.has('debug')
{% endannotatedhighlight %}

This checks if there's a `debug` parameter in the URL query string.
There is code that uses this variable, but I can't see any effect when I set it?
Weird.

I wonder if I need to do something extra in my browser to enable the debug behaviour, or if it's a broken leftover from when this code was being written.

{% annotatedhighlight
  lang="javascript"
  start_line="8"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L8-L15" %}
async function loadImage(url) {
  const el = new Image()
  return new Promise((resolve, reject) => {
    el.onload = () => resolve(el)
    el.onerror = (err) => reject(err)
    el.src = url
  })
}
{% endannotatedhighlight %}

This function loads an image from a URL, then the Promise completes.
I'm not sure what this is for yet; I guess I'll find out later.

{% annotatedhighlight
  lang="javascript"
  start_line="17"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L17-L19" %}
// Skip to visible portion of animation when cropped on small screens
const { left, width } = animContainer.getClientRects()[0]
const offScreenDelta = Math.abs(left) / width
{% endannotatedhighlight %}

These variables are something to do with the geometry of the animation container.
In particular, [`getClientRects()`][getClientRects] tells us the dimensions of its bounding box.
I'm not sure what these variables are used for yet.

[getClientRects]: https://developer.mozilla.org/en-US/docs/Web/API/Element/getClientRects

{% annotatedhighlight
  lang="javascript"
  start_line="21"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L21-L34"
%}
const heroSwoops = [
  {
    canvas: document.querySelector('#purple-swoop'),
    path: 'M-34 860C-34 860 42 912 102 854C162 796 98 658 50 556C2 454 18 48 142 88C272 130 290 678 432 682C574 686 434 102 794 90C1009 83 1028 280 1028 280',
    pathLength: 2776,
    anchorPoints: [558, 480.5],
    position: [558, 640.5],
    imagePath: '/assets/images/landing-page/hero/purple-swoop.png',
    lineWidth: 210,
    debugColor: 'purple',
    image: null,
    state: { progress: offScreenDelta },
  },
  …
{% endannotatedhighlight %}

This is an array with five entries that correspond to the five "swoop" images in the animation.
I don't really understand what all the values do yet, but I'm guessing they're something to do with the geometry of the swoop.

I imagine it'll become clear what these variables are for as I read the rest of the code.

There's a similar variable for the bird logo, which doesn't have an SVG path but does have some geometry variables I assume will make sense later:

{% annotatedhighlight
  lang="javascript"
  start_line="83"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L83C3-L92C4"
%}
const logo = {
  canvas: document.querySelector('#bird'),
  positionStart: [899.2, 202.5],
  positionEnd: [1084, 388],
  anchorPoints: [304, 268.5],
  position: [610, 672.5],
  imagePath: '/assets/images/landing-page/hero/bird.png',
  image: null,
  state: { progress: offScreenDelta },
}
{% endannotatedhighlight %}

[svg_path]: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/path
[pathviz]: https://svg-path-visualizer.netlify.app/#M-34%20860C-34%20860%2042%20912%20102%20854C162%20796%2098%20658%2050%20556C2%20454%2018%2048%20142%2088C272%20130%20290%20678%20432%20682C574%20686%20434%20102%20794%2090C1009%2083%201028%20280%201028%20280

<h3 id="initswoops">Even more setup in the <code>initSwoops()</code> and <code>initLogo()</code> functions</h3>

After setting up all the variables, there's an [`initSwoops()` function][initSwoops] that takes a bunch of variables from the `heroSwoops` array, and returns two values:

1.  A [canvas drawing context][getContext], with a couple of properties like the thickness of lines and the line dash pattern.
    Here's what happens in the default case:

    ```javascript
    const ctx = canvas.getContext('2d')

    // The reference animation's transform origin is in the center of the canvas
    // We're not going to reset this as it will make pulling values directly from AE easier
    ctx.translate(posX - image.naturalWidth / 2, posY - image.naturalHeight / 2)

    // Set mask styles
    ctx.lineWidth = lineWidth
    ctx.lineCap = 'round'

    ctx.setLineDash([pathLength])
    ctx.lineDashOffset = pathLength
    ```

    That mention of mask styles is intriguing -- I've played with [masks for SVG](/2021/inner-outer-strokes-svg/), but never in an HTML canvas.

2.  A [`Path2D` object][Path2D] that follows the `path` defined in `heroSwoops`.
    This is only a single line:

    ```javascript
    let pathInstance = new Path2D(path)
    ```

By default, this function still isn't drawing anything, just setting up more objects.

It includes the code for handling the "prefer reduced motion" setting -- it draws the PNG image in the drawing context, which makes it appear immediately.
It also doesn't set the line dash pattern, which makes me think that must be important for the animation.

This function also includes some debugging code, but when I set add `?debug=true` to my URL, nothing seems to happen.
I can see the debugging branch is activated, but I can't seee any effect.

There's also an [`initLogo()` function][initLogo], which looks very similar.
It sets up a drawing context and handles "prefer reduced motion", but doesn't actually draw anything.

I can see these functions get called almost immediately, and then they attach these new contexts and `Path2D` instance to the `heroSwoops` and `logo` variables:

{% annotatedhighlight
  lang="javascript"
  start_line="148"
  src="https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L148C5-L164C30"
%}
// Load swoop images
const swoopImages = await Promise.all(
  heroSwoops.map((swoop) => loadImage(swoop.imagePath)),
)
// Load logo
const logoImage = await loadImage(logo.imagePath)

logo.image = logoImage
// Init canvas for each swoop layer
heroSwoops.forEach((swoop, i) => {
  swoop.image = swoopImages[i]
  const canvasData = initSwoops(swoop)
  swoop.ctx = canvasData.ctx
  swoop.pathInstance = canvasData.pathInstance
})
// Init logo canvas
logo.ctx = initLogo(logo)
{% endannotatedhighlight %}

So now we've set the initial state of the animation -- but how does it actually move?

[initSwoops]: https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L94
[initLogo]: https://github.com/swiftlang/swift-org-website/blob/10539c474bea9a084bd90daac387fde6b62bd0c4/assets/javascripts/new-javascripts/hero.js#L127-L145
[getContext]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext
[Path2D]: https://developer.mozilla.org/en-US/docs/Web/API/Path2D/Path2D

<h3 id="globalCompositeOperation">Actually animating the strokes with <code>globalCompositeOperation</code></h3>

---
---
---
a couple of geometry variables



what's that path?
let's plug into SVG path visualizer

https://svg-path-visualizer.netlify.app/#M-34%20860C-34%20860%2042%20912%20102%20854C162%20796%2098%20658%2050%20556C2%20454%2018%2048%20142%2088C272%20130%20290%20678%20432%20682C574%20686%20434%20102%20794%2090C1009%2083%201028%20280%201028%20280

looks familiar!

then a function `initSwoops` and `initLogo`

* initSwoops creates a drawing context on a canvas https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/getContext

    ```javascript
    const ctx = canvas.getContext('2d')
    ```

    if reduce motion: just draw image immediately, `ctx.drawImage(image, 0, 0)`

    otherwise, adds a path to the canvas
    this stroke follows the path we got above
    doesn't appear visually, just a Path2D object https://developer.mozilla.org/en-US/docs/Web/API/Path2D/Path2D

    looks like debug code to actually draw the path visually, but adding `?debug=true` to the URL didn't work
    I wonder if I'm doing something wrong, or if it's leftover debugging code that's since broken

*   initLogo creates another drawing context

    if reduce motion, adds image immediately
    presumably this is for the bird logo

then some code which loads all the images, and calls initSwoops and initLogo:

```javascript
try {
  // Load swoop images
  const swoopImages = await Promise.all(
    heroSwoops.map((swoop) => loadImage(swoop.imagePath)),
  )
  // Load logo
  const logoImage = await loadImage(logo.imagePath)

  logo.image = logoImage
  // Init canvas for each swoop layer
  heroSwoops.forEach((swoop, i) => {
    swoop.image = swoopImages[i]
    const canvasData = initSwoops(swoop)
    swoop.ctx = canvasData.ctx
    swoop.pathInstance = canvasData.pathInstance
  })
  // Init logo canvas
  logo.ctx = initLogo(logo)
} catch (error) {
  console.error('Error loading images:', error)
  throw error
}
```

then we bail out if reduce motion:

```
  // Skip animation if reduced motion is enabled
  if (isReduceMotionEnabled) {
    return
  }
```

## actually running the animation

okay, it's a timeline in Anime.js: https://animejs.com/documentation/timeline/

```
  const tl = anime.createTimeline({
    defaults: { duration: DURATION, ease: 'in(1.8)' },
  })
```

and a swoopUpdate function:

```
  const swoopUpdate = ({
    state,
    ctx,
    pathLength,
    pathInstance,
    image,
    canvas,
  }) => {
    // Clear canvas before next draw
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    // Progress line dash offset
    ctx.lineDashOffset = pathLength * (1 - state.progress)
    // Draw stroke
    ctx.stroke(pathInstance)
    // Source-in will allow us to only draw as far as the stroke
    ctx.globalCompositeOperation = 'source-in'
    ctx.drawImage(image, 0, 0)
    // Reset to default for our next stroke paint
    ctx.globalCompositeOperation = 'source-out'
  }
```

this looks like a function which is called to update the state of the animation

`globalCompositeOperation` is interesting!
https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/globalCompositeOperation
so only see stuff that's inside the stroke
AHA
so that's how it works
cannot just animate left to right, would look wrong -- animates along the stroke

break it down into minimal example

## start the stroke animations

https://animejs.com/documentation/timeline/timeline-methods/add

here's an animation for the stroke:

```
  tl.add(
    heroSwoops[1].state,
    {
      progress: 1,
      duration: 950 - 950 * offScreenDelta,
      onUpdate: () => swoopUpdate(heroSwoops[1]),
    },
    'start',
  )
```

heroSwoops[1].state = `{ progress: offScreenDelta }`, which is 0

then set of animation parameters:

* `progress: 1` means it will animate this progress variable from 0 to 1
    -> bit confused, no parameter named this in anime.js docs
    -> realised it's from the state parameter in `heroSwoops`
* duration = how long it will take, 950 = 950ms, just under a second
* onUpdate = every time the animation updates, it calls the swoopUpdate function

final param is position, tells us when it will begin = begins from start of animation

let's comment out all but one of these, and slow down the animation:

```
  tl.add(
    heroSwoops[0].state,
    {
      progress: 1,
      duration: 9500 - 9500 * offScreenDelta,
      onUpdate: () => swoopUpdate(heroSwoops[0]),
    },
    'start',
  )
```

can see it more clearly -- image is following stroke

## animate the logo

```
  tl.add(
    logo.state,
    {
      ease: 'out(1.2)',
      duration: 2000 - 2000 * offScreenDelta,
      delay: 7500 - 7500 * offScreenDelta,
      progress: 1,
      onUpdate: () => {
        const {
          state: { progress },
          ctx,
          image,
          canvas,
          positionStart: [startX, startY],
          positionEnd: [endX, endY],
        } = logo
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        // Progresses logo opacity from 0 to 1
        ctx.globalAlpha = progress
        const deltaX = (endX - startX) * progress
        const deltaY = (endY - startY) * progress
        ctx.drawImage(image, deltaX, deltaY)
      },
    },
    'start',
  )
```

wasn't sure what it was doing -- slow it down, becomes v obvious
fades in and translates diagonally
with that in mind, X/Y variables are obvious -- dictate current position

https://animejs.com/documentation/animatable/animatable-settings/ease

* ease is interesting

---

takeaways

* anime.js library and timelines
* MutationObserver
* globalCompositeOperation

this is super cool!


animation is one of those topics that's always felt daunting to me, esp because involves graphics programs, ooh scary
not all of this is code -- somebody had to create those graphic assets
first time I've thought "oh, I get it"
I can see a path to creating my own animations this way

(will i? questionable, have many ideas that never go anywhere!)
but it feels a bit easier than it did before

{% endcomment %}