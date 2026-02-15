---
layout: page
title: ""
colors:
  css_light: "#098a07"
  css_dark:  "#5ff042"
old_syntax_highlighting: true
---

<style type="x-text/scss">
  @use "components/article_cards";
  
  hr {
    height: 50px;
    width:  50px;

    --hr-background-image: url("data:image/svg+xml;charset=UTF-8,<svg xmlns=%22http://www.w3.org/2000/svg%22 x=%220px%22 y=%220px%22 viewBox=%220 0 98 98%22 width=%2250px%22><path fill=\%22%2317823e33\%22 d=%22M30.636,61.596c-1.006,1.497-1.859,2.997-2.56,4.5c-3.046,6.531-3.178,13.179-0.396,19.941  c0.536,1.304-0.087,2.797-1.391,3.333c-1.305,0.536-2.797-0.087-3.333-1.391c-3.354-8.155-3.195-16.171,0.476-24.045  c3.45-7.397,10.028-14.608,19.732-21.633c2.324-1.893,4.818-3.785,7.483-5.678c1.069-0.759,1.321-2.241,0.562-3.31  c-0.759-1.069-2.241-1.321-3.31-0.561C37.653,40.026,29.77,47.454,24.243,55.01c-2.331-13.176-0.587-23.597,5.221-31.032  c8.019-10.267,24.155-15.49,47.983-15.54c-0.048,23.828-5.272,39.965-15.538,47.984C54.43,62.264,43.927,63.992,30.636,61.596z%22/></svg>");

    @media (prefers-color-scheme: dark) {
      --hr-background-image: url("data:image/svg+xml;charset=UTF-8,<svg xmlns=%22http://www.w3.org/2000/svg%22 x=%220px%22 y=%220px%22 viewBox=%220 0 98 98%22 width=%2250px%22><path fill=\%22%2326d96799\%22 d=%22M30.636,61.596c-1.006,1.497-1.859,2.997-2.56,4.5c-3.046,6.531-3.178,13.179-0.396,19.941  c0.536,1.304-0.087,2.797-1.391,3.333c-1.305,0.536-2.797-0.087-3.333-1.391c-3.354-8.155-3.195-16.171,0.476-24.045  c3.45-7.397,10.028-14.608,19.732-21.633c2.324-1.893,4.818-3.785,7.483-5.678c1.069-0.759,1.321-2.241,0.562-3.31  c-0.759-1.069-2.241-1.321-3.31-0.561C37.653,40.026,29.77,47.454,24.243,55.01c-2.331-13.176-0.587-23.597,5.221-31.032  c8.019-10.267,24.155-15.49,47.983-15.54c-0.048,23.828-5.272,39.965-15.538,47.984C54.43,62.264,43.927,63.992,30.636,61.596z%22/></svg>");
    }
  }

  img#headshot {
    border-radius: 50%;
    margin-left:   var(--default-padding);
    margin-bottom: var(--default-padding);
  }

  @media screen and (min-width: 500px) {
    main {
      padding-top: calc(1.5 * var(--default-padding));
    }

    img#headshot {
      margin-top: -3em;
      float: right;
    }
  }

  @media screen and (max-width: 500px) {
    img#headshot {
      display: block;
      margin-top: var(--default-padding);
      margin-left:  auto;
      margin-right: auto;
    }
  }

  #popular_tags a {
    white-space: nowrap;
  }
</style>

**Hi, I’m Alex. Welcome to my website!**

{%
  picture
  filename="profile_green_sq.jpg"
  id="headshot"
  parent="/images"
  width="230"
  alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants."
  class="rounded_corners"
%}

I'm a software developer, writer, and a hand crafter, and I live in the UK.
In my day job I build software for digital preservation, and I think a lot about archiving and long-term systems.

This website is where I share stuff I find interesting or fun.
That includes notes on technical problems I've solved, personal reflections or thoughts, and fun toys that I've built.

I'm queer and trans, and my pronouns are "they" or "she".

