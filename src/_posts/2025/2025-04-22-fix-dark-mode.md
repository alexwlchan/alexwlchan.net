---
layout: post
date: 2025-04-22 06:40:55 +0000
title: A flash of light in the darkness
summary: If you're using an image as your background, remember to set a fallback colour as well, especially if you're in dark mode.
tags:
  - css
  - blogging about blogging
---
I support dark mode on this site, and as part of the dark theme, I have a colour-inverted copy of the default background texture.
I like giving my website a subtle bit of texture, which I think makes it stand out from a web which is mostly solid-colour backgrounds.
Both my textures are based on the ["White Waves" pattern][white_waves] made by Stas Pimenov.

<style type="text/css">
  #comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: var(--border-width);
  }

  #comparison img {
    border: var(--border-width) var(--border-style) var(--block-border-color);
    object-fit: none;
  }

  #comparison img:nth-child(1) {
    border-top-left-radius:    var(--border-radius);
    border-bottom-left-radius: var(--border-radius);
  }

  #comparison img:nth-child(2) {
    border-top-right-radius:    var(--border-radius);
    border-bottom-right-radius: var(--border-radius);
  }
</style>

<figure style="width: 500px;">
  <div id="comparison">
    <img src="/static/white-waves.png" alt="" class="dark_aware">
    <img src="/static/black-waves.png" alt="" class="dark_aware">
  </div>
  <figcaption>
    If you don’t switch between light and dark mode, you’ve probably only seen one of these background textures.
  </figcaption>
</figure>

I was setting these images as my background with two CSS rules, using the [`prefers-color-scheme: dark`][prefers_dark] media feature to use the alternate image in dark mode:

```
body {
  background: url('https://alexwlchan.net/theme/white-waves-transparent.png');
}

@media (prefers-color-scheme: dark) {
  body {
    background: url('https://alexwlchan.net/theme/black-waves-transparent.png');
  }
}
```

This works, mostly.

But I prefer light mode, so while I wrote this CSS and I do some brief testing whenever I make changes, I'm not *using* the site in dark mode.
I know how dark mode works in my local development environment, not how it feels as a day-to-day user.

Late last night I was using my phone in dark mode to avoid waking the other people in the house, and I opened my site.
I saw a brief flash of white, and then the dark background texture appeared.
That flash of bright white is precisely what you *don't* want when you're using dark mode, but it happened anyway.
I made a note to work it out in the morning, then I went to bed.

Now I'm fully awake, it's obvious what happened.
Because my only `background` is the image URL, there's a brief gap between the CSS being parsed and the background image being loaded.
In that time, the browser doesn't have anything to put in the background, so you just get pure white.

This was briefly annoying in the moment, but it would be even more worse if the background texture never loaded.
I have light text on black in dark mode, but without the background image it's just light text on white, which is barely readable:

{%
  picture
  filename="dark_mode_sans_background.png"
  width="374"
  class="screenshot dark_aware"
  alt="Screenshot of light grey text on a white background. The text is difficult to read because it has barely any contrast with the background."
%}

I never noticed this in local development, because I'm usually working in a well-lit room where that white flash would be far less obvious.
I'm also using a local version of the site, which loads near-instantly and where the background image is almost certainly saved in my browser cache.

I've made two changes to prevent this happening again.

1.  **I've added a colour to use as a fallback until the image loads.**
    The CSS `background` property supports adding a colour, which is used until the image loads, or as a fallback if it doesn't.
    I already use this in a few places, and now I've added it to my `body` background.

    <pre><code>body {
      background: url('https://…/white-waves-transparent.png') <mark>#fafafa</mark>;
    }

    @media (prefers-color-scheme: dark) {
      body {
        background: url('https://…/black-waves-transparent.png') <mark>#0d0d0d</mark>;
      }
    }</code></pre>

    This avoids the flash of unstyled background before the image loads -- the browser will use a solid dark background until it gets the texture.

2.  **I've added [`rel="preload"` elements][preload] to the `head` of the page, so the browser will start loading the background textures faster.**
    These elements are a clue to the browser that these resources are going to be useful when it renders the page, so it should start loading them as soon as possible:

    ```
    <link
      rel="preload"
      href="https://alexwlchan.net/theme/white-waves-transparent.png"
      as="image"
      type="image/png"
      media="(prefers-color-scheme: light)"
    />
    <link
      rel="preload"
      href="https://alexwlchan.net/theme/black-waves-transparent.png"
      as="image"
      type="image/png"
      media="(prefers-color-scheme: dark)"
    />
    ```

    This means the browser is downloading the appropriate texture at the same time as it's downloading the CSS file.
    Previously it had to download the CSS file, parse it, and only then would it know to start downloading the texture.
    With the preload, it's a bit faster!

    The difference is probably imperceptible if you're on a fast connection, but it's a small win and I can't see any downside (as long as I scope the `preload` correctly, and don't preload resources I don't end up using).

    I've seen a lot of sites using `<link rel="preload">` and I've only half-understood what it is and why it's useful -- I'm glad to have a chance to use it myself, so I can understand it better.

This bug reminds me of a phenomenon called [flash of unstyled text][fout].
Back when custom fonts were fairly new, you'd often see web pages appear briefly with the default font before custom fonts finished loading.
There are well-understood techniques for preventing this, so it's unusual to see that brief unstyled text on modern web pages -- but the same issue is affecting me in dark mode
I avoided using custom fonts on the web to avoid tackling this issue, but it got me anyway!

In these dark times for the web, old bugs are new again.

[white_waves]: https://www.toptal.com/designers/subtlepatterns/white-waves-pattern/
[prefers_dark]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme
[fout]: https://en.wikipedia.org/wiki/Flash_of_unstyled_content
[preload]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preload
