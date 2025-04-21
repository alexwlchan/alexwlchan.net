---
layout: post
title: Fixing the background of my site in dark mode
summary: If you're using an image as your background, remember to set a fallback colour as well.
tags:
  - css
  - blogging about blogging
---
I support dark mode on this site, even though I don't use it myself.
As part of my dark theme, I have a colour-inverted copy of the background texture I use on the light mode of the site, which is the ["White Waves" pattern][white_waves] made by Stas Pimenov.

<style type="text/css">
  #comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: var(--border-width);
  }

  #comparison img {
    border: var(--border-width) var(--border-style) var(--block-border);
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
    <img src="/theme/white-waves-transparent.png" alt="">
    <img src="/theme/black-waves-transparent.png" alt="">
  </div>
  <figcaption>
    If you don't switch between light and dark mode, odds are good that you've only ever seen one of these background textures.
  </figcaption>
</figure>

I was setting these images as the background with two CSS rules, using the [`prefers-color-scheme: dark`][prefers_dark] media feature to swap out the image in dark mode:

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

And this works… mostly.

But I mostly use light mode, so while I wrote this CSS and I do some brief testing whenever I make changes, I'm not *using* the site in dark mode.
I know how it works in my local development environment, not how it feels as a day-to-day user.

Late last night I had my phone in dark mode to avoid waking the other people in the house, and I opened my site.
I saw a brief flash of white, and then the dark background texture appeared.
That flash of bright white is precisely what you *don't* want when you're using dark mode, but it happened anyway.
I made a note to work it out in the morning, then I went to bed.

Now I'm fully awake, it's obvious what happened.
Because I'm only setting the image URL as the `background` property, there's a brief gap between the CSS being parsed and the background image being loaded.
In that time, the browser doesn't have anything to put in the background, so you just get pure white.

I've made two changes to prevent this happening again.

1.  **I've added a colour to use as a fallback until the image loads.**
    You can add a colour to your `background` property, and it's used until the image loads, or as a fallback if it doesn't.
    I already use this in a few places, and I'd just forgotten to add it for my background textures.

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

This whole "bug" reminds me of a phenomenon called [flash of unstyled text][fout], where web pages would briefly appear with the default font before custom fonts finished loading.
I rarely use custom fonts on the web so I never encountered this issue in the font context, but it's still affecting me in dark mode!

[white_waves]: https://www.toptal.com/designers/subtlepatterns/white-waves-pattern/
[prefers_dark]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme
[fout]: https://en.wikipedia.org/wiki/Flash_of_unstyled_content
[preload]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preload
