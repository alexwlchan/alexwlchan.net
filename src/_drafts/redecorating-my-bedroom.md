---
layout: post
title: Redecorating my bedroom
summary: Splashing some sunshine in the room where I sleep.
tags: home domestic
---

Back in March, I was visiting my sister and her newly-redecorated home, and it finally pushed me to redecorate my bedroom in a way I've been considering for about two years.

My bedroom used to have white walls, a dark grey wall, and a purple sliding wardrobe left by the previous owners.
I set it up when I first moved in – enough to be functional, but not especially warm or inviting.
This is the only picture I have of what it used to look like, because it was never a space that sparked much joy:

{%
  picture
  filename="IMG_9838.jpg"
  visible_width="750px"
  class="photo"
%}

Ever since I moved in, I thought about adding a splash of colour to the walls -- probably purple, to match the large wardrobe -- but I'm not sure that would work.
I was always worried that more purple would make the room feel even colder than it already was.

One of my sister's new rooms is pastel yellow, and it felt like a really nice space -- I asked her for the name of the paint, and wondered if I could use it in my room.
Purple and yellow is a combination that can work, with the right shades…

But what I actually realised is that the purple wardrobe had to go.
I kept it when I moved in, because I couldn't afford to replace it at the time, and it worked well enough -- but it was never a great fit for my needs.
It's mostly hanging rails, with very little shelf storage, and two metres of clothes rail is way more than I need.
The sliding doors also made it impossible to get to both halves at once; I had my pyjamas in one half and the laundry basket in the other.
Getting changed for bed was always a mildly frustrated experience.

I'd been gradually saving towards its replacement, and now was the time.

One Sunday, after one of the doors got stuck *yet again*, I finally broke out the toolbox and reduced it to parts.
I took great glee in disassembling something which has been a countless source of minor irritations.
(If I'd stopped for a second, I might have realised that Sunday afternoon before a busy week is an awful time to start a DIY project -- but I can be very impulsive.)

<style type="x-text/scss">
  #wardrobe {
    display: grid;
    grid-template-columns: auto auto;
    grid-gap: $grid-gap;
  }

  @media screen and (max-width: 500px) {
    #wardrobe {
      grid-template-columns: auto;
    }
  }
</style>

<div id="wardrobe" class="photo">
  <div>
    {% picture filename="70155648040__99EE2B94-C722-4E3F-922E-0093161E3058.jpg" visible_width="750px" %}
  </div>
  <div>
    {% picture filename="70155977066__50021B9A-2ED9-4BDD-B213-25F89132398E.jpg" visible_width="750px" %}
  </div>
</div>

I was shocked by how much of a difference just this change made – as well as the purple doors, the interior of the wardrobe was a drab grey, and it sucked a lot of life out of the room.
Just removing it made the room feel much lighter.
(It also uncovered a previously unknown-to-me plug socket!)

The next day, I went to the paint shop, and I bought several shades of yellow.
I went for pastel yellow on three of the walls (<span style="background: rgb(251, 229, 173); padding: 2px 5px; border-radius: 100px; color: black;">“Vanilla Sundae” 54YY 85/291</span>), and a bright yellow to replace the grey feature wall (<span style="background: rgb(251, 184, 71); padding: 2px 5px; border-radius: 100px; color: black;">“Sun Flare” 22YY 57/627</span>).
I love having bright feature walls in my rooms; I think they really make a space "pop".

I also redid the white on the ceiling, the skirting boards, and door frame, but do not ask me what shades they are.
Dulux have more names for white than Eskimos have words for snow.

<style type="x-text/scss">
  #painting {
    display: grid;
    grid-template-columns: calc(66% - 5px) calc(34% - 5px);
    grid-template-rows:    calc(50% - 5px) calc(50% - 5px);
    grid-gap: $grid-gap;
    aspect-ratio: 16 / 9;

    div:nth-child(1) {
      grid-column: 1 / 2;
      grid-row:    1 / span 2;
    }

    div:nth-child(2) {
      grid-column: 2 / 2;
      grid-row:    1 / 2;
    }

    div:nth-child(3) {
      grid-column: 2 / 2;
      grid-row:    2 / 2;
    }

    img {
      width:  100%;
      height: 100%;
      object-fit: cover;
    }
  }

  @media screen and (max-width: 500px) {
    #painting {
      grid-template-columns: auto;
      grid-template-rows: auto auto auto;

      div:nth-child(1) {
        grid-column: 1 / 1;
        grid-row:    1 / 3;
      }

      div:nth-child(2) {
        grid-column: 1 / 1;
        grid-row:    2 / 3;
      }

      div:nth-child(3) {
        grid-column: 1 / 1;
        grid-row:    3 / 3;
      }
    }
  }
</style>

<div id="painting" class="photo">
  <div>
    {%
      picture
      filename="IMG_3467.jpg"
      visible_width="500px"
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_3465.jpg"
      visible_width="250px"
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_3485.jpg"
      visible_width="250px"
    %}
  </div>
</div>

The painting took about a week, from start to finish.
Each wall got at least two coats, plus a coat of primer over the dark grey to lighten it before I added the yellow.
I'd always thought of the white walls in my bedroom as relatively clean, but I found lots of marks and scuffs on the wall that I'd previously missed – all gone now!

Once the painting was done, I wanted to review the furniture layout – including replacing the old wardrobe.
In the old layout, there was quite a lot of "dead" space – behind the door and down the sides of the wardrobe, and I think that made the room feel smaller than it was.
There was a lot of space I couldn't use.

I decided to push the bed into the corner, and open up the room.
This is a rough sketch of the layout I decided, which has way less "dead" space:

{%
  picture
  filename="bedroom_layout.png"
  visible_width="489px"
%}

I've lived with this layout for about six weeks, and I'm really enjoying it.
This is how my bed looks now (and yes, those are [cheetahs on the bedding]({% post_url 2023/2023-03-13-cats-cross-stitch-and-copyright %})):

{%
  picture
  filename="P5080114.jpg"
  visible_width="950px"
  class="photo wide_img"
%}

The chest of drawers gives me much more shelf space, and a lot of my clothes are now neatly packed inside.
I also rearranged some of my under-bed storage, which I was only half-using.
I've now repacked it so there's a lot more stuff under there, mostly stuff I need to keep but don't need to get to frequently -- like my guest bedding and some old paperwork.

At the other end of the room, the bright yellow adds a big burst of colour:

{%
  picture
  filename="P5080094.jpg"
  visible_width="950px"
  class="photo wide_img"
%}

The mirror is massive, and makes the room feel bigger.
It's also delightful for twirling in front of and admiring my sparkly outfits.
(And a very minor change: it now looks along the long end of the room, not the short end – so it feels even bigger than before.)
I love having a big mirror, highly recommend.

The clothes rail is new, and adds a splash of additional colour to the room.
My wardrobe has a lot of blue and green, which go especially nicely with the yellow walls.

And the door is hiding my messy laundry basket and waste bin.
I can still get to them in a pinch, but they're squirreled away.