I hope you like it!

<br/>

<style>
  #homepage_cards {
    list-style-type: "";
    padding: 0;
    margin: 0;
    
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--grid-gap);
  }
  
  @media screen and (max-width: 450px) {
    #homepage_cards {
      grid-template-columns: auto;
    }
  }

  @media screen and (min-width: 1000px) {
    #homepage_cards {
      --grid-columns: repeat(3, minmax(0, 1fr));
      margin-left:  -100px;
      margin-right: -100px;

      /* In Safari 18.2, the <ul> won't automatically expand to the width
       * just because the margin is there -- we have to tell it to expand */
  
      /* Why 199px and not 200px? To work around a subpixel bug in WebKit,
       * where I get a hairline crack on the right-hand side of my cards
       * in the three column view. :( */
      width: calc(100% + 199px);
    }
  }
  
  .card {
    border: var(--border-width) var(--border-style) var(--primary-color);
    border-radius: var(--border-radius);
    background-color: var(--background-color);
    
    h2 {
      margin: 0;
      padding: 10px;
      background: var(--card-bg) var(--primary-color);
      background-size: auto 125%;
      color: white;
      text-align: center;
      border-radius: calc(var(--border-radius) - 3px) calc(var(--border-radius) - 3px) 0 0;
    }
    
    ul {
      list-style-type: "";
      padding: var(--default-padding);
      margin-top: 0;
      margin-left: 0;
    
      li {
        text-wrap: balance;
        display: grid;
        grid-template-columns: 24px auto;
        gap: 7px;
        margin-top: 6px;
      }
      
      a {
        color: var(--primary-color);
      }
      
      svg {
        margin-top: 2px;
        margin-left: 0;
        margin-right: auto;
      }
    }
  }
  
  #writing {
    --primary-color: var(--red);
    --card-bg:       url('/h/d01c11.png');
  }
  
  #life {
    --primary-color: var(--green);
    --card-bg:       url('/h/118207.png');
  }
  
  #archives {
    --primary-color: var(--blue);
    --card-bg:       url('/h/115bda.png');
  }
  
  @media screen and (prefers-color-scheme: dark) {
    #homepage_cards h2 {
      color: black;
    }
    
    #writing {
      --card-bg: url('/h/ff4a4a.png');
    }
  
    #life {
      --card-bg: url('/h/5ff042.png');
    }
  
    #archives {
      --card-bg: url('/h/40c3ff.png');
    }
  }
  </style>
  
  <style>
    path, ellipse {
      stroke: currentColor;
      stroke-linecap: round;
      fill: none;
    }
    
    .border {
      stroke-width: 2;
    }
    
    circle.dot {
      fill: currentColor;
      stroke: none;
    }
    
    g[data-value="1"] {
      .upper, .lower, .mid { display: none; }
      .mid.center { display: block; }
    }

    g[data-value="2"][data-alt="false"] {
      .upper, .lower, .mid { display: none; }
      .upper.left, .lower.right { display: block; }
    }
    g[data-value="2"][data-alt="true"] {
      .upper, .lower, .mid { display: none; }
      .upper.right, .lower.left { display: block; }
    }
    
    g[data-value="3"][data-alt="false"] {
      .upper, .lower, .mid { display: none; }
      .upper.right, .mid.center, .lower.left { display: block; }
    }
    g[data-value="3"][data-alt="true"] {
      .upper, .lower, .mid { display: none; }
      .upper.left, .mid.center, .lower.right { display: block; }
    }

    g[data-value="4"] {
      .center, .mid { display: none; }
    }

    g[data-value="5"] {
      .center, .mid { display: none; }
      .mid.center { display: block; }
    }

    g[data-value="6"][data-alt="false"] {
      .center { display: none; }
    }
    g[data-value="6"][data-alt="true"] {
      .mid { display: none; }
    }

    .dot {
      stroke: none;
      fill: currentColor;
    }
    
    #die_outline {
      stroke: currentColor;
      stroke-linecap: round;
      fill: none;
    }
  </style>
