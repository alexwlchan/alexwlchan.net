---
layout: post
title: Launching a rocket in the worst possible way
summary: Let's see how we can use the &lt;marquee&gt; tag to fly a spaceship.
tags: code-crimes html
theme:
  card_type: summary_large_image
  image: /images/2022/artemis_launch.jpg
index:
  tint_color: "#382b20"
---

<style>
  .wrapper {
   border: 3px solid #f0f0f0;
   background: black;
   color: white;
   border-radius: 10px;
   text-align: center;
   font-family: Helvetica, Arial, sans-serif;
   position: relative;
   padding: 1em;
  }

  .wrapper p:first-child {
   margin-top: 0;
  }

  .wrapper p:last-child {
   margin-bottom: 0;
  }

  .wrapper button {
   position: absolute;
   right: 5px;
   top: 5px;
   background: white;
   color: black;
   border-radius: 2px;
  }

  #directions marquee {
   height: 100px;
  }

  .marquee_example {
   display: grid;
   grid-gap: 10px;
   margin: 1em;
  }

  .marquee_example code {
   background: none;
  }

  #truespeed {
   grid-template-columns: auto;
  }

  /*
   On wide screens, there's a 2×2 grid of examples with rounded corners
   on the edge of the square.

   On narrow screens, there a 1×4 grid of examples with rounded corners
   at the top and bottom.

   (Or a 2×1 and 1×2)
  */
  .example_2up .wrapper, .example_4up .wrapper {
   width: calc(100% - 2em - 5px);
  }

  .example_2up, .example_4up {
   grid-template-columns: calc(50% - 5px) calc(50% - 5px);
  }

  .example_3up .wrapper:nth-child(1) { border-radius: 10px 10px 0 0; }
  .example_3up .wrapper:nth-child(2) { border-radius: 0; }
  .example_3up .wrapper:nth-child(3) { border-radius: 0 0 10px 10px; }

  .example_4up .wrapper:nth-child(1) { border-radius: 10px 0 0 0; }
  .example_4up .wrapper:nth-child(2) { border-radius: 0 10px 0 0; }
  .example_4up .wrapper:nth-child(4) { border-radius: 0 0 10px 0; }
  .example_4up .wrapper:nth-child(3) { border-radius: 0 0 0 10px; }

  .example_2up .wrapper:nth-child(1) { border-radius: 10px 0 0 10px; }
  .example_2up .wrapper:nth-child(2) { border-radius: 0 10px 10px 0; }

  @media screen and (min-width: 500px) {
   .example_4up .wrapper:nth-child(1) button { display: none; }
   .example_2up .wrapper:nth-child(1) button { display: none; }
  }

  @media screen and (max-width: 500px) {
   .example_2up .wrapper:nth-child(2) button { display: none; }
   .example_4up .wrapper:nth-child(2) button { display: none; }

   .example_4up,
   .example_2up {
     grid-template-columns: auto;
   }

   .example_2up .wrapper,
   .example_4up .wrapper {
     width: calc(100% - 2em);
   }

   .example_4up .wrapper:nth-child(1) { border-radius: 10px 10px 0 0; }
   .example_4up .wrapper:nth-child(2) { border-radius: 0 0 0 0; }
   .example_4up .wrapper:nth-child(3) { border-radius: 0 0 0 0; }
   .example_4up .wrapper:nth-child(4) { border-radius: 0 0 10px 10px; }

   .example_2up .wrapper:nth-child(1) { border-radius: 10px 10px 0 0; }
   .example_2up .wrapper:nth-child(2) { border-radius: 0 0 10px 10px; }
  }
</style>

Last month, NASA made headlines as they (finally) launched their SLS rocket as part of the Artemis 1 mission.
The long and expensive development of SLS has been the subject of much debate, and caused a lot of online rage.
I will now induce similar rage at a fraction of the cost.

NASA's rocket reminded me of [a little website][glitch] I made last year, where you can control a rocket in the browser -- all using web technology from the 1990s.
You can fly in different directions, change speed, and even do a mid-space stop!
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



We can use [the emoji rocket][emoji] which comes with our browser, and which you may have seen elsewhere -- this is a *reusable* rocket.
Very environmentally conscientious!

```html
🚀
```

Now let's make it move.

