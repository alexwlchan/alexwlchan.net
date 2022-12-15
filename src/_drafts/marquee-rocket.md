---
layout: post
title: Launching a rocket with the &lt;marquee&gt; tag
summary: You can get surprisingly far with 1990s technology.
tags: code-crimes html
theme:
  card_type: summary_large_image
  image: /images/2022/artemis_launch.jpg
index:
  tint_color: "#382b20"
---

<style>
  #directions,
  #scroll_delay,
  #truespeed {
    display: grid;
    grid-gap: 10px;
  }

  #directions .wrapper,
  #scroll_delay .wrapper,
  #truespeed .wrapper {
    width: 100%;
  }

  #directions {
    grid-template-columns: calc(50% - 5px) calc(50% - 5px);
  }

  #scroll_delay {
    grid-template-columns: calc(50% - 5px) calc(50% - 5px);
  }

  #truespeed {
    grid-template-columns: auto;
  }

  .wrapper {
    border: 3px solid #f0f0f0;
    background: black;
    color: white;
    max-width: 582px;
    margin-left:  auto;
    margin-right: auto;
    border-radius: 10px;
    text-align: center;
    font-family: Helvetica, Arial, sans-serif;
    position: relative;
  }

  .wrapper button {
    position: absolute;
    right: 5px;
    top: 5px;
    background: white;
    color: black;
    border-radius: 2px;
  }
</style>

Last month, NASA made headlines as they (finally) launched their SLS rocket as part of the Artemis 1 mission.
Some critics of the SLS have pointed out that it's based on old technology, including engines that [literally flew on the Shuttle][shuttle] -- but I don't think that's an issue.
I'm a big fan of using old tech -- if it's tried and tested, why not use it?

NASA's rocket reminded me of [a web app][glitch] I made last year, which allows you to control a rocket in the web browser -- all using web technology from the 1990s.
In this post, we'll peek under the covers and see how it works.

<picture>
  <source
    srcset="/images/2022/marquee_rocket_1x.webp 1x,
            /images/2022/marquee_rocket_2x.webp 2x,
            /images/2022/marquee_rocket_3x.webp 3x"
    type="image/webp"
  >
  <source
    srcset="/images/2022/marquee_rocket_1x.png 1x,
            /images/2022/marquee_rocket_2x.png 2x,
            /images/2022/marquee_rocket_3x.png 3x"
    type="image/png"
  >
  <img
    src="/images/2022/marquee_rocket_1x.png"
    class="screenshot"
  >
</picture>

<p id="reduceMotion">
  <strong>Accessibility note:</strong> this post has a lot of moving text and images.
  If you find that distracting, you can <button id='playPauseAll' onclick='script:toggleAllMarquees();'>pause all</button> or play/pause the individual examples.
</p>

[shuttle]: https://www.space.com/artemis-1-space-shuttle-hardware
[glitch]: http://marquee-rocket.glitch.me/



  {% separator "marquee-870892.svg" %}






---

---


In this post, I'll show you how I made [a web app][glitch] which allows you to control a rocket in the browser using 1990s web technology.
Nothing will hold us back -- not gravity, not physics, not taste and decency.


The launch reminded me of a silly project I made at the end of last year.
I meant to write about it at the time, forgot, and then I was reminded of it today.



This started when Laurie Voss ran an [&lt;Angle&gt; Bracket tournament][tournament], a series of Twitter polls to determine the Internet's favourite HTML tag.
I was following [Danielle Leong][leong], who was a fearless cheerleader of the marquee tag, and I discovered the tournament through her tweets.

The final four tags were &lt;a&gt;, &lt;div&gt;, &lt;marquee&gt; and &lt;script&gt;, and Laurie tweeted what could only be read as a challenge:

