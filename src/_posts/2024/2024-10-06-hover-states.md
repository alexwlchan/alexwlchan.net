---
layout: post
date: 2024-10-06 21:22:28 +0000
title: Two examples of hover styles on images
summary: When I hover over an image, I can add a border to a link, or change the colours of an SVG icon.
tags:
  - css
  - svg
  - drawing things
---
I enjoy adding [`:hover` styles][mdn] to my websites.
A good hover style reminds me of how fast and responsive our computers can be, if we let them.
For example, I add a thicker underline when you hover over a link on this site, and it appears/disappears almost instantly as I move my cursor around.
It feels snappy; it makes me smile.

I want to show you a pair of hover states I've been trying for images.

[mdn]: https://developer.mozilla.org/en-US/docs/Web/CSS/:hover

## Adding an image border on hover

If I'm showing a small preview of an image that's a clickable link to the full-sized version, I like to add a coloured border when you hover over it.
It's a visual clue that something will happen when you click, and "see the big version of the image" is a pretty normal thing to happen.

Initially I implemented this by adding a `border` property on hover, for example:

{% code lang="css" %}
a:hover img {
  border: 10px solid red;  /* don't do this */
}
{% endcode %}

But a border takes up room on the page, which causes everything to get rearranged around it.
Everything moves to make space for the border that just appeared, which is precisely what I don't want.
I want a subtle hover, not a disruptive one!

There are ways you can prevent this movement, but I couldn't get them to work in a way I found satisfactory.
For example, you could add a negative margin to offset the border, or an always-on transparent border that only changes colour when you hover -- but those can interfere with other CSS rules.
It became a game of whack-a-mole to make all my margins work in a consistent way.

The better approach I've found is to add a [`box-shadow`](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow) with no blur -- this looks like a border, but it's purely visual and doesn't take up any space on the page.
This is the rule I use:

{% code lang="css" %}
a:hover img {
  /* Four length values and a color */
  /* <offset-x> | <offset-y> | <blur-radius> | <spread-radius> | <color> */
  box-shadow: 0 0 0 10px red;
}
{% endcode %}

<style>
  #examples {
    display: grid;
    grid-gap: var(--grid-gap);
    grid-template-columns: repeat(2, 1fr);
    margin-left:  auto;
    margin-right: auto;
    max-width: 500px;
  }

  #rounded_examples {
    display: grid;
    grid-gap: var(--grid-gap);
    grid-template-columns: repeat(3, 1fr);
    margin-left:  auto;
    margin-right: auto;
    max-width: 500px;
  }

  #examples,
  #rounded_examples {
    text-align: center;
  }

  #examples p {
    margin-bottom: 0;
  }

  .border_hover a,
  .shadow_hover a {
    display: inline-block;
  }

  .border_hover:hover img,
  #examples.hover .border_hover img,
  #rounded_examples.hover .border_hover img {
    border: 10px solid var(--primary-color);
  }

  .shadow_hover:hover img,
  #examples.hover .shadow_hover img,
  #rounded_examples.hover .shadow_hover img {
    box-shadow: 0 0 0 10px var(--primary-color);
  }

  .outline_hover:hover img,
  #rounded_examples.hover .outline_hover img {
    outline: 10px solid var(--primary-color);
  }
</style>

Here's a demo of both approaches.
Notice how the rest of the page moves around when you add a `border`, but not when you add a `box-shadow`:

<div id="examples">
  <div>
    <a href="https://www.pexels.com/photo/hummingbird-sitting-on-branch-16820102/" class="border_hover">
      {%
        picture
        filename="hummingbird.jpg"
        alt=""
        width="200"
      %}
    </a>
    <p><code>border</code></p>
  </div>

  <div>
    <a href="https://www.pexels.com/photo/hummingbird-sitting-on-branch-16820102/" class="shadow_hover">
      {%
        picture
        filename="hummingbird.jpg"
        alt=""
        width="200"
      %}
    </a>
    <p><code>box-shadow</code></p>
  </div>
</div>

(If you're on a device that doesn't support hovering, you can <a href="#examples" onclick="document.querySelector('#examples').classList.toggle('hover');">toggle the hover styles manually</a>.)