If you're a hip, modern web developer, you probably know how to make things move on a web page.
Maybe you'd use [CSS animation], or [Motion Path], or break out some [@keyframes].
But as we're constantly told, things were better in the olden days, and that includes web technology.
Old-school web nerds know the best way to move text in a web page: the unjustly-deprecated [marquee tag][marquee].

```html
<marquee>🚀</marquee>
```

If you've never come across it, the marquee tag causes text to scroll across a page.
It makes our rocket move from right to left:

<div id="first_example" class="marquee_example">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('first_example')">pause</button>
    <marquee>🚀</marquee>
  </div>
</div>

But you don't need to be a rocket scientist to realise something's wrong -- it's flying in the wrong direction!
Almost [all rocket emojis][emoji] have the pointy bit in the upper-right, but the marquee tag is taking us to the left.
We need to find a steering wheel.

[emoji]: https://emojipedia.org/rocket/
[mojibake]: https://en.wikipedia.org/wiki/Mojibake
[encoding]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-charset
[CSS animation]: https://developer.mozilla.org/en-US/docs/Web/CSS/animation
[Motion Path]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Motion_Path
[@keyframes]: https://developer.mozilla.org/en-US/docs/Web/CSS/@keyframes
[marquee]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee



  {% separator "marquee-870892.svg" %}



The steering wheel for the marquee tag comes in the form of the [direction attribute][direction], which lets us specify one of the four cardinal directions.

<div id="directions" class="marquee_example example_4up">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('directions')">pause</button>
    <code>&lt;marquee direction="up"&gt;</code>
    <marquee direction="up">🚀</marquee>
  </div>
  <div class="wrapper">
    <button onclick="toggleMarqueFor('directions')">pause</button>
    <code>&lt;marquee direction="right"&gt;</code>
    <marquee direction="right">🚀</marquee>
  </div>
  <div class="wrapper">
    <code>&lt;marquee direction="down"&gt;</code>
    <marquee direction="down">🚀</marquee>
  </div>
  <div class="wrapper">
    <code>&lt;marquee direction="left"&gt;</code>
    <marquee direction="left">🚀</marquee>
  </div>
</div>

We can only pick a single direction; we can't, for example, combine `direction="up left"` to get our rocket to move diagonally.
This is probably for the best, as it avoids an inexperienced operator trying to launch their rocket in the direction `"up down"`, which could go very wrong.

It only supports the four cardinal directions; you can't, for example, combine the attributes .
This is probably for the best, as it avoids somebody like me trying to set `direction="up down"`.

The marquee tag is also aware of non-English languages -- it scrolls from right-to-left in my posts, but if you specify a [right-to-left script][rtl] with [the dir attribute][dir], it scrolls from left-to-right (opposite to the direction of the text).

<div id="rtl_text" class="marquee_example example_2up">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('rtl_text')">pause</button>
    <code>&lt;marquee dir="ltr"&gt;</code>
    <marquee dir="ltr">🚀 English rocket 🚀</marquee>
  </div>
  <div class="wrapper">
    <button onclick="toggleMarqueFor('rtl_text')">pause</button>
    <code>&lt;marquee dir="rtl"&gt;</code>
    <marquee dir="rtl">🚀
بھارتی راکٹ 🚀</marquee>
  </div>
</div>

This is good news for international relations: now everyone can build rockets!

But it's still a bit… slow.
Space is big.
[Vastly, hugely, mind-bogglingly big.][big]
If a rocket is going to get across space, it has to be moving incredibly quickly.
Can we go faster?

[direction]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#attr-direction
[rtl]: https://en.wikipedia.org/wiki/Right-to-left_script
[dir]: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/dir
[big]: https://www.goodreads.com/quotes/14434-space-is-big-you-just-won-t-believe-how-vastly-hugely



  {% separator "marquee-870892.svg" %}



Text in the marquee tag doesn't scroll as continuous motion; instead it gets updated at discrete intervals.
The time between intervals is controlled by the [scrolldelay attribute][scrolldelay] (which counts in milliseconds), and if we crank it up the discrete motion becomes obvious:

<div id="scrolldelay" class="marquee_example example_2up">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('scrolldelay')">pause</button>
    <code>&lt;marquee scrolldelay="1000"&gt; (1s)</code>
    <marquee scrolldelay="500">🚀</marquee>
  </div>
  <div class="wrapper">
    <button onclick="toggleMarqueFor('scrolldelay')">pause</button>
    <code>&lt;marquee scrolldelay="5000"&gt; (5s)</code>
    <marquee scrolldelay="5000">🚀</marquee>
  </div>
