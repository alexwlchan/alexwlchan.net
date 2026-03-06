---
layout: page
title: ""
colors:
  css_light: "#098a07"
  css_dark:  "#5ff042"
---

<style type="x-text/scss">
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

<style>
  #homepage_cards {
    list-style-type: "";
    padding: 0;
    margin: 0;
    
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--grid-gap);
  }
  
  @media screen and (max-width: 650px) {
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
      margin-top:  0;
      margin-left: 0;
    
      li {
        text-wrap: balance;
        display: grid;
        grid-template-columns: 24px auto;
        gap: 7px;
        margin-top: 6px;
      }
      
      li:first-child {
        margin-top: 0;
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
  
  #recent_articles {
    --primary-color: var(--red);
    --link-color:    var(--red);
  }
  
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
    
  #homepage_cards_wrapper {
    margin-top: 2.5em;
    background: rgba(153, 153, 153, 0.12);
  }
  
  @media (prefers-color-scheme: dark) {
    #homepage_cards_wrapper {
      background: rgba(43, 43, 43, 0.55);
    }
  }
  
  /* The width of the window is 100vw, the width of <main> is 100%.
   *
   * When we expand <section>s to break out of <main>, we need to add
   * a negative left margin to move it against the edge of the window,
   * then re-add our padding.
   *
   *    |                   |
   *    |    +++++++++++    | 
   *    |    +++++++++++    | 
   *    |                   |
   *
   *         <!- 100% ->
   *     <----- 100vw ----->
   *
   */
  #homepage_cards_wrapper {
    padding:     1.5em 0;
    width:       calc(100vw);
    margin-left: calc(50% - 50vw);
    
    & > * {
      max-width: var(--max-width);
      margin: 0 auto;
      padding: 0 var(--default-padding);
    }
  }
  
  #recent_articles h2 {
    margin-top: 1.5em;
  }
  
</style>

<section id="homepage_cards_wrapper">
<div>
  <ul id="homepage_cards">
    <li id="writing" class="card">
      <h2>My writing</h2>
      <ul>
        <li>
          {% inline_svg filename="icons/programming.svg" class="dark_aware" %}
          <span>
            <a href="/computers-and-code/">Computers and code</a>
          </span>
        </li>
        <li>
          {% inline_svg filename="icons/floppy_disk.svg" class="dark_aware" %}
          <span>
            <a href="/digital-preservation/">Digital preservation</a>
          </span>
        </li>
        <li>
          {% inline_svg filename="icons/accessibility.svg" class="dark_aware" %}
          <span>
            <a href="/inclusion/">Inclusion and accessibility</a>
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
          <a href="/work/">My day job</a>
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
</div>
</section>

<section id="recent_articles">
<h2>Recent articles</h2>
{%- set articles = (site.articles | sort(attribute="date", reverse=True))[:5] -%}
{%- with include_topic = true -%}
  {%- include "partials/article_links.html" -%}
{%- endwith -%}
<p><a href="/articles/" style="color: var(--text-color);">Read more articles</a> &rarr;</p>
</section>

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
  