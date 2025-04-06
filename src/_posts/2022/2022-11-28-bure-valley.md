---
layout: post
date: 2022-11-28 19:57:52 +0000
title: A day out at the Bure Valley Railway
summary: My photos from a delightful day on a steam railway with smol trains.
tags:
  - photography
  - trains
colors:
  css_light: "#101c75"
  css_dark:  "#238fd1"
index:
  feature: true
---

<!-- https://twitter.com/alexwlchan/status/1448052181886722053 -->

Last October, I had a day trip to the [Bure Valley Railway][bvrw], a narrow-gauge heritage railway in north Norfolk.
I came across it quite by chance -- I was driving through Aylsham to get to a B&B, and I spotted a sign pointing to the railway.
I checked the website for a timetable, bought myself a ticket, and set out for a day of steam trains.

I had a lovely time, and this post has a few of my photos.

<style type="x-text/scss">
  @use "mixins.scss" as *;

  /* See https://alexwlchan.net/2022/04/supposedly-simple-image-layout/ */
  .grid_4up {
    display: grid;
    grid-template-columns: calc(33% - 5px) calc(33% - 5px) calc(33% - 5px);
    grid-template-rows:    calc(50% - 5px) calc(50% - 5px);
    grid-gap: var(--grid-gap);
  }

  .grid_4up .upper {
    grid-row: 1 / 2;
  }

  .grid_4up .lower {
    grid-row: 2 / 2;
  }

  .grid_4up a img {
    width:  100%;
    height: 100%;
    object-fit: cover;
  }

  @media screen and (min-width: 750px) {
    .grid_4up .left.upper .picture_wrapper  { border-radius: 11px 0 0 0; }
    .grid_4up .left.upper img               { border-radius: 10px 0 0 0; }

    .grid_4up .right.upper .picture_wrapper { border-radius: 0 11px 0 0; }
    .grid_4up .right.upper img              { border-radius: 0 10px 0 0; }

    .grid_4up .right.lower .picture_wrapper { border-radius: 0 0 11px 0; }
    .grid_4up .right.lower img              { border-radius: 0 0 10px 0; }

    .grid_4up .left.lower .picture_wrapper  { border-radius: 0 0 0 11px; }
    .grid_4up .left.lower img               { border-radius: 0 0 0 10px; }

    .rounded_corners {
      .picture_wrapper { border-radius: 11px; }
      img              { border-radius: 10px; }
    }
  }

  @media screen and (min-width: 500px) {
    .grid_4up {
      aspect-ratio: 1;
    }
  }

  @media screen and (max-width: 500px) {
    .grid_4up {
      display: block;
    }

    .grid_4up .upper, .grid_4up .left {
      margin-bottom: 10px;
    }
  }

  .grid_3up {
    @include three_part_grid()
  }

  @media screen and (min-width: 750px) {
    .grid_3up {
      div:nth-child(1) .picture_wrapper { border-radius: 11px 0 0 11px; }
      div:nth-child(1) img              { border-radius: 10px 0 0 10px; }

      div:nth-child(2) .picture_wrapper { border-radius: 0 11px 0 0;    }
      div:nth-child(2) img              { border-radius: 0 10px 0 0;    }

      div:nth-child(3) .picture_wrapper { border-radius: 0 0 11px 0;    }
      div:nth-child(3) img              { border-radius: 0 0 10px 0;    }
    }
  }
</style>

