---
layout: post
date: 2023-05-11 20:21:18 +0000
title: Redecorating my bedroom
summary: Splashing some sunshine in the space where I sleep.
tags:
  - home
colors:
  css_light:   "#815701"
  index_light: "#815701"
  css_dark:    "#c79d2b"
  index_dark:  "#c79d2b"
---

Back in March, I was visiting my sister and her newly-redecorated home, and it gave me the inspiration to finally redecorate my bedroom – something I've been thinking about for two years.

---

My bedroom used to have white walls, a dark grey feature wall, and a purple sliding wardrobe, all left by the previous owners.
I added my own bed and a few other decorations when I first moved in, but nothing more substantial – enough to be functional, but not especially warm or inviting.
I only ever took a handful of photos of this setup:

{%
  picture
  filename="IMG_9838.jpg"
  width="750"
  class="photo"
  alt="A poorly-framed photograph of a bedroom. There's a double bed partially visible at the bottom of the frame, with a purple mattress cover. In front of the bed is a large wardrobe taking up most of one wall, which has purple and white sections on the front. The purple sections are slightly reflective, and show the bed on the other side of the room. On the bed is a large, upside down plushy shark (a Bhålaj), who looks about as excited as I feel about this room."
%}

Ever since I moved in, I thought about adding a splash of colour to the walls and making it my own -- probably purple, to match the large wardrobe -- but I was never sure that it would work.
I was always worried that more purple would make the room feel even colder than it already was.

One of my sister's new rooms is pastel yellow, and it felt like a really nice space -- and I decided I wanted that same yellow in my house.
Purple and yellow is a combination that can work, with the right shades, but I could see this yellow wouldn't go with the purple.

The purple wardrobe had to go.

I kept it when I moved in, because I couldn't afford to replace it at the time, and it worked well enough -- but it was never a great fit for my needs.
It's mostly hanging rails, with very little shelf storage, and two metres of clothes rail is way more than I need.
The sliding doors also made it impossible to get to both halves at once; I had my pyjamas in one half and the laundry basket in the other.
Getting changed for bed was always a mildly frustrated experience.

I'd been gradually saving towards its replacement, and now was the time.
I broke out the toolbox and reduced the wardrobe to a pile of parts.
I took great glee in disassembling something which has been a source of countless minor irritations.

<style type="x-text/scss">
  #wardrobe {
    display: grid;
    grid-template-columns: auto auto;
    grid-gap: var(--grid-gap);
  }

  @media screen and (max-width: 500px) {
    #wardrobe {
      grid-template-columns: auto;
    }
  }
</style>

<div id="wardrobe" class="photo">
  <div>
    {%
      picture
      filename="70155648040__99EE2B94-C722-4E3F-922E-0093161E3058.jpg"
      width="750"
      alt="The same bedroom from a previous angle, with a partially disassembled wardrobe against one wall. The doors have been removed and you can see the empty interior, which shows three vertical compartments separated by dividers. The interior is a drab and uninspiring grey, with dark water stains in several parts."
    %}
  </div>
  <div>
    {%
      picture
      filename="70155977066__50021B9A-2ED9-4BDD-B213-25F89132398E.jpg"
      width="750"
      alt="A pile of flat-pack wardrobe pieces stacked against a fence."
    %}
  </div>
</div>

I was shocked by how much of a difference just this change made – as well as the purple doors, the interior of the wardrobe was a drab grey, and it sucked a lot of life out of the room.
Just removing it made the room feel much lighter.
(It also uncovered a previously unknown-to-me plug socket!)

---

The next day, I went to the paint shop, and I bought several shades of yellow.
I went for pastel yellow on three of the walls (“Vanilla Sundae” 54YY 85/291), and a bright yellow to replace the grey on the feature wall (“Sun Flare” 22YY 57/627).
I love having bright feature walls in my rooms; I think they really make a space "pop".

I also redid the white on the ceiling, the skirting boards, and door frame, but do not ask me what shades they are.
Dulux have more names for white than Eskimos have words for snow.

<style>
  #painting {
    display: grid;
    grid-template-columns: calc(66% - 5px) calc(34% - 5px);
    grid-template-rows:    calc(50% - 5px) calc(50% - 5px);
    grid-gap: var(--grid-gap);

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

    @media screen and (min-width: 500px) {
      aspect-ratio: 16 / 9;
    }

    @media screen and (max-width: 500px) {
      /* Disabling `display: grid;` fixes a weird bug where the first/second
       * photos end up overlapping entirely.
       */
      display: block;

      div:nth-child(2) {
        margin-top:    var(--grid-gap);
        margin-bottom: var(--grid-gap);
      }
    }
  }
</style>