<blockquote id="update_outline">
  <p>
    <strong>Update, 23 October 2024:</strong>
    Several people wrote to me to tell me about CSS's <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/outline"><code>outline</code> property</a>, which takes the same arguments as <code>border</code> but doesn’t take up any space.
  </p>
  <p>
    I had a vague memory of trying this and it not working, but I couldn’t remember why.
  </p>
  <p>
    I did some investigating and discovered what looks like a bug in Safari/Webkit.
    If you apply <code>text-decoration</code> styles on hover, they prevent any <code>outline</code> styles from appearing.
    Given that Safari is my primary browser and I use a lot of <code>text-decoration</code> styles, I imagine I tried <code>outline</code> at some point, ran into this issue or something similar, and I never thought about the property again.
  </p>
  <p>
    (This isn’t the first hover-related bug I’ve encountered in Safari.
    I ran into <a href="https://bugs.webkit.org/show_bug.cgi?id=61697">another bug</a> in March, and I’ve filed this <code>outline</code>/<code>text-decoration</code> bug as <a href="https://bugs.webkit.org/show_bug.cgi?id=282009">bug&nbsp;282009</a>.)
  </p>
  <p>
    If you don’t use <code>text-decoration</code> or you don’t care about Safari/WebKit support, then you may find <code>outline</code> very handy.
    It uses the same syntax as <code>border</code>, so it’s easier to remember than <code>box-shadow</code>.
  </p>
  <p><code style="white-space: pre;">a:hover img {<br/> <span></span> outline: 10px solid red;<br/>}</code></p>
</blockquote>




## Changing the colour of icons on hover

A while ago I added social media links to the footer of this website.
I displayed them as subtle, monochrome icons, to avoid overwhelming the footer with an explosion of different brand colours.
I thought it would be fun to show the site's brand colour when you hovered over the icon.
If, say, you hover over the bird icon and see Twitter's shade of blue, it's a subtle confirmation that this is indeed a link to my Twitter profile.

