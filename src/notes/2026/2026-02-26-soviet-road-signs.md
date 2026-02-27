---
layout: note
title: Road signs in the Soviet union don't have circular heads
summary: Their heads are more a sort of rounded triangle shape, a bit like an oval or an egg.
date: 2026-02-27 19:54:09 +0000
topic: The world around us
---
Earlier this week, I saw a photo of a road sign that caught my eye.
The [original image][alamy] is a stock photo that I can't reproduce without a license, but here's a [freely available alternative][pexels] that shows the same sign:

<figure>
  {%
    picture
    filename="pexels-sejio402-27134572.jpg"
    width="750"
    alt="A construction site with a warning sign in the foreground. The sign is a red triangle with a yellow background, and a black stick figure shovelling something. The stick figure’s head is separated from their body, and a sort of oval shape."
  %}
  <figcaption>
    <a href="https://www.pexels.com/photo/traffic-signs-27134572/">Traffic signs</a> by Sergei Starostin on Pexels.
    Used under the <a href="https://www.pexels.com/license/">Pexels License</a>.
  </figcaption>
</figure>

I understood the sign immediately.
The details differ from the signs I'm used to, but it's recognisably a "men at work" sign meant to warn you about ongoing roadworks.

The man's head is an oval or egg shape, which is a style I'd not seen before.
I'm used to signs where the head is a perfect circle, or signs where the head is very distinct and stylised, like the [Ampelmännchen][wiki-ampel] seen at pedestrian crossings in Germany.

Writing this note, I realise there are road signs I'm familiar with that don't have rounded heads, but I'd never noticed.
For example, the UK's "children crossing" sign is meant to depict a girl with a non-circular haircut, but I'd never noticed it before.
(Although Margaret Calvert, the original designer, [refreshed the design][children-crossing] in 2016 to make the haircut more prominent.
Perhaps that's why I never noticed it.)

<style>
  .three_up {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--grid-gap);
    align-items: center;
    
    img {
      aspect-ratio: 1 !important;
      object-fit: cover;
    }
    
    svg {
      width: 100%;
    }
  }
</style>

<figure>
  <div class="three_up">
    {%
      picture
      filename="pexels-cesar-diaz-356944981-14290014.jpg"
      width="250"
      alt="A green sign with white lettering that says ‘Escaleras de emergencia’ with a stick figure of a running person. The stick figure’s head is detached from their body and a perfect circle."
    %}
    {%
      picture
      filename="pexels-jos-van-ouwerkerk-377363-1616781.jpg"
      width="250"
      alt="Red and green pedestrian crossing lights. The red light is a small figure with their arms oustretched and a wide brimmed hat, while the green light is the same figure walking, their head tipped back slightly."
    %}
    {%
      picture
      filename="Downpatrick_signs_(10)_August_2009.JPG"
      width="250"
      alt="A warning sign labelled ‘School’. The sign is a red triangle with a white background, and two stick figure children are walking from left to right. The right-hand child is slightly older and walking the younger child by the hand. Their heads are attached to their bodies, and the older girl’s head is non-circular, but in a subtle way."
    %}
  </div>
  <figcaption>
    Left to right:
    (1) a circular head on an emergency exit sign, photographed by <a href="https://www.pexels.com/photo/sign-on-white-wall-14290014/">Cesar Diaz</a>, used under the Pexels License;
    (2) the stylised head of the Ampelmännchen, photographed by <a href="https://www.pexels.com/photo/selective-focus-photography-of-traffic-light-1616781/">Jos van Ouwerkerk</a>, used under the Pexels License;
    (3) a school sign in Northern Ireland, photographed by <a href="https://commons.wikimedia.org/wiki/File:Downpatrick_signs_(10),_August_2009.JPG">Wikimedia user Ardfern</a>, used under CC BY-SA 3.0.
  </figcaption>
</figure>

It took me a bit of searching, but I eventually learnt that the egg-shaped head in the original image is a design choice that goes back at least as far as the Soviet Union.
Soviet road signs were specified by the GOST 10807-78 standard, released in 1980, and copies are [available online][gost-10807-78].

