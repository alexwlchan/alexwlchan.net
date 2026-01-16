---
layout: post
date: 2022-12-21 20:33:41 +00:00
title: Getting an Important Internet Checkmark to follow your cursor
summary: Party like it's 1996! A trailing checkmark cursor will make your Brand Website feel fun and authentic.
tags:
  - fun stuff
  - code crimes
  - javascript
colors:
  css_light: "#0e558b"
  css_dark:  "#55acee"
---

<style>
  .cursor_example {
    height: 300px;
    background: white;
    position: relative;
    max-width: calc(100vw - 2em);
    margin-left:  calc(50% - 50vw + 1em);
    margin-right: calc(50% - 50vw + 1em);
  }

  #regularCursor {
    border: 5px solid transparent;
    border-image: linear-gradient(to bottom right, #0e558b 0%, #1f6aa3 12.5%, #3180bc 25%, #4396d5 37.5%, #55acee 50%, #4396d5 67.5%, #3180bc 75%, #1f6aa3 87.5%, #0e558b 100%);
    border-image-slice: 1;
  }

  #bigCursor {
    border: 5px solid transparent;
    border-image: linear-gradient(to bottom right, #dcaa02 0%, #c59822 12.5%, #af8742 25%, #997662 37.5%, #836501 50%, #997662 67.5%, #af8742 75%, #c59822 87.5%, #dcaa02 100%);
    border-image-slice: 1;
  }

  #unverifiedCursor {
    border: 5px solid transparent;
    border-image: linear-gradient(to bottom right, #83254f 0%, #91296a 12.5%, #9f2d85 25%, #ad31a0 37.5%, #bb3571 50%, #ad31a0 67.5%, #9f2d85 75%, #91296a 87.5%, #83254f 100%);
    border-image-slice: 1;
  }

  .cursor_example .container {
    padding: 1em;
  }

  .cursor_example .container code {
    background: none;
  }
</style>

Are you an Important Brand?
Do you have an Internet Presence?
Do you worry about being Impersonated Or Parodied Online?
Then I may have something for you.

On your social media, you can bask in the warmth of an Important Internet Checkmark which tells your users that they're interacting with your bona fide Brand Ambassadors.

<figure style="width: 548px;">
  {%
    picture
    filename="acme_corporation_delicious.png"
    alt="A social media profile for ACME Corporation with a blue check mark."
    width="548"
    class="screenshot"
  %}
  <figcaption>
    Mmm… that blue checkmark tastes of trust.
  </figcaption>
</figure>

But what if your users click your link in bio, and they go to your corporate website?
How can they be assured that they're looking at your Legitimate Content?

What you need is an Important Internet Checkmark that can follow users to your site, and more precisely follow around their cursor.
That way, they'll always know that whatever they're looking at right now is Authentic Brand Material.
And that's what I can give you today:

<div id="regularCursor" class="cursor_example"></div>

You can customise the size and colour of your checkmark, and even have multiple different checkmarks on the same page.
Maybe you could use a green checkmark to tell them about your commitment to the environment, a purple checkmark to show your support of disabled people, or a gold checkmark to describe your shareholder dividends.
The sky's the limit!

You should make sure to change the meaning of the colours regularly, so your brand stays Fresh and Cutting Edge.

<div id="bigCursor" class="cursor_example"></div>

And it's not just for Big Brands – whether you're running [a parody account on Cohost][cohost] or you're a [millionnaire web marketer][grant], you can get an Anticheckmark so that everyone knows you're Definitely Not Who You Say You Are:

[cohost]: https://cohost.org/staff/post/658118-introducing-cohost
[grant]: https://www.theguardian.com/politics/2015/mar/15/grant-shapps-admits-he-had-second-job-as-millioniare-web-marketer-while-mp

<div id="unverifiedCursor" class="cursor_example"></div>

