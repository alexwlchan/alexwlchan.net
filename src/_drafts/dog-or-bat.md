---
layout: post
title: What mammal is that?
summary: In which Apple Photos accidentally tells me about a cool new animal.
tags:
  - fun-stuff
colors:
  index_light: "#834e32"
  index_dark:  "#c0b49d"
---

I was visiting my parents over Christmas, and they have a large dog called Ziva.
I like to take silly photos of the family pets, and this is one from last week that shows off a super-sized snoot:

<figure style="width: 600px">
  {%
    picture
    filename="ziva.jpg"
    width="600"
    class="photo"
    alt="A blurry photo of a dog with grey fur. The photo is a close-up on her nose, which is filling a large portion of the frame, and the rest of the photo is her face, with mostly closed eyes and ears folded back. She's resting on the arm of a comfy chair, half-asleep."
  %}
  <figcaption>
    No Photoshop here, just my iPhone’s Ultra Wide camera held close to her nose.
  </figcaption>
</figure>

For giggles, I decided to use the [animal detection feature][visual_lookup] to tell me what sort of dog Ziva is.
We're not actually sure of her breed because she's a rescue dog of unknown parentage, so it's always fun to try the animal detection and see what it suggests.

When I tried, I was shown a button I hadn't seen before: *Look up Mammal*.

{%
  picture
  filename="look-up-mammal.png"
  width="375"
  class="screenshot"
  alt="The same photo in the iOS Photos app, with an overlay sheet showing a 'Look Up Mammal' button."
%}

And with the best will in the world, I couldn't have guessed what it would suggest:

{%
  picture
  filename="hammer-headed-bat.png"
  width="375"
  class="screenshot"
  alt="A list of results for 'Look up Mammal', showing two suggestions: a Hammer-headed bat, and a Wolf."
%}

After we'd all had a good laugh at this suggestion, I opened [the Wikipedia page][wiki] and went down a rabbit hole.
When you see some photos, it starts to make more sense – several of the photos featured really do show a sizable snout.
Given the distortion in my photo, you can see why the algorithm thought there could be a match (and where the "hammer-headed" name comes from):

<style>
  #two_up_bats {
    display: grid;
    grid-template-columns: auto auto;
    grid-gap: 10px;
  }
</style>

<figure class="photo">
  <div id="two_up_bats">
    {%
      picture
      filename="hammer-headed-bat-1.jpg"
      width="750"
      link_to="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0223139#sec002"
      alt="A front-facing view of a bat with an elongated nose. The bar is a dark, reddish brown, looking directly at the camera, and its wings are folded along its sides. Its being held in the hand of somebody with a yellow glove."
    %}

    {%
      picture
      filename="hammer-headed-bat-2.jpg"
      width="750"
      link_to="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0223139#sec002"
      alt="The same bat, now in profile. Its elongated nose is more visible, which is large and rounded."
    %}
  </div>
  <figcaption>
    Photo by Sarah Olson et al, from an <a href="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0223139#sec002">article in PLOS ONE</a>.
    Used under CC0.
  </figcaption>
</figure>

And it turns out it's a pretty cool creature – it's a "megabat" (great name) and its wingspan can be close to a metre wide.
I think of bats as small and cuddly, but if something flew past that was that size, I'd be pretty nervous.
Imagine if something that looked like this flew towards you with outstretched wings on a dark night:

<figure style="width: 600px;">
  {%
    picture
    filename="fully-loaded-bat.jpg"
    width="600"
    class="photo"
    link_to="https://www.inaturalist.org/photos/247839218"
    alt="Another photo of a bat with partially extended wings, being held in somebody's hands. The wings are probably about a foot wide, and not fully extended. Several sharp looking claws are visible on the inner side of the wing."
  %}
  <figcaption>
    Photo by Bart Wursten, published on <a href="https://www.inaturalist.org/photos/247839218">iNaturalist</a>, used under CC BY-NC 4.0.
  </figcaption>
</figure>

And for extra scary points, it makes a [pretty loud honking sound], so loud that it's often considered a pest.
This noise is how males attract females, and it's so important that their internal organs are actually shaped around their ability to honk:

> The most noticeable anatomical features of the male involve sound production. The larynx is one-half the length of the vertebral column and fills most of the thoracic cavity, pushing the heart, lungs and alimentary canal backward and sideways.
>
> <cite>— <a href="https://academic.oup.com/mspecies/article/doi/10.2307/3504110/2600338"><em>Hypsignathus monstrosus</em></a>, by Paul Langevin and Robert M. R. Barclay, Mammalian Species Issue 357, 26 April 1990.</cite>

That [same paper](https://academic.oup.com/mspecies/article/doi/10.2307/3504110/2600338) also features a delightful description of the male nose, which sounds like somebody getting revenge for the way male authors describe women in novels:

> Males have a large, square, truncated head (Tate, 1942) with enormous pendulous lips, ruffles around a warty snout and a hairless, split chin (Lang and Chapin, 1917).

I find myself down this sort of rabbit hole surprisingly often, and I've begun to think of it as "serendipitous search results".
Whatever Ziva is, she's definitely not an African species of large bat, but it appeared in my search results anyway, and that was the start of some fun reading.
At other times, I'll look for a specific book at my local library, and they don't have it, but I'll end up reading half a dozen books with similar titles because that's what the search could find.

If you want more pictures of cool bats, there are a bunch of them [on iNaturalist][pics].
If not, I'll see you next time I stumble upon something fun and unexpected while searching.

[visual_lookup]: https://support.apple.com/en-gb/104962
[wiki]: https://en.wikipedia.org/wiki/Hammer-headed_bat
[pretty loud honking sound]: https://www.youtube.com/watch?v=BLm6YVFvNG8
[pics]: https://www.inaturalist.org/observations/144407784