{% tweet https://twitter.com/seldo/status/1461848209769197573 %}

How far could I get with just &lt;marquee&gt;?

This post is going to explain how I made the [&lt;marquee&gt; rocket][glitch], and give you a little tour of the Internet's second favourite HTML tag.

<p id="reduceMotion">
  (This post has a bunch of moving text. If you find that distracting, you can <button id='playPauseAll' onclick='script:toggleAllMarquees();'>pause all</button> or play/pause them manually.)
</p>

[tournament]: https://theanglebracket.com
[leong]: https://twitter.com/tsunamino/status/1461429962708193280



  {% separator "marquee-870892.svg" %}



If you've been unfortunate enough to miss it, the [&lt;marquee&gt; tag][mdn] creates a scrolling bit of text:

```html
<marquee>This text will scroll</marquee>
```

which scrolls from right-to-left, like this:

<div id="first_example">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('first_example')">pause</button>
    <marquee>This text will scroll</marquee>
  </div>
</div>

Today it's been replaced by more modern techniques like CSS transitions and animations, but it still has a fond place in the heart of old-school web nerds.
(Hi.)

I started by putting a rocket emoji in a marquee tag, which felt like a good start:

```html
<marquee>🚀</marquee>
```

but this rocket can only move in one direction, and it's going backwards.
Almost all [rocket emojis][emojis] are pointing towards the upper-right, so a rocket going leftward is going in the wrong direction.



  {% separator "marquee-870892.svg" %}



The &lt;marquee&gt; tag supports a `direction` attribute which lets you specify which way your scrolling text should go:

<div id="directions">
  <div class="wrapper">
    direction="up"
    <marquee direction="up">🚀</marquee>
  </div>
  <div class="wrapper">
    <button onclick="toggleMarqueFor('directions')">pause</button>
    direction="right"
    <marquee direction="right">🚀</marquee>
  </div>
  <div class="wrapper">direction="down"<marquee direction="down">🚀</marquee></div>
  <div class="wrapper">direction="left"<marquee direction="left">🚀</marquee></div>
</div>

It only supports the four cardinal directions; you can't, for example, combine the attributes `direction="up left"` to get diagonally scrolling text.
This is probably for the best, as it avoids somebody like me trying to set `direction="up down"`.

[mdn]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee
[emojis]: https://emojipedia.org/rocket/



  {% separator "marquee-870892.svg" %}



A couple of other interesting attributes are `scrollamount`, `scrolldelay`, and `truespeed`, which configure how fast the text scrolls.
Text always moves at a fixed speed, but you can pick what it is.

Scrolling text is updated at discrete intervals, rather than as a continuous motion -- I wonder if that reflects the limitation of graphics cards in the 1990s?
This becomes more obvious if you increase the `scrolldelay`, which is the number of milliseconds between intervals.
As the intervals get further apart, they become more visible:

<div id="scroll_delay">
  <div class="wrapper">
    scrolldelay = 1000 (1s) <br/>
    scrollamount = 10
    <marquee scrolldelay="1000" scrollamount="10">🚀</marquee>
  </div>
  <div class="wrapper">
    <button onclick="toggleMarqueFor('scroll_delay')">pause</button>
    scrolldelay = 60 (0.06s)<br/>
    scrollamount = 10
    <marquee scrolldelay="60" scrollamount="10">🚀</marquee>
  </div>
  <div class="wrapper">scrolldelay = 1000 (1s)<br/>scrollamount = 20<marquee scrolldelay="1000" scrollamount="20">🚀</marquee></div>
  <div class="wrapper">scrolldelay = 60 (0.06s)<br/>scrollamount = 20<marquee scrolldelay="60" scrollamount="20">🚀</marquee></div>
</div>

If you want to crank down the interval below 60&nbsp;milliseconds, you have to add the `truespeed` attribute, otherwise it gets clamped to a 60&nbsp;ms refresh interval.
This feels like another clue that this tag is designed to avoid over-taxing the graphics card.

<div id="truespeed">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('truespeed')">pause</button>
    scrolldelay = 60 (0.06s) <br/>
    without truespeed
    <marquee scrolldelay="60">🚀</marquee>
  </div>
  <div class="wrapper">
    scrolldelay = 1 (0.001s) <br/>
    without truespeed
    <marquee scrolldelay="1">🚀</marquee>
  </div>
  <div class="wrapper">
    scrolldelay = 1 (0.001s) <br/>
    with truespeed
    <marquee scrolldelay="1" truespeed>🚀</marquee>
  </div>
</div>

All these parameters are great, but they just allow me to create a static rocket.
A true web app requires interactivity -- how can I achieve that with a marquee tag?



  {% separator "marquee-870892.svg" %}



My brainwave was realising that a marquee tag with `scrollamount="0"` is a static element, which I can position wherever I like:

```html
<marquee scrollamount="0">this text won’t move</marquee>
```

<div class="wrapper">
  <marquee scrollamount="0">this text won’t move</marquee>
</div>

And it supports the [onclick attribute][onclick], which allowed me to build something which is a very poor imitation of a button:

```html
<marquee scrollamount="0" onclick="document.getElementById('rocket').direction = 'left'">
  go left
</marquee>
```

You can run arbitrary JavaScript inside the `onclick` handler, so I could control the direction and speed of the rocket by modifying the attributes on the marquee element.
I then positioned the buttons with `position: absolute;` and fixed margins, which let me create a little control panel:

<picture>
  <source
    srcset="/images/2022/marquee_buttons_1x.webp 1x,
            /images/2022/marquee_buttons_2x.webp 2x"
    type="image/webp"
  >
  <source
    srcset="/images/2022/marquee_buttons_1x.png 1x,
            /images/2022/marquee_buttons_2x.png 2x"
    type="image/png"
  >
  <img
    src="/images/2022/marquee_buttons_1x.png"
    class="screenshot"
  >
</picture>

The play/pause button is a bit interesting; initially I considered toggling the `scrollamount` attribute between 0 and its current value, but it got a bit fiddly because you could also reduce the `scrollamount` to 0 with the speed controls.
Re-reading the MDN docs, I discovered that marquee has [start() and stop() methods][methods] which will start and stop the scrolling. Perfect!

But as far as I can tell, there's no way to programatically determine whether a marquee tag is currently scrolling -- I had to track whether it was stop/started in an external variable.

This is also where you really see the differences in browser support.
In Safari, clicking these buttons will change direction immediately -- the rocket can zigzag across the page.
In Chrome, clicking these buttons won't take effect until it scrolls off the edge of the window.
In Firefox, clciking these buttons take effect immediately, but it restarts the scroll from the edge of the window.

The speed controls are similarly inconsistent -- in Firefox and Safari, the speed changes immediately, but in Chrome it waits for the next cycle.

The marquee tag has been deprecated for years, and even when it was supported there were probably only a handful of sites (if any) that were dynamically changing the direction or speed.
It's hardly surprising that a consensus has failed to emerge.

[onclick]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/onclick
[methods]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#methods



  {% separator "marquee-870892.svg" %}


If you load the [marquee rocket](http://marquee-rocket.glitch.me/), you're expecting something that moves around the page -- that's the whole point.
But while I was writing this blog post, I was initially unsure of what to do.

I find the inline examples useful; I think seeing what the HTML will do is better than having it described.
But all that motion can be distracting for some readers, and makes it harder for them to read the text.
(It's distracting for me as I'm writing it.)
Do I include the examples, or not?

And then it struck me – I already know how to stop/start a scrolling marquee tag!
I've added play/pause buttons to each group of examples, plus a pagewide button at the top of the post.
The examples will scroll by default, but if it's distracting you can turn it off.

As I was writing this post, I also learnt that browsers can send a [prefers-reduced-motion CSS media feature][prm] that asks web pages to turn off unnecessary animation.
If you've got that setting enabled, I disable scrolling by default, but you can switch it back on if you'd find it useful.

[prm]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion



  {% separator "marquee-870892.svg" %}



I learnt a couple of extra things about the marquee tag while writing this post.

First: it scrolls from right-to-left in my browser, but it varies based on your text direction.
In particular, if you specify a [right-to-left script][rtl] using [the dir attribute][dir], the marquee tag will scroll from left-to-right (opposite to the direction of text):

```html
<marquee dir="ltr">hello world</marquee>
<marquee dir="rtl">مرحبا بالعالم</marquee>
```

<div id="rtl_text" class="wrapper" style="position: relative;">
  <button onclick="toggleMarqueFor('rtl_text')">pause</button>
  <marquee dir="ltr">hello world</marquee>
  <marquee dir="rtl">مرحبا بالعالم</marquee>
</div>

I also accidentally learnt that it's possible to nest marquee tags:

```html
<marquee>
  This text
  <marquee>
    This text
    <marquee>This text will scroll</marquee>
    will scroll
  </marquee>
  will scroll
</marquee>
```

which looks about as good as you'd expect (and different across browsers):

<div id="nested">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('nested')">pause</button>
    <marquee style="color: #d01c11;">
      This text
      <marquee style="color: #d0c611;">
        This text
        <marquee style="color: #1131d0;">This text will scroll</marquee>
        will scroll
      </marquee>
      will scroll
    </marquee>
  </div>
</div>

I learnt this when I screwed up the escaping in my Markdown source file, and got an HTML file with half a dozen unclosed &lt;marquee&gt; tags.
I was struck by the complete visual mess that stood before me.
The possibilities are as endless as they are horrifying.

[rtl]: https://en.wikipedia.org/wiki/Right-to-left_script
[dir]: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/dir



  {% separator "marquee-870892.svg" %}



Why am I telling you all this?
No matter how
despite my best effort, not going to lead to resurgence of marquee tag

<script>
  var isAllMarqueeScrolling = true;

  function toggleAllMarquees() {
    for (let id of ['first_example', 'directions', 'scroll_delay', 'truespeed', 'rtl_text', 'nested']) {
      if (isAllMarqueeScrolling) {
        stopMarqueeFor(id);
      } else {
        startMarqueeFor(id);
      }
    }

    document.getElementById('playPauseAll').innerHTML = isAllMarqueeScrolling ? 'play all' : 'pause all';

    isAllMarqueeScrolling = !isAllMarqueeScrolling;
  }

  function stopMarqueeFor(id) {
    const wrapper = document.getElementById(id);

    wrapper.querySelectorAll('marquee').forEach(m => m.stop());
    wrapper.querySelector('button').innerHTML = 'play';
    wrapper.setAttribute('stop-scrolling', 'yes');
  }

  function startMarqueeFor(id) {
    const wrapper = document.getElementById(id);

    wrapper.querySelectorAll('marquee').forEach(m => m.start());
    wrapper.querySelector('button').innerHTML = 'pause';
    wrapper.removeAttribute('stop-scrolling');
  }

  function toggleMarqueFor(id) {
    const wrapper = document.getElementById(id);

    if (wrapper.hasAttribute('stop-scrolling')) {
      startMarqueeFor(id);
    } else {
      stopMarqueeFor(id);
    }
  }

  window.onload = function(event) {
    const isReduced =
      window.matchMedia(`(prefers-reduced-motion: reduce)`) === true ||
      window.matchMedia(`(prefers-reduced-motion: reduce)`).matches === true;

    if (isReduced) {
      toggleAllMarquees();
      document.getElementById("reduceMotion").innerHTML = "(This post has a bunch of moving text. I’ve stopped it by default because you have ‘reduce motion’ enabled, but you might lose some of the effect. If you’d like to see the animations, you can <button id='playPauseAll' onclick='script:toggleAllMarquees();'>play all</button> or play/pause them manually.)"
    }
  };
</script>