<style type="x-text/scss">
  /* Colour the icons correctly.
   *
   * Each icon contains two shapes:
   *
   *    - the `background` (the circle)
   *    - the `accent` (the cutout for the icon)
   *
   * In the default state, the background is white and the accent is
   * transparent, letting through the default footer colour.
   *
   * When you hover, we make the accent white and replace the background
   * with the brand colours, as a visual cue that it's the site you expect.
   */
  #social_icons {
    text-align: center;
    line-height: 0;
    list-style-type: none;
    padding: 0;
  }

  #social_icons a .background { fill: var(--accent-grey); }
  #social_icons a .accent     { fill: none;               }

  #social_icons a:hover,
  #social_icons.hover a {
    .accent { fill: white; }

    &[href="mailto:alex@alexwlchan.net"]              .background { fill: #0067B9; }
    &[href="https://books.alexwlchan.net"]            .background { fill: #333; }
    &[href="https://alexwlchan.net/atom.xml"]         .background { fill: #F99000; }
    &[href="https://twitter.com/alexwlchan"]          .background { fill: #1DA1F2; }
    &[href="https://social.alexwlchan.net/@alex"]     .background { fill: #563ACC; }
    &[href="https://github.com/alexwlchan/"]          .background { fill: #24292f; }
    &[href="https://www.linkedin.com/in/alexwlchan/"] .background { fill: #007EBB; }

    &[href="https://ko-fi.com/alexwlchan"] #kofi_heart  { fill: #f14255; };
    &[href="https://ko-fi.com/alexwlchan"] #kofi_circle { fill: #50aee4; };
  }

  #social_icons > li {
    display: inline-block;
  }

  #social_icons > li:not(:last-child) {
    margin-right: 10px;
  }
</style>

Here are all the icons I had in this system:

<ul id="social_icons">
  {% comment %}
    Be careful about tweaking the whitespace here; the included SVGs
    are quite sensitive to linebreaks and the like.

    In particular, if you push the closing </a> down to a new line,
    the underlines start appearing between icons.
  {% endcomment %}
  <li>
    <a href="mailto:alex@alexwlchan.net">
      <span class="visually-hidden">email</span>
      <span aria-hidden="true">{% inline_svg filename="social_icons/email.svg" %}</span></a>
  </li>

  <li>
    <a href="https://books.alexwlchan.net">
      <span class="visually-hidden">what I’m reading</span>
      <span aria-hidden="true">{% inline_svg filename="social_icons/book.svg" %}</span></a>
  </li>

  <li>
    <a id="footer_link--rss" href="https://alexwlchan.net/atom.xml">
      <span class="visually-hidden">RSS feed</span>
      <span aria-hidden="true">{% inline_svg filename="social_icons/rss.svg" %}</span></a>
  </li>

  <li>
    <a href="https://twitter.com/alexwlchan">
      <span class="visually-hidden">Twitter</span>
      <span aria-hidden="true">{% inline_svg filename="social_icons/twitter.svg" %}</span></a>
  </li>

  <li>
    <a rel="me" href="https://social.alexwlchan.net/@alex">
      <span class="visually-hidden">Mastodon</span>
      <span>{% inline_svg filename="social_icons/mastodon.svg" %}</span></a>
  </li>

  <li>
    <a href="https://github.com/alexwlchan/">
      <span class="visually-hidden">GitHub</span>
      <span aria-hidden="true">{% inline_svg filename="social_icons/github.svg" %}</span></a>
  </li>

  <li>
    <a href="https://www.linkedin.com/in/alexwlchan/">
      <span class="visually-hidden">LinkedIn</span>
      <span>{% inline_svg filename="social_icons/linkedin.svg" %}</span></a>
  </li>

  <li>
    <a href="https://ko-fi.com/alexwlchan">
      <span class="visually-hidden">Kofi</span>
      <span>{% inline_svg filename="social_icons/kofi.svg" %}</span></a>
  </li>
</ul>

(If you're on a device that doesn't support hovering, you can <a href="#social_icons" onclick="document.querySelector('#social_icons').classList.toggle('hover');">toggle the hover styles manually</a>.)

The brand icons come from the websites themselves; the generic icons are from [the Noun Project](https://thenounproject.com).
When I downloaded the icon, I typically got an SVG file with one or more `path` elements that defined the icon's shape.

For example, this is what I got in the SVG file for [the email icon](https://thenounproject.com/icon/email-1573175/):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200pt" height="1200pt" version="1.1" viewBox="0 0 1200 1200" xmlns="http://www.w3.org/2000/svg">
 <path d="m323.46 411.07 …"/>
</svg>
```

To turn this into my footer icon, I wrapped the `path` in a slightly more complex SVG:

```xml
<svg width="30px" height="30px" version="1.1" viewBox="0 0 950 950" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>

    <!-- Wrap the original envelope shape in a named group -->
    <g id="envelopeIcon">
      <svg x="-125" y="-125">
        <path d="m323.46 411.07 …"/>
      </svg>
    </g>

    <!-- Define a mask that blocks out the envelope shape -->
    <mask id="envelope">
      <rect x="0" y="0" width="950" height="950" fill="white"/>
      <use xlink:href="#envelopeIcon" fill="black"/>
    </mask>
  </defs>

  <!-- Define two shapes that actually get drawn -->
  <circle cx="475" cy="475" r="450" class="background"/>
  <circle cx="475" cy="475" r="475" class="foreground" mask="url(#envelope)"/>
</svg>
```

First I define a shape `envelopeIcon` which uses that original `path`, and defines the shape of the element as a reusable group.
Then I define [an SVG mask](/2021/inner-outer-strokes-svg/) `envelope` that blocks out the envelope shape.
Finally, I define two shapes that actually get drawn: a `foreground` and a `background`.

Here's a 3D view of the two shapes, so you can see more clearly how they form a set of layers:

{%
  inline_svg
  filename="layers.svg"
  class="dark_aware"
%}

Now I have two elements that I can style independently.
For example:

{% code lang="css" %}
.email .foreground { fill: gray; }
.email .background { fill: none; }

a:hover .email .foreground { fill: blue;  }
a:hover .email .background { fill: white; }
{% endcode %}

This technique can be extended to more complex icons -- split it into multiple elements, and style each one independently.

It took me a while to get these icons working as I wanted, and I remember trying some quite fiddly hacks.
As I was writing this post, I was pleasantly surprised to discover that the hover styles aren't as complicated as I thought.
I just had to figure out the general approach.

One thing I'm proud of is how readable this site is without CSS.
I made these icons look good on a sans-CSS page by adding inline `fill` attributes to the background/foreground elements (e.g. `<circle fill="white" …>`).
These inline styles get applied even if CSS is broken or disabled.
I lose the interactivity, but the icon is still legible.

By the time you read this, those icons will have vanished from the footer.
They were fun for me to work on, but almost nobody used them and they added almost 8KB of HTML to every page.
That might not seem like much, until I tell you the average page size was a slender 21.1KB -- nearly 40% of my HTML was spent on social media links nobody was clicking!