</div>

The default value is 85&nbsp;milliseconds, which is about 12&nbsp;fps.
I wonder if this is a limitation of graphics cards in the 1990s, and an attempt to reduce the number of times web pages had to be redrawn -- the marquee tag was originally introduced in IE3, when computers were much less powerful.
(Alternatively, maybe it's some form of short-range teleport-based propulsion.)

If you want to crank down the interval below 60&nbsp;milliseconds, you have to add the [truespeed attribute][truespeed].
That feels like another sign that maybe this is designed to avoid over-taxing the computer, by clamping the refresh rate unless you explicitly opt in.

<div id="truespeed" class="marquee_example example_3up">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('truespeed')">pause</button>
    <code>&lt;marquee scrolldelay="60"&gt;</code>
    <marquee scrolldelay="60">🚀</marquee>
  </div>
  <div class="wrapper">
    <code>&lt;marquee scrolldelay="1"&gt;</code>
    <marquee scrolldelay="1">🚀</marquee>
  </div>
  <div class="wrapper">
    <code>&lt;marquee scrolldelay="1" truespeed&gt;</code>
    <marquee scrolldelay="1" truespeed>🚀</marquee>
  </div>
</div>

If you want to change the distance the text scrolls at each interval, you can set the [scrollamount attribute][scrollamount].
This doesn't seem to have any limits.

<div id="scrollamount" class="marquee_example example_3up">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('scrollamount')">pause</button>
    <code>&lt;marquee scrollamount="6"&gt;</code> (default)
    <marquee scrollamount="6">🚀</marquee>
  </div>
  <div class="wrapper">
    <code>&lt;marquee scrollamount="12"&gt;</code>
    <marquee scrollamount="12">🚀</marquee>
  </div>
  <div class="wrapper">
    <code>&lt;marquee scrollamount="24"&gt;</code>
    <marquee scrollamount="24">🚀</marquee>
  </div>
</div>


Although there aren't any defined limits, you may want to be careful.

If you really crank up the scrollamount, you can get some weird visual effects -- the text might get stuck in place, or it might not be visible at all.
In my browser (Safari), the rocket below just flips between two positions, offset 300 and 600 pixels from the right-hand side.
If I shrink my window to less than 300 pixels wide, it disappears entirely.
It reminds me of the [wagon-wheel effect][wagon].

<div id="wagonwheel" class="marquee_example">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('wagonwheel')">pause</button>
    <code>&lt;marquee scrollamount="300"&gt;</code>
    <marquee scrollamount="300">🚀</marquee>
  </div>
</div>

So now we can make our rocket go as fast as we like -- but what if we need to stop suddenly?

Maybe [our advanced autopilot][robert] has spotted a parked spaceship, there's an asteroid up ahead, or an astronaut ran out into the space road.
Can we give our autopilot a handbrake?

[scrolldelay]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#attr-scrolldelay
[truespeed]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#attr-truespeed
[scrollamount]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#attr-scrollamount
[wagon]: https://en.wikipedia.org/wiki/Wagon-wheel_effect
[robert]: http://www.robots-and-androids.com/robert-the-robot.html



  {% separator "marquee-870892.svg" %}



Initially I considered building a brake that modifies the scrollamount attribute -- if we reduce it to 0, the rocket will stop moving.
You have to save the original scrollamount value somewhere, and restore it when you want to restart, but that's doable.

When I re-read the MDN docs, I discovered the marquee tag has [stop() and start() methods][start_stop], which will stop and start the scrolling.
That feels a bit nicer than fiddling with attributes, and they're what I'm using for the play/pause buttons on the examples in this post.

What I couldn't find is any way to determine if a marquee element is currently scrolling -- to build a play/pause toggle, you have to track the state of the scrolling in an external variable.

This gives us a basic start/stop, but what if we want more advanced controls?
What if we want to change the speed or direction mid-flight?
How do we introduce more interactivity?

[start_stop]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#methods



  {% separator "marquee-870892.svg" %}



If I've learnt anything from watching Star Trek, it's that the best interfaces have buttons.
(Preferably physical ones.)
We should build a panel of buttons to control our rocket.
And of course, there's a very convenient way to create buttons on the web.
Do you know what it is?

That's right, it's the marquee tag.

If we set `scrollamount="0"` on a marquee tag, we get a static element.
We can make our button do something by defining an `onclick` handler, and then we can position it like any HTML element.
For example:

```html
<marquee
  scrollamount="0"
  style="background: white; width: 45px; height: 45px; cursor: hand;"
  onclick="
    rocket = document.getElementById('rocket');
    if (rocket.attributes['is-moving'] === 'no') {
      rocket.start();
      rocket.attributes['is-moving'] = 'yes';
    } else {
      rocket.stop();
      rocket.attributes['is-moving'] = 'no';
    };">
  ⏯
</marquee>
```

Once I had this trick in mind, I was able to construct a panel of buttons to control the rocket:

<style>
  #buttons {
    display: grid;
    grid-template-columns: auto auto;
    grid-gap: 10px;
    margin: 1em;
  }

  @media screen and (max-width: 500px) {
    #buttons {
      margin-left:  0;
      margin-right: 0;
    }
  }

  #buttons picture:nth-child(1) img {
    width: 100%;
    object-fit: cover;
    aspect-ratio: 1 / 1;
    border-top-right-radius:    0;
    border-bottom-right-radius: 0;
  }

  #buttons picture:nth-child(2) img {
    width: 100%;
    object-fit: cover;
    aspect-ratio: 1 / 1;
    border-top-left-radius:    0;
    border-bottom-left-radius: 0;
  }
