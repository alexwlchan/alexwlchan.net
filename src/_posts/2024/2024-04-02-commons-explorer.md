---
layout: post
date: 2024-04-02 15:40:35 +00:00
title: The new Flickr Commons Explorer
summary: A new way to browse the photos in the Flickr Commons programme.
tags:
  - flickr
  - flickr foundation
colors:
  css_light: "#d0395a"
  css_dark:  "#DBD4D3"
link: https://commons.flickr.org/
---
One of the things I've been working on at the Flickr Foundation is a new "Commons Explorer", a way to browse the photos in the Flickr Commons.

Flickr Commons is a collection of historical photography from cultural institutions from all around the world, all with no known copyright restrictions.
It started with the Library of Congress in 2008, and now includes over 100 institutions from 24 different countries.

One of the cool things about Flickr Commons is the variety of photos, and I enjoy looking "across" the Commons.
I used a lot of Commons photos in my [Monki Gras talk] last month, and I had fun using the [new search][search] to find dance-related photos from all the different members.

The [Commons Explorer] is a new tool that encourages this sort of cross-collection exploration.
It tries to treat the Flickr Commons as a single collection of photographs, and to provide interesting views into the data that are more than just traditional search.
There are lots of cool photos to find!

You can try the new Commons Explorer at [commons.flickr.org](https://commons.flickr.org), or you can learn more in [our introductory blog post](https://www.flickr.org/new-flickr-commons-explorer/).

<style type="x-text/scss">
  #grid {
    display: grid;
    grid-template-columns: 3fr 2fr;
    grid-template-rows: auto auto;
    grid-gap: var(--grid-gap);

    img {
      width:  100%;
      height: 100%;
      object-fit: cover;
    }

    picture:nth-child(1) {
      grid-row: 1 / span 2;

      img {
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
      }
    }

    picture:nth-child(2) {
      img {
        border-top-left-radius: 0;
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
      }
    }

    picture:nth-child(3) {
      img {
        border-top-left-radius: 0;
        border-top-right-radius: 0;
        border-bottom-left-radius: 0;
      }
    }
  }
  </style>

<div id="grid">
  {%
    picture
    filename="commons_explorer_screenshot1.png"
    width="444"
    class="screenshot"
    alt="The homepage of the Commons Explorer, showing an introductory message and a 2-column grid of recent photos."
  %}

  {%
    picture
    filename="commons_explorer_screenshot2.png"
    width="296"
    class="screenshot"
    alt="A list of members in the Flickr Commons, showing cards for each member. Each card has a selected photo from the member, their name, and some basic metadata."
  %}

  {%
    picture
    filename="commons_explorer_screenshot3.png"
    width="296"
    class="screenshot"
    alt="Conversations on Flickr Commons photos -- comments people have left. There’s a single conversation on a photo of a woman called “Peggy Barthes”, with two comments shown next to the photo."
  %}
</div>

[Monki Gras talk]: /2024/step-step-step/
[search]: https://commons.flickr.org/search?query=dance
[Commons Explorer]: https://commons.flickr.org/
[conversations page]: https://commons.flickr.org/conversations/