This sign is entry 1.23 Дорожные работы ("men at work").
The same head shape appears in signs like 1.20 Пешеходный переход ("pedestrian crossing") and 1.21 Дети ("children").

<figure>
  <div class="three_up">
    {%
      inline_svg
      filename="SU_road_sign_1.23.svg"
      class="dark_aware"
    %}
    {%
      inline_svg
      filename="RU_road_sign_1.22.svg"
      class="dark_aware"
    %}
    {%
      inline_svg
      filename="SU_road_sign_1.21.svg"
      class="dark_aware"
    %}
  </div>
  <figcaption>
    Soviet Union road sign SVGs by Wikimedia user Юкатан, used under CC BY-SA 3.0 (<a href="https://en.wikipedia.org/wiki/File:SU_road_sign_1.23.svg">1.23</a>,
     <a href="https://en.wikipedia.org/wiki/File:RU_road_sign_1.22.svg">1.20</a>, <a href="https://en.wikipedia.org/wiki/File:RU_road_sign_1.23.svg">1.21</a>)
  </figcaption>
</figure>

I looked through the rest of the standard, and there are some other signs I enjoyed and would like to see when I'm driving: the adorable cow in 1.24 Перегон скота ("cattle drive"), the bugle in 3.26 Подача звукового сигнала запрещена ("sounding the horn is prohibited"), and the gently swaying tree in 6.11 Место отдыха ("resting place").

<figure>
  <div class="three_up">
    {%
      inline_svg
      filename="RU_road_sign_1.26.svg"
      class="dark_aware"
    %}
    {%
      inline_svg
      filename="RU_road_sign_3.26.svg"
      class="dark_aware"
      style="width: 88%;"
    %}
    {%
      inline_svg
      filename="RU_road_sign_7.11.svg"
      class="dark_aware"
      style="width: 59%;"
    %}
  </div>
  <figcaption>
    Soviet Union road sign SVGs by Wikimedia user Юкатан, used under CC BY-SA 3.0 (<a href="https://en.wikipedia.org/wiki/File:RU_road_sign_1.26.svg">1.24</a>,
     <a href="https://en.wikipedia.org/wiki/File:RU_road_sign_3.26.svg">3.26</a>, <a href="https://en.wikipedia.org/wiki/File:RU_road_sign_7.11.svg">6.11</a>)
  </figcaption>
</figure>

These signs all look familiar even to non-Soviet drivers because of the [Vienna Convention on Road Signs and Signals][wiki-vienna-con], which established international standards for road signs and images.
The full text is [available online][vienna-con], and Annex 3 includes symbols to be used on road signs.
The detail was left to individual countries, but the broad shapes are meant to be consistent.

After the dissolution of the Soviet Union, road signs gradually diverged in the new countries.
I found a cool website by Bartolomeo Mecánico, which collects photos of different road signs around the world, and there's a page with examples of the men at work sign in [former Soviet countries][elve-men-at-work].

[alamy]: https://www.alamy.com/road-sign-are-going-construction-work-close-up-figurine-of-a-man-with-a-shovel-on-a-yellow-background-high-quality-photo-image433881547.html
[children-crossing]: https://www.transportxtra.com/publications/parking-review/news/48901/children-crossing-sign-refreshed-and-restored/
[elve-men-at-work]: https://www.elve.net/rmenru.htm
[gost-10807-78]: https://files.stroyinf.ru/Data/444/44457.pdf
[pexels]: https://www.pexels.com/photo/traffic-signs-27134572/
[vienna-con]: https://unece.org/DAM/trans/conventn/Conv_road_signs_2006v_EN.pdf
[wiki-ampel]: https://en.wikipedia.org/wiki/Ampelm%C3%A4nnchen
[wiki-vienna-con]: https://en.wikipedia.org/wiki/Vienna_Convention_on_Road_Signs_and_Signals
