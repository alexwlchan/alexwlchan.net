---
layout: post
date: 2022-12-16 10:01:11 +0000
title: Launching a rocket in the worst possible way
summary: Taking the humble &lt;marquee&gt; tag where no HTML tag has gone before.
tags:
  - code crimes
  - html
  - fun stuff
colors:
  index_light: "#ba4220"
  index_dark:  "#eb7028"
index:
  feature: true
---

<!-- Cover image:
  https://thenounproject.com/icon/marquee-870892/
  https://thenounproject.com/icon/rocket-1050360/
  https://wellcomecollection.org/works/vzkap9dq/images?id=gd3spdt2
 -->

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

  @media (prefers-color-scheme: dark) {
    .wrapper {
      border-color: #3f3f3f;
    }
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

NASA's rocket reminded me of [a little website][rocket] I made last year, where you can control a rocket in the browser -- all using web technology from the 1990s.
You can fly in different directions, change speed, and even do a mid-space stop!
In this post, we'll peek under the covers and see how it works.

{%
  picture
  filename="marquee_rocket.png"
  alt="A web page with a rocket icon on a black background. On the left-hand side are a series of buttons labelled 'direction' and 'speed' which control the rocket."
  class="screenshot"
  width="582"
%}

<p id="reduceMotion">
  <strong>Accessibility note:</strong> this post has a lot of moving text and images.
  If you find that distracting, you can <button id='playPauseAll' onclick='script:toggleAllMarquees();'>pause all</button> or play/pause the individual examples.
</p>

[shuttle]: https://www.space.com/artemis-1-space-shuttle-hardware
[rocket]: /fun-stuff/marquee-rocket/



  ---



We can use [the emoji rocket][emoji] which comes with our browser, and which you may have seen elsewhere -- this is a *reusable* rocket.
Very environmentally conscientious!

```html
🚀
```

Now let's make it fly.

If you're a hip, modern web developer, you probably know how to make things move on a web page.
Maybe you'd use [CSS animation], or [Motion Path], or break out some [@keyframes].
But as we're constantly told, things were better in the olden days, and that includes web technology.
Old-school web nerds know the best way to move text in a web page: the unjustly-deprecated [marquee tag][marquee].

```html
<marquee>🚀</marquee>
```

If you've never come across it, the marquee tag causes text to scroll across a page.
It makes our rocket move from right to left:

<div id="first_example" class="marquee_example indented">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('first_example')">pause</button>
    <marquee>🚀</marquee>
  </div>
</div>

This looks pretty good already!

But you don't need to be a rocket scientist to realise something's wrong -- we're flying backwards!
Almost [all rocket emojis][emoji] have the pointy bit in the upper-right, but the marquee tag is taking us to the left.
We need to find a steering wheel.

[emoji]: https://emojipedia.org/rocket/
[mojibake]: https://en.wikipedia.org/wiki/Mojibake
[encoding]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-charset
[CSS animation]: https://developer.mozilla.org/en-US/docs/Web/CSS/animation
[Motion Path]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Motion_Path
[@keyframes]: https://developer.mozilla.org/en-US/docs/Web/CSS/@keyframes
[marquee]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee



  ---



You can steer a marquee tag with the [direction attribute][direction], which lets you pick one of four directions.
The scroll will go in whatever direction you pick:

<div id="directions" class="marquee_example indented example_4up">
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

The marquee tag is also aware of non-English languages -- it scrolls from right-to-left in my posts, but if you specify a [right-to-left script][rtl] with the [dir attribute][dir], it scrolls from left-to-right (opposite to the direction of the text).

<div id="rtl_text" class="marquee_example indented example_2up">
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

This is good news for international relations: everyone can build rockets!

But it's still a bit… slow.
Space is big.
[Vastly, hugely, mind-bogglingly big.][big]
If a rocket is going to get across space, it has to be moving incredibly quickly.
Can we go faster?

[direction]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#attr-direction
[rtl]: https://en.wikipedia.org/wiki/Right-to-left_script
[dir]: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/dir
[big]: https://www.goodreads.com/quotes/14434-space-is-big-you-just-won-t-believe-how-vastly-hugely



  ---



Text in the marquee tag doesn't scroll as continuous motion; instead it gets updated at discrete intervals.
The time between intervals is controlled by the [scrolldelay attribute][scrolldelay] (which counts in milliseconds), and if we crank it up the discrete motion becomes more obvious:

<div id="scrolldelay" class="marquee_example indented example_2up">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('scrolldelay')">pause</button>
    <code>&lt;marquee scrolldelay="1000"&gt; (1s)</code>
    <marquee scrolldelay="500" scrollamount="9">🚀</marquee>
  </div>
  <div class="wrapper">
    <button onclick="toggleMarqueFor('scrolldelay')">pause</button>
    <code>&lt;marquee scrolldelay="5000"&gt; (5s)</code>
    <marquee scrolldelay="5000" scrollamount="9">🚀</marquee>
  </div>
</div>

The default value is 85&nbsp;milliseconds, which is about 12&nbsp;fps.
I wonder if this is a limitation of graphics cards in the 1990s, and an attempt to reduce the number of times web pages had to be redrawn -- the marquee tag was originally introduced in IE3, when computers were much less powerful.
(Alternatively, maybe it's some form of short-range teleport-based propulsion.)

If you want to crank down the interval below 60&nbsp;milliseconds, you have to add the [truespeed attribute][truespeed].
That feels like another sign that maybe this is designed to avoid over-taxing the computer, by clamping the refresh rate unless you explicitly opt in.
Notice that `scrolldelay="1"` makes no difference until I add this attribute:

<div id="truespeed" class="marquee_example indented example_3up">
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

If you want to change how far the text scrolls at each interval, use the [scrollamount attribute][scrollamount].

<div id="scrollamount" class="marquee_example indented example_3up">
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


Although this doesn't seem to have any limits, you may want to be careful.

If you really crank up the scrollamount, you can get some weird visual effects -- the text might get stuck in place, or it might not be visible at all.
In my browser (Safari), the rocket below just flips between two positions, offset 300 and 600 pixels from the right-hand side.
If I shrink my window to less than 300 pixels wide, it disappears entirely.
It reminds me of the [wagon-wheel effect][wagon].

<div id="wagonwheel" class="marquee_example indented">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('wagonwheel')">pause</button>
    <code>&lt;marquee scrollamount="300"&gt;</code>
    <marquee scrollamount="300">🚀</marquee>
  </div>
</div>

So now we can launch our rocket, set a direction and pick a speed -- and then we'll keep going that way, that speed, forever.

What if we need to change course?
Maybe [our advanced autopilot][robert] has spotted a parked spaceship, there's an asteroid up ahead, or an astronaut ran out into the road.
Can we get some controls?

[scrolldelay]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#attr-scrolldelay
[truespeed]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#attr-truespeed
[scrollamount]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#attr-scrollamount
[wagon]: https://en.wikipedia.org/wiki/Wagon-wheel_effect
[robert]: http://www.robots-and-androids.com/robert-the-robot.html



  ---



If I've learnt anything from watching Star Trek, it's that all the best interfaces have buttons, preferably physical ones.
We should design a panel of buttons that control our rocket.
And of course, lots of people need buttons on the web, so there's an HTML tag you can use for making buttons.
Can you guess what it is?

That's right, it's the marquee tag.

We can set `scrollamount="0"`, which makes it static, so it moves like a button.
We can add a `style` to can change its appearance, so it looks like a button.
And we can define an `onclick` handler to make it do something when the user clicks, so it behaves like a button.

Here's an example:

```html
<marquee
  id="up"
  scrollamount="0"
  style="background: white; width: 35px; height: 44px; cursor: hand;"
  onclick="document.getElementById('rocket').direction = 'up';"
>
  ↑
</marquee>
```

Once I had this brilliant idea, I was able to construct a panel of buttons to control the rocket:

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

<!-- TODO: Fix this properly with a grid -->

<figure id="buttons">
  {%
    picture
    filename="tos_buttons_fixed.jpg"
    alt="Two panels of coloured lights and buttons on a spaceship console. We can see somebody in a gold uniform reaching out to push the buttons."
    class="screenshot"
    width="350"
  %}
  {%
    picture
    filename="marquee_buttons.png"
    alt="Buttons on a web page. There are four arrows labelled 'direction' arranged in a T-shape, like a keyboard, then three buttons labelled 'speed' for play/pause, go slower, and go faster."
    class="screenshot"
    width="350"
  %}
</figure>

The `onclick` handlers for direction and speed are finding the scrolling element, then modifying the various direction/speed attributes we've discussed above.

I'm arranging the buttons into a grid with `position: absolute;` and fixed margins, which mean they'll always be in the same place.
Muscle memory for buttons is very useful!

The play/pause button uses two handy methods on the marquee tag: [stop() and start()][start_stop], which will stop and start the scrolling.
I'm slightly perturbed that there's no way to determine if a marquee is currently scrolling; I have to store that state in an external variable -- but it seems to work.

These controls are where you really see the differences in browser support.
The direction and speed controls behave differently across browsers.
In some browsers, they take immediate effect, in others you have to wait for the current scroll to complete before you see any change.

The marquee tag has been deprecated for years, and even when it was supported there were probably only a handful of sites that were dynamically changing the direction or speed.
It's unsurprising, if disappointing, that a consensus has failed to emerge.

[start_stop]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/marquee#methods



  ---



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

This looks about as good as you'd expect:

<div id="nested" class="marquee_example indented">
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

Different browsers render this even more differently, so you may see something completely different to me.

I learnt this when I screwed up the escaping in a draft of this post, and got an HTML file with half a dozen unclosed &lt;marquee&gt; tags.
I was struck by the complete visual mess that stood before me.
The possibilities are as endless as they are horrifying.

[stages]: https://en.wikipedia.org/wiki/Multistage_rocket



  ---



## Why are you doing this?

This all started when Laurie Voss ran an [&lt;Angle&gt; Bracket tournament][tournament], a series of Twitter polls to determine the Internet's favourite HTML tag.
I was following [Danielle Leong][leong], who was a fearless cheerleader of the marquee tag, and I discovered the tournament through her tweets.

The four finalists were &lt;a&gt;, &lt;div&gt;, &lt;marquee&gt; and &lt;script&gt;, and Laurie tweeted what could only be read as a challenge:

{% tweet https://twitter.com/seldo/status/1461848209769197573 %}

How far could I get with just &lt;marquee&gt;?

I built the [&lt;marquee&gt; rocket](/fun-stuff/marquee-rocket/) as a small website with a bit of interactivity that only uses the marquee tag -- and to prove that you don't need &lt;script&gt; to do JavaScript shenanigans.

It was a useful reminder that HTML is enormous, and I only know a tiny fraction of it.
I'd been aware of the marquee tag for over a decade, but I thought it was just for horizontally scrolling text.
I didn't know about any of these attributes or methods -- so how much stuff am I missing on the bits of HTML I actually use on a day-to-day basis?

And although I'm never going to use my newfound knowledge of the marquee tag, I did learn some things which might actually be useful in a real project – including the right-to-left script modifier, and some stuff around the "reduce motion" accessibility settings which I'm using in this post.

I'll end with a final example, which brings together all our new marquee knowledge:

<div id="to_the_moon" class="marquee_example indented">
  <div class="wrapper">
    <button onclick="toggleMarqueFor('to_the_moon')">pause</button>
    <code>&lt;marquee direction="right" scrollamount="1" scrolldelay="30" truespeed&gt;</code><br/>
    <span style="float: left;">🌍</span>
    <marquee
      scrollamount="1"
      scrolldelay="30"
      truespeed
      direction="right"
      style="margin-left: 25px; margin-right: 25px;"
    >
      🚀
    </marquee>
    <span style="float: right;">🌕</span>
  </div>
</div>

NASA aren't the only ones who can send a rocket to the Moon.

[tournament]: https://theanglebracket.com
[leong]: https://twitter.com/tsunamino/status/1461429962708193280

<script>
  var isAllMarqueeScrolling = true;

  function toggleAllMarquees() {
    document.querySelectorAll('.marquee_example').forEach(elem => {
      if (isAllMarqueeScrolling) {
        stopMarqueeFor(elem);
        return;
      } else {
        startMarqueeFor(elem);
        return;
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
      return;
    } else {
      stopMarqueeFor(elem);
      return;
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