</style>

<ul id="homepage_cards">
  <li id="writing" class="card">
    <h2>My writing</h2>
    <ul>
      <li>
        {% inline_svg filename="icons/programming.svg" class="dark_aware" %}
        <span>
          <a href="/systems/">Systems and software</a>
        </span>
      </li>
      <li>
        {% inline_svg filename="icons/floppy_disk.svg" class="dark_aware" %}
        <span>
          <a href="/digital-preservation/">Digital preservation</a> and <a href="/digital-preservation/tiny-archives/">Tiny archives</a>
        </span>
      </li>
      <li>
        {% inline_svg filename="icons/lightbulb.svg" class="dark_aware" %}
        <a href="/personal-thoughts/">Personal thoughts</a>
      </li>
      <li>
        {% inline_svg filename="icons/pencil.svg" class="dark_aware" %}
        <a href="/art/">Art and creativity</a>
      </li>
      <li>
        {% inline_svg filename="icons/map_pin.svg" class="dark_aware" %}
        <a href="/world/">The world around us</a>
      </li>
    </ul>
  </li>
  <li id="life" class="card">
    <h2>My life</h2>
    <ul>
      <li>
        {% inline_svg filename="icons/id_card.svg" class="dark_aware" %}
        <a href="/about-me/">About me</a>
      </li>
      <li>
        {% inline_svg filename="icons/layers.svg" class="dark_aware" %}
        <a href="/about-the-site/">About the site</a>
      </li>
      <li>
        {% inline_svg filename="icons/office.svg" class="dark_aware" %}
        <a href="/day-job/">My day job</a>
      </li>
      <li>
        {% inline_svg filename="icons/branch.svg" class="dark_aware" %}
        <a href="/license/">Using my code</a>
      </li>
      <li>
        {% inline_svg filename="icons/heart.svg" class="dark_aware" %}
        <a href="/say-thanks/">Say thanks</a>
      </li>
      <li>
        {% inline_svg filename="icons/envelope.svg" class="dark_aware" %}
        <a href="/contact/">Contact me</a>
      </li>
    </ul>
  </li>
  <li id="archives" class="card">
    <h2>My archives</h2>
    <ul>
      <li>
        {% inline_svg filename="icons/microphone.svg" class="dark_aware" %}
        <a href="/talks/">Talks I’ve given</a>
      </li>
      <li>
        {% inline_svg filename="icons/book.svg" class="dark_aware" %}
        <a href="/book-reviews/">Books I’ve read</a>
      </li>
      <li>
        {% inline_svg filename="icons/dice.svg" class="dark_aware" %}
        <a href="/fun-stuff/">Fun stuff I’ve made</a>
      </li>
      <li>
        {% inline_svg filename="icons/paperplane.svg" class="dark_aware" %}
        <a href="https://buttondown.com/alexwlchan">Newsletter</a>
      </li>
      <li>
        {% inline_svg filename="icons/newspaper.svg" class="dark_aware" %}
        <a href="/articles/">Articles</a>
      </li>
      <li>
        {% inline_svg filename="icons/note.svg" class="dark_aware" %}
        <a href="/notes/">Notes</a>
      </li>
    </ul>
  </li>
</ul>

<script>
  function randomiseDieValue(selector, choices) {
    const elem = document.querySelector(selector);
    const chosenIndex = Math.floor(Math.random() * choices.length);
    elem.setAttribute("data-value", choices[chosenIndex]);
    
    const isAlternative =
      (choices[chosenIndex] === "2" && selector === "#lowerDie") ? false
      : Math.random() < 0.5;

    elem.setAttribute("data-alt", isAlternative);
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    randomiseDieValue("#lowerDie", ["2", "3", "4", "5", "6"]);
    randomiseDieValue("#upperDie", ["1", "2", "3", "4", "5", "6"]);
  })
</script>
  