<figure class="wide_img grid_3up">
  <div>
    {%
      picture
      filename="IMG_5744.jpg"
      alt="A black steam engine with a boxy shape, running on narrow rails. It has red fittings on the wheels and front bumper, and gold trim and decoration. It’s very shiny and well-cleaned! The cab is at the back of the train, a covered space with circular windows. It's pulling a single carriage, which is empty and has doors open towards the camera."
      width="622"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_5751.jpg"
      alt="A dark blue steam engine, sitting in the sidings. It has a burgundy nameplate “Blickling Hall”, the number “6”, and a head plate “Bure Valley Railway”. It’s sitting partway out of a large grey, box-shaped shed. Partially visible is a tender inside the shed – this is a tender engine. Like the black engine, this has red plates on the wheels and gold trim."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_6183.jpg"
      alt="A light blue steam engine sitting in a workshop. It’s a similar shape to the first engine – fairly box like. It doesn’t have any gold decorations, just a small nameplate in the centre  of the side. Around it are various boxes and tools, presumably used for maintaining the engines."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
</figure>

I started the day at Aylsham, and I arrived pretty early, so I saw the engines being wheeled out of the depot -- on this particular day, the black *John of Gaunt* and the dark blue *Blickling Hall* were both pulling trains.
Despite looking impeccable to my eye, they were still getting regular polishing and touch-ups from the volunteers.

As they were setting up, one of the drivers explained how the engines they're using are stored during the winter.
Their fires are left burning overnight, rather than being extinguished and re-lit each day.
This reduces stress on the mechanical components -- repeated up-and-down temperature changes would do more damage than keeping them warm.

Aylsham station has both passenger platforms and an engine shed.
The carriages themselves are pretty short, to match the engines, and they have a minimal step and several wheelchair spaces.

<figure class="wide_img grid_3up" style="grid-template-columns: calc(50% - 5px) calc(50% - 5px);">
  <div>
    {%
      picture
      filename="IMG_5747.jpg"
      alt="Looking down a train platform with two overhead signs for “Platform 3” and “Platform 2”. Sitting below the sign in platform 2 are a row of burgundy carriages. The carriages are about a metre high, with windows running along the top half, and split into doors for the different compartments. Some of the doors are labelled – for example, the closest door is labelled “Saloon”."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_5734.jpg"
      alt="A row of burgundy carriages, with the interiors more clearly visible -- there are five doors on each carriage, leading to a compartment with bench seats facing each other."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_5794.jpg"
      alt="An engine shed with three tracks leading in, with numbers overhead 1/2/3. Two engines are visible -- a dark blue engine and a light blue engine. To the left-hand side you can see the carriages with doors open, and passengers milling around and ready to board."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
</figure>

The line runs from Aylsham to Wroxham, and it's a 45 minute trip -- a proper railway, not just a garden train set.
That gave me plenty of time to sit back and enjoy the Norfolk countryside.
(I didn't take many pictures of the scenery, so you'll just have to take my word for it that it's pretty.)

<figure class="wide_img rounded_corners">
  {%
    picture
    filename="IMG_5816.jpg"
    alt="Looking out through a train carriage window at passing fields. It’s a field of mostly grass, with some trees along the edge in the distance, and various bushes and foliage appearing at the bottom of the window. There are also warning and safety stickers around the window, but they’re too dark to be easily legible."
    width="950"
    loading="lazy"
    link_to_original
  %}
</figure>

The carriages were quite comfortable, and I had a compartment all to myself.
In what's become a bit of a habit, the colour of my outfit matched the seat covers.
I never plan this, it just happens to me.
I showed the picture below to a close friend, who described as "[my] author photo", which feels distressingly accurate.

<figure class="wide_img rounded_corners">
  {%
    picture
    filename="IMG_5800.jpg"
    alt="A selfie! I’m sitting on one of the seats in a maroon-coloured jumper and a red scarf, with my right arm outstretched over the top of the seat. I’m wearing glasses, dark-coloured lipstick, and I have dark brown hair falling on either side of my face. I’m tilting my head a bit, and smiling – because my jumper is the same colour as the seat! (Well, almost.)"
    width="950"
    loading="lazy"
    link_to_original
  %}
</figure>

I got out at Wroxham for a brief wander.
I don't have any strong memories of the village, but I was able to get some lunch and wander into a few shops.
I was in a distinctly new place -- the train had taken me *somewhere*, which is what trains are meant to do.

At some point it started raining, so I retreated to the cover of the station, where I got to see the engines being prepped for the return journey.
First the drivers topped up the water tanks, then they drove the engines onto a turntable.
They had to turn them by hand (which looked like quite a workout!), so the engines were facing the opposite direction, ready to pull the return journey.

In these pictures you can see the drivers standing next to the trains, and hopefully this gives you a sense of scale -- they're still large engines, but small compared to mainline trains:

<figure class="wide_img grid_3up">
  <div>
    {%
      picture
      filename="IMG_5844.jpg"
      alt="A black, boxy steam engine with a driver filling it up using a blue hose. The driver is standing next to the train, close to their full height, and they're about as tall as the train."
      width="622"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_5852.jpg"
      alt="The black steam engine sitting on a turntable. At the far end is the driver, pushing against one of the handles to turn the train. Beyond the turntable are three tracks and the rest of the station."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_5921.jpg"
      alt="A dark blue engine sitting on the turntable. This is larger than the black engine, and it's taking two people pushing to turn it around. It looks like quite a strain!"
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
</figure>

Adding to the sense that the Bure Valley Railway is a transport link and not just a museum piece, the Wroxham terminus is right next to the mainline [Hoveton & Wroxham station](https://en.wikipedia.org/wiki/Hoveton_%26_Wroxham_railway_station).
You can walk between the stations, and standard gauge trains pass on the other side of the fence.
Of course, the drivers whistle at each other as they pass.

This let me get two of my favourite pictures of the day -- trains from both lines in the same shot.

First is this photo of *Blickling Hall* with a [Stadler FLIRT train][flirt] (a name which I enjoy for somebody's commitment to a bit; it's the same acronym in both English and German):

<figure class="wide_img rounded_corners">
  {%
    picture
    filename="IMG_5958.jpg"
    alt="The dark blue tender engine pulling its burgundy carriages, and on a parallel line above and to the left, a grey-and-red modern commuter train, which is much more sleek and streamlined."
    width="950"
    loading="lazy"
    link_to_original
  %}
</figure>

Second is this profile shot of *Blickling Hall* with a Class 37 diesel, which was pulling a line of tank wagons.
I love the contrast of the grimy diesel with the polished steamie:

<figure class="wide_img rounded_corners">
  {%
    picture
    filename="IMG_5934.jpg"
    alt="A profile shot of the dark blue tender engine and a large blue/turquoise diesel engine heading in the opposite direction on the track above."
    width="950"
    loading="lazy"
    link_to_original
  %}
</figure>

The engines create a lot of steam!
My camera could cut through the haze, but in the last photo in this next set, I literally couldn't see the engine through the fog (or anything else!).

There was a lot of steam coming from two tubes near the front of the engine, not through the main funnel.
I remember thinking that was odd on the day -- I did see steam coming out of the funnels, so they're not just decorative -- but I don't know enough about how steam engines work to know why steam comes out of two places.

<figure class="wide_img grid_3up">
  <div>
    {%
      picture
      filename="IMG_6027.jpg"
      alt="A black steam engine sitting on a turntable, blowing steam out of several pipes and holes. It’s facing towards the camera – it’s just been turned around from the other direction."
      width="622"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_5895.jpg"
      alt="A dark blue tender engine, blowing copious clouds of white steam from the very front of the engine. Behind it are several low-height coaches, which it’s just pulled along half the journey."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div>
    {%
      picture
      filename="IMG_5997.jpg"
      alt="The same dark blue engine, almost invisible behind the enormous cloud of smoke it’s producing."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
</figure>

Once I'd finished taking photos at Wroxham, I got back on the train for the return journey to Aylsham.
The weather had become thoroughly grey and rainy, so the scenery wasn't quite as pretty, but it was still a nice trip.

This Tuesday was actually the first day my employer had mandated a return to the office, and if I hadn't been on leave, I'd have been on a packed commuter service heading into central London.
Even with overcast skies, a steam train through Norfolk was a much better choice.

I really enjoyed seeing the trains at work, and I'm decidedly not a pro photographer -- but I still enjoyed taking a few "artsy" shots.
Hopefully these show what impeccable condition the engines are kept in -- even the tiny details are clean and shiny.

<figure class="wide_img grid_4up">
  <div class="upper left">
    {%
      picture
      filename="IMG_5782.jpg"
      alt="Looking down the side of the dark blue engine at a jaunty angle. I’m right up close to its side, so the train fills the photo."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div class="upper">
    {%
      picture
      filename="IMG_6081.jpg"
      alt="The very front of the black engine, with the face plate clearly visible. It has silver hands pointing to 5 o’clock, and a headlamp in front of the funnel."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div class="upper right">
    {%
      picture
      filename="IMG_5784.jpg"
      alt="Looking down the side of the black engine, with the tracks disappearing off into the distance. It’s a very skewed perspective."
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div class="left lower">
    {%
      picture
      filename="IMG_6086.jpg"
      alt="A close-up of some weird gizmo on the side of the black train. There are copper pipes and coils and brass valves… I have no idea what it does, but it looks cool!"
      width="500"
      loading="lazy"
      link_to_original
    %}
  </div>
  <div class="right lower" style="grid-column: 2 / span 2">
    {%
      picture
      filename="IMG_6088.jpg"
      alt="A side view of the black engine, including parts of the wheels and piston arrangement. The wheel parts are picked out in silver and red. So many exciting and graceful parts!"
      width="627"
      loading="lazy"
      link_to_original
    %}
  </div>
</figure>

They're really good looking trains.

<figure class="wide_img rounded_corners">
  {%
    picture
    filename="IMG_5994.jpg"
    alt="One more photo of the dark blue engine pulling a line of carriages, next to the sign for Wroxham Station."
    width="950"
    loading="lazy"
    link_to_original
  %}
</figure>

All the volunteers and staff I met were lovely.
I didn't talk to many of them -- I'm shy, and they were working -- but those I chatted to were very nice and generous with their knowledge, and keen to show off their railway.
Some heritage railways have a bit of a gatekeeper-y "real train geeks only" vibe, but I got none of that here.

I'll end with a photo of me, with windswept hair and a big smile, another favourite from the day:

<figure class="wide_img rounded_corners">
  {%
    picture
    filename="IMG_6211.jpg"
    alt="Another selfie! I’m a bit dishevelled, my hair is ruffled, and my hands are full of stuff. I’m standing in front of the station canopy, and I’m beaming. Huge smile."
    width="950"
    loading="lazy"
    link_to_original
  %}
</figure>

I had a wonderful day out -- beautiful enginers, gorgeous scenery, lovely volunteers.

There are only a few running days [left on this year's timetable][timetable], but if you enjoy trains and you can find a time I'd really recommend a visit.

[timetable]: https://www.bvrw.co.uk/timetable
[flirt]: https://en.wikipedia.org/wiki/Stadler_FLIRT
[bvrw]: https://www.bvrw.co.uk/
