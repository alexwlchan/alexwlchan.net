---
layout: post
date: 2023-03-13 13:24:57 +0000
title: Cats, cross-stitch, and copyright
summary: In celebration of my favourite apex predator.
tags:
  - cross-stitch
colors:
  index_light: "#7c590f"
  index_dark:  "#debd4d"
  css_light:   "#976f02"
  css_dark:    "#fcb905"
is_featured: true
---

I've always been a cat person, and my favourite species of cat (aside from the cats I've actually lived with) is the cheetah.

This probably goes back to a school project about cheetahs I did when I was nine years old -- I had to write about an endangered species for science class.
I have very distinct memories of this project, down to the glossy photo I stuck on the front cover, so I was delighted to find it while sorting through [some old papers] recently.

I wrote this project in March **2002** (!), which means it's one of the oldest bits of my writing I still have.
And while my writing and design skills have improved since then, I can see echoes of my current style in even this early work.
Here are a few of the pages:

<figure id="school_project" class="wide_img">
  <div>
    {%
      picture
      filename="IMG_3362.jpg"
      width="475"
      alt="A two-page spread, showing the first page of the project. On the left-hand side is the green piece of card I used as a cover; on the right-hand side is the cover page. It says 'The Cheetah' in big letters, followed by 'Endangered species!' as a subtitle. Then there's a big glossy photo of a cheetah snarling its teeth, and below that some attribution: 'by Alexander Chan / Berkhampstead School / March 2002'."
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_3367.jpg"
      width="238"
      alt="Four hand-drawn illustrations on a page titled 'A cheetah running'. The first drawing shows the cheetah pushing down on its back feet; the second shows how this pushes the cheetah forward; the third shows its four legs lifted off the ground; the final picture shows its front legs touch down."
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_3373.jpg"
      width="238"
      alt="A page of general information, including the etymology of the word 'cheetah', some translations in different languages, the fact that a fully-grown cheetah has over 3000 spots, and that a cheetah is recognisable by the black 'tear mark' that runs down its face. There's an illustration of a cheetah looking at the reader, in which the tear mark is visible on either side of its nose."
    %}
  </div>
</figure>

I don't remember a lot else from this time, but this project and the fact about cheetahs have a distinctive black "tear mark" has always stuck in my brain.

[some old papers]: /2023/school-stuff/

---

I was recently casting around for another cross-stitch project to do, and while searching Etsy I found a cheetah pattern.
Perfect!
I got to work, and two months later I have this to show for it:

<figure>
  {%
    picture
    filename="IMG_3360.jpg"
    width="950"
    class="wide_img"
    alt="Some cross-stitch embroidery of a cheetah. The cheetah is running, with it legs angled beneath it as if its partway off the ground. It's leaning towards the right, with its tail curving behind it. The piece is stitched on white fabric in varying shades of yellow/brown/black, and mounted in a square frame made of yellowy-orange wood."
  %}
  <figcaption>
    I find it very difficult to take good photos of my cross-stitch pieces.
    There’s a large pane of glass in the frame that makes it tricky to find an angle which doesn’t have me in the reflection, and my camera struggles with the white balance.
    I’m sure it’s possible to take good photos, but the best way to enjoy this art is in person!
  </figcaption>
</figure>

I really like the finished piece -- it captures the energy of a running cheetah, the colours are gorgeous, and you can see the distinctive black tear lines.
I stitched it on 18 count aida, using a dozen or so shades of thread.
The bright yellow frame was made by [Landseer Picture Framing], and it's approximately 14″ square.
I've hung it next to my bookshelf, and it brightens up the wall nicely.

Normally this is where I'd link to where you can buy the pattern, but on this occasion I won't -- because I'm not sure I want to promote the seller.

[Landseer Picture Framing]: https://landseerpictureframes.co.uk/

---

A couple of weeks ago I showed somebody the work-in-progress, and they said "oh hey, I think I've seen that picture before".
My heart sank, because I know what that means.

I used Google Lens to do a reverse image lookup, and I found various low-quality Amazon pages and Etsy products with a similar image -- t-shirts, mugs, posters, and more.

{%
  picture
  filename="etsy-cheetah-listing.jpg"
  width="600"
  class="screenshot"
  alt="An Etsy listing of a canvas print of a similar-looking cheetah picture, but with more fine detail than the cross-stitched version."
%}

The Etsy seller I bought my cross-stitch pattern from has dozens of patterns, with a variety of art styles, and they don't mention any artist names.
I think they're probably scraping the images, running them through software to create a cross-stitch pattern (there are plenty of tools for doing this), and selling them for their own profit.
The original artist probably doesn't see a penny.
I'm no expert, but this feels like blatant copyright infringement.

I did eventually find who I think deserves the artistic credit – **Faenkova Elena**, an illustrator from Minsk who sells high-quality copies of this image on both [Shutterstock] and [Dreamstime].

I want to support artists, and I want them to be fairly compensated for their work!
I feel gross knowing that I've inadvertently helped somebody make an unfair profit off an artist's work, and it's not the first time this has happened.
I've bought other Etsy cross-stitch patterns without realising they were based on somebody else's art.

I've bought a standard image licence on Shutterstock, which includes personal, non-commercial use -- so I feel less bad about what's hanging on my wall -- but I wish I didn't have to play art detective when I'm buying patterns.
I wish Etsy and Amazon were better at stopping copyright infringement.

These issues aside, I really am thrilled with this latest piece – it was fun to make and it's a nice splash of colour in my living room.

[Shutterstock]: https://www.shutterstock.com/image-illustration/cute-cheetah-watercolor-illustration-african-animal-292143374
[Dreamstime]: https://www.dreamstime.com/stock-illustration-cheetah-t-shirt-graphics-african-animals-cheetah-illustration-splash-watercolor-textured-background-unusual-illustration-w-image56129690

<style type="x-text/scss">
  #school_project {
    display: grid;
    grid-template-columns: 
      calc(50% - var(--grid-gap) * 2/3)
      calc(25% - var(--grid-gap) * 2/3)
      calc(25% - var(--grid-gap) * 2/3);
    grid-gap: var(--grid-gap);
  }

  #school_project > div {
    grid-row: 1 / 1;
  }

  @media screen and (max-width: 500px) {
    #school_project {
      grid-template-columns: 50% 50%;
    }

    #school_project > div:nth-child(1) {
      grid-row: 1 / 2;
      grid-column: 1 / span 2;
    }

    #school_project > div:nth-child(2) {
      grid-row: 2 / 2;
      grid-column: 1 / 2;
    }

    #school_project > div:nth-child(3) {
      grid-row: 2 / 2;
      grid-column: 2 / 2;
    }
  }

  #school_project > div img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
</style>
