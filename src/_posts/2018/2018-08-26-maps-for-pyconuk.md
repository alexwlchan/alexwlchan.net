---
layout: post
date: 2018-08-26 07:10:28 +0000
title: Making the venue maps for PyCon UK
summary: A quick braindump of my thoughts from drawing some venue maps for PyCon UK.
tags: pyconuk graphic-design
theme:
  card_type: summary_large_image
  image: /images/2018/venue-map_first.png
---

We've just published [the venue information][venue] for this year's PyCon UK.
The page includes maps of Cardiff City Hall (where the conference is hosted), which were a suggestion from Kirk, and a lot of fun to make.

This is what the maps look like:

<figure>
  <div style="max-width: 48%; display: inline-block;">
  {%
    image :filename => "venue-map_ground.png",
    :alt => "A map of the ground floor of City Hall."
  %}
  </div>
  <div style="max-width: 48%; display: inline-block;">
  {%
    image :filename => "venue-map_first.png",
    :alt => "A map of the first floor of City Hall."
  %}
  </div>
  <figcaption>
    Internal maps of Cardiff City Hall.
    Left: ground floor.
    Right: first floor.
    The yellow and blue are the same colours as used on the PyCon UK website.
  </figcaption>
</figure>

A good internal map helps people find their way around an unfamiliar venue, and can save organisers a lot of questions!
Chloe runs the registration desk, and I think she spent half of last year's conference giving out directions.
A map can also translate between venue room names and conference terminology, which don't always match.

[conf]: /2018/08/inclusive-conferences/#clear-internal-signage

Since a few people were asking, this is how I made the maps:

<ol>
  <li>
    <p>
      The <a href="https://www.cardiffcityhall.com/rooms/">Cardiff City Hall website</a> has floor plan PDFs showing the location of each room.
      For example, here&rsquo;s their floorplan showing the Marble Hall:
    </p>

    {%
      image :filename => "marble_hall.png",
      :alt => "A map of Cardiff City Hall, with the Marble Hall highlighted in red.",
      :style => "border: 1px solid #D3D3D3;"
    %}

    <p>
      I saved a floorplan for both floors, and used <a href="https://flyingmeat.com/acorn/">Acorn</a> to remove the text at the top and the background image of City Hall.
      This gave me a pair of blank floor plans.
    </p>

    <p>
      Here's the blank map I had for the first floor:
    </p>

    {%
      image :filename => "first_floor_blank.png",
      :alt => "Another map of City Hall, with one room highlighted in red, and all the text removed.",
      :style => "border: 1px solid #D3D3D3;"
    %}
  </li>
  <li>
    <p>
      I coloured in all the rooms we're using, and added text labels.
      This is what I labelled:
    </p>

    <ul>
      <li>Every room being used for sessions</li>
      <li>The toilets, and which ones are accessible</li>
      <li>The quiet room</li>
      <li>The creche</li>
      <li>The lift</li>
    </ul>

    <p>
      I used the conference blue and yellow, rather than the City Hall shade of red -- a bit of branding makes it clearer these are PyCon-specific.
    </p>

    <p>
      Note that they're labelled according to the PyCon terminology, not the City Hall room names.
      We use Room G for the creche, but most people don't know that, so it's labelled "creche".
      Similarly, the quiet room is really the council chamber, but not everybody would know to look for "council chamber" on a map.
    </p>

    <p>
      In a few cases, I tweaked the layout to make the label fit, or make something easier to find.
      For example, the lift is larger than it appears on the plans.
    </p>

    <p>
      (I considered labelling the toilets as male/female, but we have non-binary and trans attendees, and our bathroom policy is "use whichever toilet you feel most comfortable with".
      We're stuck with the gendered bathrooms because of City Hall, but I figured I could avoid perpetuating that on the maps.)
    </p>
  </li>
  <li>
    <p>
      I added the help desk, which doesn&rsquo;t appear on any City Hall floorplans, but is a key part of the conference!
    </p>
  </li>
  <li>
    <p>
      I lightly shaded the stairs, hallways, and bits of corridor I expect people to use or get to the rooms.
      I&rsquo;m trying to say &ldquo;you shouldn&rsquo;t need to go outside these areas&rdquo;.
    </p>
  </li>
  <li>
    <p>
      These floorplans are very accurate depictions of the building, showing all the internal rooms and doorways.
      Outside the main conference area, this detail is just noise that clutters the map, so I erased a bunch of internal walls to clean up the map.
    </p>

    <p>
      If you compare the PDF for the Marble Hall and my first floor map, you might see some of the walls I removed.
    </p>
  </li>
</ol>

For now, the maps are just on the conference website.
I'm hoping to get some printouts done, and put them around the venue with little red "you are here" dots -- but I don't know if we're allowed to put up posters yet.
Even so, this was a nice little project to work on, and I think it's an improvement on what we had last year.

[venue]: https://2018.pyconuk.org/venue/