<div id="painting" class="photo">
  <div>
    {%
      picture
      filename="IMG_3467.jpg"
      width="500"
      alt="Looking into the partially painted bedroom through the door -- you can see three walls, with the window on the far side. The bed is in the middle of the room, covered in dust sheets and a variety of painting tools. Two of the walls have some patches of the light yellow on them, some of my initial roller work. Outside the window is darkness -- I was painting at night."
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_3465.jpg"
      width="250"
      alt="Another view into the room, this time looking towards the door. The grey feature wall is visible behind the bed, because I haven't started painting it yet. There's a little bit of masking around the door frame and some plastic sheets covering a large mirror on the wall."
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_3485.jpg"
      width="250"
      alt="Another angle of the feature wall, which has some masking tape around it and some initial roller work for the darker yellow. The yellow doesn't fully cover the wall yet; underneath it you can see the white primer I applied to lighten the grey."
    %}
  </div>
</div>

The painting took about a week, from start to finish.
Each wall got at least two coats, plus a coat of primer over the dark grey to lighten it before I added the yellow.
I'd always thought of the white walls in my bedroom as relatively clean, but I found lots of marks and scuffs on the wall that I'd previously missed – all gone now!

Once the painting was done, I wanted to review the furniture layout.
In the old layout, there was quite a lot of "dead" space – behind the door and down the sides of the wardrobe, and I think that made the room feel smaller than it was.
There was a lot of space I couldn't use.

I decided to push the bed into the corner, and open up the room.
This is a rough sketch of the new layout, which has way less "dead" space:

{%
  picture
  filename="bedroom_layout.png"
  width="489"
  alt="Two floorplans, the old on the left and the new on the right. In the old floorplan, the bed is sitting along the middle of one wall, with gaps down either side. There's also the old wardrobe pushed up against the opposite wall, leaving narrow gaps at either end. In the new floorplan, the bed is pushed into one corner, with a set of drawers and a clothes rail pushed against two other walls. There's also the bin and laundry stuck in the corner behind the door, in a space which was previously empty."
%}

The key idea of this new layout is to combine all the free space into a single area into the centre of the room, rather than break it up with furniture in the middle.
I did the same thing when I redecorated my office last year, and it made a big difference to the feel of the room.

---

I've lived with the new wall colours and furniture layout for about six weeks, and I'm really enjoying it.
My bedroom has gone from drab and uninspiring, to warm and inviting.

This is how my bed looks now (and yes, those are [cheetahs on the bedding](/2023/cats-cross-stitch-and-copyright/)):

{%
  picture
  filename="P5080114.jpg"
  width="950"
  class="photo wide_img"
  alt="Looking towards one end of the bedroom. On the left hand side is a double bed pushed into one corner, with a white duvet cover with small cheetahs on it, plus a large stack of pillows. On the right hand side is a tall, white set of drawers, with a variety of small objects on top (mostly toys and books). The walls are painted a light yellow colour."
%}

The chest of drawers gives me much more shelf space, and a lot of my clothes are now neatly packed inside.
I also rearranged some of my under-bed storage, which I was only half-using.
I've now repacked it so there's a lot more stuff under there, mostly stuff I need to keep but don't need to get to frequently -- like my guest bedding and some old paperwork.
In the new layout, I have easy access to one side and difficult access to the other, whereas before I had mediocre access to both sides.

At the other end of the room, the bright yellow adds a big burst of colour:

{%
  picture
  filename="P5080094.jpg"
  width="950"
  class="photo wide_img"
  alt="Looking towards the other end of the room, with the end of the bed just visible in the bottom right-hand corner. The wall is a bright, egg-yolk yellow. On the left-hand side is a mirror that's almost the full height of the wall. To the right of the mirror is a clothes rail with various clothes hanging from it, and a few pairs of shoes on the floor below. To the right of the clothes rail is the open bedroom door, hiding the corner behind it."
%}

The mirror is massive, and makes the room feel bigger.
It's also delightful for twirling in front of and admiring my sparkly outfits.
I always enjoy full-length when I stay in hotels, and I love having one in my bedroom – it's well worth the difficulty it took to fix it to the wall.

The clothes rail is new, and adds a splash of extra colour.
My clothes have a lot of bright colours, and I like having them on display, where I can enjoy them even when I'm not wearing them.
Next to it, the door is hiding my messy laundry basket and waste bin.
I can still get to them in a jiffy, but they're invisible most of the time.

You'll also notice my [cheetah cross-stitch](/2023/cats-cross-stitch-and-copyright/) on the wall – the yellow frame is a perfect match for my feature wall, which was a happy coincidence.
The picture was being framed while I was doing the painting, and I'd forgotten I had it on order.

I'll keep tweaking, including some photos on the wall, but in the meantime this has been a nice improvement to the room where I spend every not-waking hour.