And what's the price of this Internet Magnificence?
$44 billion and your name dragged through the mud?
$20 a month?
How about $8?

No, this costs the same as all the best ideas: it's Free!

All you have to do is [add some random JavaScript file to your website][js], and if you do that regularly, the carelessness and inevitable security breach will cost you far more than whatever I could charge you for some extra Brand Legitimacy.

[js]: /files/2022/verifiedCursor.js



  ---


Okay, so this is actually a daft idea I had this morning because of all the shenanigans around Twitter Blue and what the different colours of checkmark do or don't mean.
I had the idea in the shower, and I got it working on the train ride into the office.

Most of the heavy lifting is done by Tim Holman's collection of [’90s cursor effects][holman].
I made some small tweaks to his snowflake cursor, swapped out the emoji for an SVG image, and it worked almost immediately.
If you've ever wondered how these effects work, I recommend reading [his source code][code] -- although I've never really used the canvas element or the cursor APIs, I could read his code and understand how it worked.
Thanks Tim!

This was also inspired by Tumblr's [Important Blue Internet Checkmarks][tumblr] and [Cohost Unverified&#8482;][cohost].

If you want to use it, upload [the JavaScript file][js] somewhere and load it in your page like so:

```html
<script src="verifiedCursor.js"></script>

<script>
  window.addEventListener('load', (event) => {
    verifiedCursor({
      // make it bigger or smaller
      size: 2,

      // choose a colour other than blue
      color: '#730192',

      // how fast do you want checkmarks to appear?
      // 0 = none, 1 = lots
      rate: 0.05,

      // do you want to put it inside an element?
      // if you skip this option, it'll cover the page
      element: document.getElementById("verifiedContent"),
    });
  });
</script>
```

You can also call it as `verifiedCursor()` if you just want to use the defaults.

Today was my last working day of the year.
The sensible thing to do would be to avoid deploying any big changes, so nothing breaks over the Christmas holiday.
The silly thing to do would be to add Important Internet Checkmarks to the site, so somebody laughs over the Christmas holiday.
Time will tell if I was sensible or silly…

[holman]: https://tholman.com/cursor-effects/
[code]: https://github.com/tholman/cursor-effects
[tumblr]: https://staff.tumblr.com/post/700564142648606720/hi-were-introducing-completely-useless-blue
[cohost]: https://cohost.org/staff/post/658118-introducing-cohost



<script src="/files/2022/verifiedCursor.js"></script>

<script>
  window.addEventListener('load', (event) => {
    verifiedCursor({
      size: 2,
      rate: 0.5,
      element: document.getElementById("regularCursor"),
    });
    verifiedCursor({
      size: 3,
      color: '#dcaa02',
      rate: 0.05,
      element: document.getElementById("bigCursor"),
    });
    verifiedCursor({
      size: 1.25,
      color: '#0e9201',
      rate: 0.04,
      element: document.getElementById("bigCursor"),
    });
    verifiedCursor({
      size: 2,
      color: '#730192',
      rate: 0.05,
      element: document.getElementById("bigCursor"),
    });
    verifiedCursor({
      size: 1.75,
      color: '#019275',
      rate: 0.05,
      element: document.getElementById("bigCursor"),
    });
    verifiedCursor({
      size: 2.25,
      color: '#b64702',
      rate: 0.02,
      element: document.getElementById("bigCursor"),
    });
    verifiedCursor({
      size: 3.5,
      color: '#000000',
      rate: 0.002,
      element: document.getElementById("bigCursor"),
    });
    verifiedCursor({
      size: 3.5,
      color: '#ffffff',
      rate: 0.002,
      element: document.getElementById("bigCursor"),
    });
    unverifiedCursor({
      size: 2,
      rate: 0.5,
      element: document.getElementById("unverifiedCursor"),
    });
    /* verifiedCursor({ scale: 3, color: '#d01c11' });
    unverifiedCursor({ scale: 2 }); */
  });
</script>