</style>

<figure id="buttons">
  <picture>
    <source
      srcset="/images/2022/tos_buttons_1x.webp 1x,
              /images/2022/tos_buttons_2x.webp 2x,
              /images/2022/tos_buttons_3x.webp 3x,
              /images/2022/tos_buttons_4x.webp 4x"
      type="image/webp"
    >
    <source
      srcset="/images/2022/tos_buttons_1x.jpg 1x,
              /images/2022/tos_buttons_2x.jpg 2x,
              /images/2022/tos_buttons_3x.jpg 3x,
              /images/2022/tos_buttons_4x.jpg 4x"
      type="image/jpeg"
    >
    <img
      src="/images/2022/tos_buttons_1x.jpg"
      class="screenshot"
    >
  </picture>
  <picture>
    <img
      src="/images/2022/marquee_buttons.png"
      class="screenshot"
    >
  </picture>
</figure>



These buttons work by modifying the various direction/speed attributes on the marquee element, and calling the start()/stop() method for play/pause.

This is where you really see the differences in browser support.
In Safari, clicking these buttons will change direction immediately -- the rocket can zigzag across the page.
In Chrome, clicking these buttons won't take effect until it scrolls off the edge of the window.
In Firefox, clicking these buttons take effect immediately, but it restarts the scroll from the edge of the window.

The speed controls are similarly inconsistent -- in Firefox and Safari, the speed changes immediately, but in Chrome it waits for the next cycle.

<!-- The marquee tag has been deprecated for years, and even when it was supported there were probably only a handful of sites that were dynamically changing the direction or speed.
It's unsurprising, if disappointing, that a consensus has failed to emerge. -->



  {% separator "marquee-870892.svg" %}



These buttons control a single rocket, but advanced rockets have [multiple stages][stages].
While I was writing this blog post, I discovered that we can also do multistage rockets with the marquee tag -- by nesting tags inside each other.

```html
<marquee>
  🚀 first
  <marquee>
    🚀 second
    <marquee>🚀 third stage 🚀</marquee>
    stage 🚀
  </marquee>
  stage 🚀
</marquee>
```

This looks about as good as you'd expect, and different browsers render it differently:

<div id="nested">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('nested')">pause</button>
    <marquee style="color: #ef4239;">
      🚀 first
      <marquee style="color: #d0c611;">
        🚀 second
        <marquee style="color: #1196d0;">🚀 third stage 🚀</marquee>
        stage 🚀
      </marquee>
      stage 🚀
    </marquee>
  </div>
</div>

I learnt this when I screwed up the escaping in my Markdown source file, and got an HTML file with half a dozen unclosed &lt;marquee&gt;> tags.
I was struck by the complete visual mess that stood before me.
The possibilities are as endless as they are horrifying.

