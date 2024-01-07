---
layout: post
title: The best way to tell a website your age
summary: Using SVG animations to create a fun and exciting new input UI.
tags:
  - code-crimes
  - drawing-things
---
There's a growing number of countries creating laws that require age verification laws to access certain content online.
Now children can be protected from adult content like well-organised spreadsheets, YouTube videos about kitchen appliances, and websites that sell you socks.
These laws are a brilliant idea that will definitely fix everything.

However, there is one point of contention: how should websites ask for your age?

I've been doing research in this area, and inspired by the work of [expert UI designer Tru Narla][trunarla], I've come up with my own proposal.
We all know the best way to tell somebody's age is to count the candles on their birthday cake, so I've built a cake-based interface:

<style type="x-text/scss">
  $width: calc(100vw - 2 * #{$default-padding} - env(safe-area-inset-left) - env(safe-area-inset-right) - 6px);

  #cakeInput {
    width: $width;
    margin-left:  calc(-1 * (#{$width} / 2 - 50%));
    background: #ff00d022;
    border: 3px solid #ff00d0;
    border-radius: 10px;
    text-align: center;
    font-family: 'Comic Sans MS', 'Comic Sans', sans-serif;
    color: #ff00d0;
    padding-bottom: 1em;
    overflow: scroll;

    display: inline-block;

    h1 {
      color: #ff00d0;
    }

    @media screen and (max-width: $max-width + $default-padding * 2) {
      margin-left:  0;
      margin-right: 0;
    }
  }
</style>

<div id="cakeInput">
  <h1>&lt;input type="age"&gt;</h1>

  {%
    inline_svg
    filename="animated-birthday-cake.svg"
  %}

  <p id="age">
  </p>

  <button onclick="script:document.querySelector('svg').pauseAnimations();">
    That’s my age!
  </button>

  <button onclick="script:restartAnimation();">
    Too far, start again!
  </button>
</div>

{%
  inline_svg
  filename="birthday-cake.svg"
%}

[trunarla]: https://www.instagram.com/mewtru/

---

To kick off the new year, Montana and North Carolina joined a growing number of states enforcing laws requiring age verification to access adult content online.



## FAQs

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

---

I think we can all agree that this is a brilliant UI, and now I've explained how it works, I'm sure all the major browsers will implement it immediately.
I look forward to getting my cheques in the post.


---

This is amazing. Not a question, but I appreciate the enthusiasm!

This is an abomination. See above.

DynamoDB isn’t a compute platform, it’s a database. Still not a question. And you’re wrong – it is a compute platform, as this experiment shows.

Why did you do this? Finally, a proper question! Partly for fun, partly as a way to get some practice with the gnarly bits of the DynamoDB API that I forget every time I use.

Can I get all the code you’ve written? Sure, it’s all here:

dynamo_calculator.py
If you want extra fun, turn on your tracing tool of choice (I like the q module) and watch how deep the recursion goes when you divide 36 by 4.

Are there any tests? I’m testing the patience of everyone who works on DynamoDB.

This code has recursion issues. How should I fix those? If you think the biggest issue with this code is that you might hit Python’s recursion limit, I can’t help you.

I like brilliant ideas. What else can you recommend? In this post I’ve talked about using one of Amazon’s compute services; other people have written about their database offerings:

Corey Quinn is a fan of Route 53.
Kevin Kutcha built a URL shortener with Lambda and only Lambda (using Lambda functions to store the URL mappings, naturally). That post was an inspiration for this one.
Can you make it worse better? Almost certainly. if you have suggestions for how to do so, please @ me on Twitter (I’m @alexwlchan).

