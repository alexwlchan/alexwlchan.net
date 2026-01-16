---
layout: post
date: 2025-02-08 22:32:46 +00:00
title: Good embedded toots
summary: |
  I replaced Mastodon's native post embeds with lightweight HTML and CSS snippets that are faster to load, more resilient to outages, and support dark mode -- and I had fun doing it.
tags:
  - mastodon
  - blogging about blogging
---
In [my previous post][bagit], there was a first for this site: I embedded a post from Mastodon.

Like many social media services, Mastodon has built-in support for [embedding posts][native].
If you're looking at a public post, you can get a snippet of HTML and JavaScript to show that post in another web page.
You add that snippet to your page, and when somebody opens it, the snippet will appear as a Mastodon post.
It's quick, easy, and not how I did it.

When I want to embed post from social media sites, I don't use the native embed.
Instead, I write my own HTML and CSS to mimic their appearance, and it looks pretty close to the real thing.

Here's a comparison of a native/custom Mastodon embed -- they're not exactly the same, but close enough that you probably wouldn't notice unless you were looking:

<figure class="comparison">
  {%
    picture
    filename="mastodon_native_embed.png"
    alt="Screenshot of an embedded Mastodon toot"
    width="541"
  %}
  {%
    picture
    filename="mastodon_custom_embed.png"
    alt="Screenshot of a custom Mastodon toot. It doesn't have the nuber of boosts or favourites, but otherwise looks pretty close."
    width="541"
  %}
</figure>

<style>
  .comparison {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 1em;
  }

  @media screen and (max-width: 500px) {
    .comparison {
      grid-template-columns: 1fr;
    }
  }
</style>

This is something I've been doing for over a decade – I got the original idea from Dr Drang, who does something [similar for tweets][good_tweets].
(He wrote that post in 2012, and it highlights the value of resilient embeds -- two of the four tweets he's quoted are no longer available.
The post would be harder to read if you couldn't see the tweets he was quoting and replying to.)

Many years ago, I copied Dr Drang's code, created my own variant, and I used that for embedding tweets.
I've now created another variant that works for Mastodon toots, and I have unfinished branches with more variants for Instagram and Bluesky.

[bagit]: /2025/bagit-errors/
[native]: https://fedi.tips/how-to-embed-mastodon-posts-on-a-website/
[the native embed]: /files/2025/native-mastodon-embed.html
[custom embed]: /files/2025/custom-mastodon-embed.html
[good_tweets]: https://leancrew.com/all-this/2012/07/good-embedded-tweets/

## Why do I prefer my embeds?

There are several reasons:

*   **My embeds are smaller and faster.**
    Mastodon posts are short, and yet [the native embed] downloads nearly a megabyte of data to display 88 words of text -- including the audio file `boop.mp3`, for reasons I can't imagine.
    Meanwhile my [custom embed] requires just 35KB.

    I try to keep this site pretty lean and lightweight -- the average size of an HTML page is just 13KB.
    Adding a megabyte of data for an embed would undo all that hard work.

*   **My embeds don't require any JavaScript, third-party or otherwise.**
    You don't need JS to show static content, and adding third-party code introduces a privacy risk for my readers.

    I'm not completely opposed to JavaScript, but it's massively overused on the modern web.
    It's useful for [interactive elements][pyramid], but I really don't need it on this content-only site.

*   **My embeds are more resilient.**
    Because I have no dependency on the Mastodon server, it doesn't matter if the server goes away or the toot is deleted.
    My page will be unaffected.

    This is why many people include social media posts as images, or copy the text into a blockquote.
    We're in a time of increased tumult and instability for social media platforms, but their woes aren't going to leave holes in my posts.

*   **My embeds support dark mode.**
    A few years ago I added dark mode to this site.
    It's not something I use myself, but I know it's important to a lot of people and it was a fun little project.
    The native Mastodon embeds [always show toots in light mode][light_mode_issue], whereas my embeds will adapt to your preference:

<figure class="comparison" style="margin-left: 40px">
  {%
    picture
    filename="mastodon_custom_embed.png"
    class="dark_aware"
    alt="Screenshot of a custom Mastodon toot in light mode."
    width="541"
  %}
  {%
    picture
    filename="mastodon_dark_embed.png"
    class="dark_aware"
    alt="Screenshot of a custom Mastodon toot in dark mode."
    width="541"
  %}
</figure>

On the other hand, the argument in favour of native embeds is that they need minimal effort, they should always work, and they support more features.
My custom embeds can't do pictures, or link previews, or quote toots, because I've never embedded a toot that uses those.
If/when I do, I'll have to write the code to support that.
I'll find that fun, but most people would find that annoying.

I don't know what accessibility is like for native embeds.
My custom embeds only use a handful of semantic HTML elements, so they get a lot of good behaviour "by default" from the browser.
I hope native embeds are good for accessibility, but I don't know enough to say whether my approach is better or worse in that regard.

[pyramid]: https://www.gov.uk/service-manual/technology/using-progressive-enhancement
[light_mode_issue]: https://github.com/mastodon/mastodon/issues/32134

## How does it work?

I have some HTML and CSS that render the embedded toot.
Here's the entirety of the HTML -- I've tweaked this ever so slightly for readability, but the key parts are there.

```html
<blockquote class="mastodon-embed">
  <div class="header">
    <a class="name_header" href="https://code4lib.social/@linguistory">
      <img class="avatar" src="linguistory.jpg" alt="">
      <div class="name">
        <span class="display_name">James Truitt (he/him)</span>
        <span class="account_name">@linguistory@code4lib.social</span>
      </div>
    </a>
    <img class="mastodon_logo" src="logo.svg">
  </div>
  <p class="text">
    Do any <a href="https://code4lib.social/tags/digipres">#digipres</a> folks happen to have a handy repo of small invalid bags for testing purposes?
    <br>
    <br>
    I'm trying to automate our ingest process, and want to make sure I'm accounting for as many broken expectations as possible.
  </p>
  <p class="meta">
    <a href="https://code4lib.social/@linguistory/113924700205617006">31 Jan 2025 at 19:49</a>
  </p>
</blockquote>
```

The CSS styles are a bit long to include here, but you can see them by reading the source code of [my demo page][demo].
I'm using [CSS grid layout][grid] to lay out the different components, but otherwise nothing too complicated.

I designed my custom embed by creating two HTML files: one with a native embed, and one with my custom embed.
I used the developer tools to get key values from the native embed, like colours and spacing, then I kept adding styles to my custom embed until it looked about right.

When I want to embed a toot now, I write a line like:

```
{% raw %}{% mastodon https://code4lib.social/@linguistory/113924700205617006 %}{% endraw %}
```

This calls a [Jekyll plugin] that replaces this line with an embedded toot.
This code is very scrappy and poorly documented, so it may not be especially easy to adapt to your own site -- if you want to do this, start from the HTML and CSS instead.

Like everything on this site, my Mastodon embeds are a work-in-progress and not something that everybody should copy.
The built-in embeds are quick, easy, and convenient, and they're what most people should use.
But what I like about having my own website is that when I do want to spend an unreasonable amount of effort on something, and do it just because I think it's fun, I can do that, and nobody can stop me.

[demo]: /files/2025/custom-mastodon-embed.html
[Jekyll plugin]: https://github.com/alexwlchan/alexwlchan.net/blob/main/src/_plugins/embed_mastodon.rb
[grid]: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