[stages]: https://en.wikipedia.org/wiki/Multistage_rocket



  {% separator "marquee-870892.svg" %}



## Why are you doing this?

This all started when Laurie Voss ran an [&lt;Angle&gt; Bracket tournament][tournament], a series of Twitter polls to determine the Internet's favourite HTML tag.
I was following [Danielle Leong][leong], who was a fearless cheerleader of the marquee tag, and I discovered the tournament through her tweets.

The four finalists were &lt;a&gt;, &lt;div&gt;, &lt;marquee&gt; and &lt;script&gt;, and Laurie tweeted what could only be read as a challenge:

{% tweet https://twitter.com/seldo/status/1461848209769197573 %}

How far could I get with just &lt;marquee&gt;?

I built the [&lt;marquee&gt; rocket][glitch] as a small website with a bit of interactivity that only uses the marquee tag -- and to prove that you don't need &lt;script&gt; to use JavaScript.

It was a useful reminder that HTML is enormous, and I only know a tiny fraction of it.
I'd been aware of the marquee tag for over a decade, but I thought it was just for horizontally scrolling text.
I didn't know about any of these attributes or methods -- so how much stuff am I missing on the bits of HTML I do use on a day-to-day basis?

And although I'm never going to use my newfound knowledge of the marquee tag, I did learn some things which might actually be useful in a real project – including the right-to-left script modifier, and some stuff around the "reduce motion" accessibility settings which I'm using in this post.

I'll end with a final example, which brings together all our new marquee knowledge:

<div id="to_the_moon" class="marquee_example">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('to_the_moon')">pause</button>
    <code>&lt;marquee direction="right" scrollamount="80" scrolldelay="1" truespeed&gt;</code><br/>
    <span style="float: left;">🌍</span>
    <marquee scrollamount="80" scrolldelay="1" truespeed direction="right">🚀</marquee>
    <span style="float: right;">🌕</span>
  </div>
</div>

My iMac's display is 218&nbsp;pixels per inch, which means that [if I set this tiny rocket now][wolfram], I'll beat NASA back to the Moon.
With a week to spare.

[tournament]: https://theanglebracket.com
[leong]: https://twitter.com/tsunamino/status/1461429962708193280
[wolfram]: https://www.wolframalpha.com/input?i=%28%28distance+from+earth+to+moon%29+%2F+%28%2880+pixels+%2F+1+milliseconds%29+%2F+%28218+pixels+per+inch%29%29%29

<script>
  var isAllMarqueeScrolling = true;

  function toggleAllMarquees() {
    document.querySelectorAll('.marquee_example').forEach(elem => {
      if (isAllMarqueeScrolling) {
        stopMarqueeFor(elem);
      } else {
        startMarqueeFor(elem);
      }
    });

    document.getElementById('playPauseAll').innerHTML = isAllMarqueeScrolling ? 'play all' : 'pause all';

    isAllMarqueeScrolling = !isAllMarqueeScrolling;
  }

  function stopMarqueeFor(elem) {
    elem.querySelectorAll('marquee').forEach(m => m.stop());
    elem.querySelectorAll('button').forEach(b => b.innerHTML = 'play');
    elem.setAttribute('stop-scrolling', 'yes');
  }

  function startMarqueeFor(elem) {
    elem.querySelectorAll('marquee').forEach(m => m.start());
    elem.querySelectorAll('button').forEach(b => b.innerHTML = 'pause');
    elem.removeAttribute('stop-scrolling');
  }

  function toggleMarqueFor(id) {
    const elem = document.getElementById(id);

    if (elem.hasAttribute('stop-scrolling')) {
      startMarqueeFor(elem);
    } else {
      stopMarqueeFor(elem);
    }
  }

  window.onload = function(event) {
    const isReduced =
      window.matchMedia(`(prefers-reduced-motion: reduce)`) === true ||
      window.matchMedia(`(prefers-reduced-motion: reduce)`).matches === true;

    if (isReduced) {
      toggleAllMarquees();
      document.getElementById("reduceMotion").innerHTML = "<strong>Accessibility note:</strong> this post has a lot of moving text and images. I’ve stopped it by default because you have the ‘reduce motion’ setting, but you might lose some of the effect. If you’d like to see the animations, you can <button id='playPauseAll' onclick='script:toggleAllMarquees();'>play all</button> or play/pause them manually.)"
    }
  };
</script>
