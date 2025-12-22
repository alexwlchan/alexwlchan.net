---
layout: post
date: 2025-12-21 18:06:56 +0000
title: Drawing Truchet tiles in SVG
summary: Using parametric templates to draw Truchet tiles, then placing them randomly to create generative patterns.
tags:
  - drawing things
  - generative art
  - svg
---
<style>
  :root {
    --nav-bg-image-light: url("/static/2025/truchet-header-light.svg");
    --nav-bg-image-dark:  url("/static/2025/truchet-header-dark.svg");
  }
</style>

<link
  rel="preload"
  href="/static/2025/truchet-header-light.svg"
  as="image"
  type="image/svg"
  media="(prefers-color-scheme: light)"
/>
<link
  rel="preload"
  href="/static/2025/truchet-header-dark.svg"
  as="image"
  type="image/svg"
  media="(prefers-color-scheme: dark)"
/>

I recently read [Ned Batchelder's post][nedbat-truchet] about [Truchet tiles][wiki-truchet], which are square tiles that make nice patterns when you tile them on the plane.
I was experimenting with alternative headers for this site, and I thought maybe I’d use Truchet tiles.
I decided to scrap those plans, but I still had fun drawing some pretty pictures.

One of the simplest Truchet tiles is a square made of two colours:

<svg viewBox="0 0 0 0" style="display: none;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <symbol id="truchetSquare">
      <rect class="bg" width="100" height="100"/>
      <path class="fg" d="M 0 0 l 100 100 l -100 0 Z"/>
    </symbol>
    
    <symbol id="truchetSquare90">
      <use href="#truchetSquare" transform="rotate(90 50 50)"/>
    </symbol>
    
    <symbol id="truchetSquare180">
      <use href="#truchetSquare" transform="rotate(180 50 50)"/>
    </symbol>
    
    <symbol id="truchetSquare270">
      <use href="#truchetSquare" transform="rotate(270 50 50)"/>
    </symbol>
    
    <!--
      The base of the truchet tile is:
        - a white rectangle
        - four outer white "wings"
        - four inner black circles which connect to other tiles
     -->
    <svg id="base_background">
      <rect x="2" y="2" width="6" height="6"/>
      <circle cx="2" cy="2" r="2"/>
      <circle cx="8" cy="2" r="2"/>
      <circle cx="2" cy="8" r="2"/>
      <circle cx="8" cy="8" r="2"/>
    </svg>
    
    <svg id="base_foreground">
      <circle cx="2" cy="5" r="1"/>
      <circle cx="8" cy="5" r="1"/>
      <circle cx="5" cy="2" r="1"/>
      <circle cx="5" cy="8" r="1"/>
    </svg>

    <symbol id="base">
      <use href="#base_background" class="bg"/>
      <use href="#base_foreground" class="fg"/>
    </symbol>
    
    <symbol id="base-inverted">
      <use href="#base_background" class="fg"/>
      <use href="#base_foreground" class="bg"/>
    </symbol>
    
    <!--
      Define some of the basic shapes that are used in the Carlson
      truchet tile set:
      
      - a slash that goes from the top edge to the right edge
      - a wedge that goes from the top edge, to the right edge, to the centre
      - a horizontal bar that goes from the left edge to the right edge
    -->
    <path
      id="slash"
      d="M 4 2
         l 2 0
         a 2 2 0 0 0 2 2
         l 0 2
         a 4 4 0 0 1 -4 -4"/>
    <path
      id="wedge"
      d="M 4 2
         l 2 0
         a 2 2 0 0 0 2 2
         l 0 2
         l -4 0"/>
    <rect id="bar" x="2" y="4" width="6" height="2"/>
    
    <!--
      Define each of the Carlson tiles.
      
      Each tile has a list of basic shapes that draw the tile, and a list
      of extra rotations.
    -->
    <symbol id="carlsonFour">
      <use href="#base"/>
    </symbol>
    
    <symbol id="carlsonFour-inverted">
      <use href="#base-inverted"/>
    </symbol>
    
    <symbol id="carlsonX">
      <use href="#base"/>
      <g class="fg">
        <use href="#wedge"/>
        <use href="#wedge" transform="rotate(90 5 5)"/>
        <use href="#wedge" transform="rotate(180 5 5)"/>
        <use href="#wedge" transform="rotate(270 5 5)"/>
      </g>
    </symbol>
    
    <symbol id="carlsonX-inverted">
      <use href="#base-inverted"/>
      <g class="bg">
        <use href="#wedge"/>
        <use href="#wedge" transform="rotate(90 5 5)"/>
        <use href="#wedge" transform="rotate(180 5 5)"/>
        <use href="#wedge" transform="rotate(270 5 5)"/>
      </g>
    </symbol>
    
    <symbol id="carlsonT">
      <use href="#base"/>
      <g class="fg">
        <use href="#wedge"/>
        <use href="#wedge" transform="rotate(90 5 5)"/>
      </g>
    </symbol>
    
    <symbol id="carlsonT-inverted">
      <use href="#base-inverted"/>  
      <g class="bg">
        <use href="#wedge"/>
        <use href="#wedge" transform="rotate(90 5 5)"/>
      </g>
    </symbol>

    <symbol id="carlsonT-r90">
      <use href="#carlsonT" transform="rotate(90 5 5)"/>
    </symbol>
    
    <symbol id="carlsonT-r90-inverted">
      <use href="#carlsonT-inverted" transform="rotate(90 5 5)"/>
    </symbol>
  
    <symbol id="carlsonT-r180">
      <use href="#carlsonT" transform="rotate(180 5 5)"/>
    </symbol>
    
    <symbol id="carlsonT-r180-inverted">
      <use href="#carlsonT-inverted" transform="rotate(180 5 5)"/>
    </symbol>
  
    <symbol id="carlsonT-r270">
      <use href="#carlsonT" transform="rotate(270 5 5)"/>
    </symbol>
    
    <symbol id="carlsonT-r270-inverted">
      <use href="#carlsonT-inverted" transform="rotate(270 5 5)"/>
    </symbol>

    <symbol id="carlsonPlus">
      <use href="#base"/>        
      <g class="fg">        
        <use href="#bar"/>
        <use href="#bar" transform="rotate(90 5 5)"/>        
      </g>
    </symbol>
    
    <symbol id="carlsonPlus-inverted">
      <use href="#base-inverted"/>        
      <g class="bg">
        <use href="#bar"/>
        <use href="#bar" transform="rotate(90 5 5)"/>
      </g>
    </symbol>

    <symbol id="carlsonSlash">
      <use href="#base"/>
      <g class="fg">
        <use href="#slash"/>
        <use href="#slash" transform="rotate(180 5 5)"/>
      </g>
    </symbol>
      
    <symbol id="carlsonSlash-inverted">
      <use href="#base-inverted"/>
      <g class="bg">
        <use href="#slash"/>
        <use href="#slash" transform="rotate(180 5 5)"/>        
      </g>
    </symbol>
  
    <symbol id="carlsonSlash-r90">
      <use href="#carlsonSlash" transform="rotate(90 5 5)"/>
    </symbol>
    
    <symbol id="carlsonSlash-r90-inverted">
      <use href="#carlsonSlash-inverted" transform="rotate(90 5 5)"/>
    </symbol>

    <symbol id="carlsonMinus">
      <use href="#base"/>
      <use href="#bar" class="fg"/>
    </symbol>

    <symbol id="carlsonMinus-inverted">
      <use href="#base-inverted"/>
      <use href="#bar" class="bg"/>
    </symbol>
      
    <symbol id="carlsonMinus-r90">
      <use href="#carlsonMinus" transform="rotate(90 5 5)"/>
    </symbol>
    
    <symbol id="carlsonMinus-r90-inverted">
      <use href="#carlsonMinus-inverted" transform="rotate(90 5 5)"/>
    </symbol>

    <symbol id="carlsonFrown">
      <use href="#base"/>
      <use href="#slash" class="fg"/>
    </symbol>
      
    <symbol id="carlsonFrown-inverted">
      <use href="#base-inverted"/>
      <use href="#slash" class="bg"/>
    </symbol>
      
    <symbol id="carlsonFrown-r90">
      <use href="#carlsonFrown" transform="rotate(90 5 5)"/>
    </symbol>
    
    <symbol id="carlsonFrown-r90-inverted">
      <use href="#carlsonFrown-inverted" transform="rotate(90 5 5)"/>
    </symbol>
  
    <symbol id="carlsonFrown-r180">
      <use href="#carlsonFrown" transform="rotate(180 5 5)"/>
    </symbol>
    
    <symbol id="carlsonFrown-r180-inverted">
      <use href="#carlsonFrown-inverted" transform="rotate(180 5 5)"/>
    </symbol>
  
    <symbol id="carlsonFrown-r270">
      <use href="#carlsonFrown" transform="rotate(270 5 5)"/>
    </symbol>
    
    <symbol id="carlsonFrown-r270-inverted">
      <use href="#carlsonFrown-inverted" transform="rotate(270 5 5)"/>
    </symbol>
  
    <style>
      :root {
        --background: var(--white);
        --foreground: var(--black);
        --border:     var(--black);
      }
      
      @media (prefers-color-scheme: dark) {
        :root {
          --background: var(--black);
          --foreground: var(--white);
          --border:     var(--white);
        }
      }
      
      .bg {
        fill: var(--background);
      }
  
      .fg {
        fill: var(--foreground);
      }
      
      svg.border {
        border: 1px solid var(--border);
        
        /* hack to fix subpixel rendering bug in WebKit */
        background: var(--foreground);
      }
      
      .carlson_bg {
        fill: var(--block-border-color);
      }
      
      .carlson_grid {
        fill: none;
        stroke: var(--red);
        stroke-width: 0.2px;
        stroke-dasharray: 0.25, 0.25;
      }
      
      figure.columns_4 {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-gap: 1em;
      }
      
      @media screen and (max-width: 500px) {
        figure.columns_4 {
          grid-template-columns: repeat(2, 1fr);
        }
      }
    </style>
  </defs>
</svg>

<figure style="width: 500px;" class="columns_4">
  {% assign squares = "#truchetSquare #truchetSquare90 #truchetSquare180 #truchetSquare270" | split: " " %}
  {% for tile in squares %}
  <svg viewBox="0 0 100 100" style="max-width: 80px; width: 100%;" xmlns="http://www.w3.org/2000/svg" class="border">
    <use href="{{ tile }}"/>
  </svg>
  {% endfor %}
</figure>

These can be arranged in a regular pattern, but they also look nice when arranged randomly:

<style>
  #square_tiles_demo {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-column-gap: 1em;
    
    figcaption {
      grid-column: 1 / span 2;
    }
  }
</style>

<figure style="width: 500px;" id="square_tiles_demo">
  <svg viewBox="0 0 400 400" style="width: 100%;" xmlns="http://www.w3.org/2000/svg" class="border">  
    <use href="#truchetSquare"/>
    <use href="#truchetSquare" x="100"/>
    <use href="#truchetSquare" x="200"/>
    <use href="#truchetSquare" x="300"/>
    <use href="#truchetSquare"         y="100"/>
    <use href="#truchetSquare" x="100" y="100"/>
    <use href="#truchetSquare" x="200" y="100"/>
    <use href="#truchetSquare" x="300" y="100"/>
    <use href="#truchetSquare"         y="200"/>
    <use href="#truchetSquare" x="100" y="200"/>
    <use href="#truchetSquare" x="200" y="200"/>
    <use href="#truchetSquare" x="300" y="200"/>
    <use href="#truchetSquare"         y="300"/>
    <use href="#truchetSquare" x="100" y="300"/>
    <use href="#truchetSquare" x="200" y="300"/>
    <use href="#truchetSquare" x="300" y="300"/>
  </svg>
  <svg viewBox="0 0 400 400" style="width: 100%;" xmlns="http://www.w3.org/2000/svg" id="randomSquares" class="border">  
    <use href="{{ squares | sample }}"/>
    <use href="{{ squares | sample }}" x="100"/>
    <use href="{{ squares | sample }}" x="200"/>
    <use href="{{ squares | sample }}" x="300"/>
    <use href="{{ squares | sample }}"         y="100"/>
    <use href="{{ squares | sample }}" x="100" y="100"/>
    <use href="{{ squares | sample }}" x="200" y="100"/>
    <use href="{{ squares | sample }}" x="300" y="100"/>
    <use href="{{ squares | sample }}"         y="200"/>
    <use href="{{ squares | sample }}" x="100" y="200"/>
    <use href="{{ squares | sample }}" x="200" y="200"/>
    <use href="{{ squares | sample }}" x="300" y="200"/>
    <use href="{{ squares | sample }}"         y="300"/>
    <use href="{{ squares | sample }}" x="100" y="300"/>
    <use href="{{ squares | sample }}" x="200" y="300"/>
    <use href="{{ squares | sample }}" x="300" y="300"/>
  </svg>
</figure>

The tiles that really caught my eye were [Christopher Carlson's][carlson].
He created a collection of "winged tiles" that can be arranged with multiple sizes in the same grid.
A tile can be overlaid with four smaller tiles with inverted colours and extra wings, and the pattern still looks seamless.

He defined fifteen tiles, which are seven distinct patterns and then various rotations:

<style>
  #carlsonTiles {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-gap: var(--grid-gap);
    width: 650px;
  }
  
  @media screen and (max-width: 500px) {
    #carlsonTiles {
      grid-template-columns: repeat(3, 1fr);
    }
  }
</style>

<figure id="carlsonTiles">
  {% assign carlson_tiles = "#carlsonFour #carlsonT #carlsonT-r90 #carlsonT-r180 #carlsonT-r270 #carlsonPlus #carlsonSlash #carlsonSlash-r90 #carlsonMinus #carlsonMinus-r90 #carlsonX #carlsonFrown #carlsonFrown-r90 #carlsonFrown-r180 #carlsonFrown-r270" | split: " " %}
  {% for tile in carlson_tiles %}
    <svg viewBox="0 0 12 12" style="width: 100%;" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="12" height="12" class="carlson_bg"/>
      <use href="{{ tile }}" x="1" y="1"/>
      <rect x="3" y="3" width="6" height="6" class="carlson_grid"/>
    </svg>
  {% endfor %}
</figure>

The important thing to notice here is that every tile only really "owns" the red square in the middle.
When laid down, you add the "wings" that extend outside the tile -- this is what allows smaller tiles to seamlessly flow into the larger pattern.

Here's an example of a Carlson Truchet tiling:

<figure style="width: 650px;">
  <svg viewBox="0 0 48 24" xmlns="http://www.w3.org/2000/svg" class="border" id="gridlinesDemo">
    <g id="layer-1" transform="translate(-2 -2) ">
      <use href="#carlsonT-r90"/>
      <use href="#carlsonFour" y="6"/>
      <use href="#carlsonX" y="12"/>
      <use href="#carlsonPlus" x="6"/>
      <use href="#carlsonX" x="6" y="6"/>
      <use href="#carlsonMinus-r90" x="6" y="12"/>
      <use href="#carlsonFrown" x="6" y="18"/>
      <use href="#carlsonMinus-r90" x="12"/>
      <use href="#carlsonFour" x="12" y="6"/>
      <use href="#carlsonFour" x="12" y="12"/>
      <use href="#carlsonSlash" x="12" y="18"/>
      <use href="#carlsonMinus-r90" x="18" y="6"/>
      <use href="#carlsonPlus" x="18" y="12"/>
      <use href="#carlsonPlus" x="24"/>
      <use href="#carlsonT-r90" x="24" y="6"/>
      <use href="#carlsonX" x="24" y="12"/>
      <use href="#carlsonSlash" x="24" y="18"/>
      <use href="#carlsonX" x="30"/>
      <use href="#carlsonT" x="30" y="6"/>
      <use href="#carlsonFour" x="30" y="12"/>
      <use href="#carlsonFrown-r270" x="30" y="18"/>
      <use href="#carlsonFour" x="36"/>
      <use href="#carlsonMinus" x="36" y="12"/>
      <use href="#carlsonFour" x="36" y="18"/>
      <use href="#carlsonFrown-r270" x="42"/>
      <use href="#carlsonMinus-r90" x="42" y="6"/>
      <use href="#carlsonSlash-r90" x="42" y="12"/>
      <use href="#carlsonFrown-r180" x="42" y="18"/>
    </g>
    <g id="layer-2" transform="translate(-1 -1) scale(0.5)">
      <use href="#carlsonX-inverted" x="6" y="36"/>
      <use href="#carlsonMinus-inverted" y="42"/>
      <use href="#carlsonSlash-r90-inverted" x="36"/>
      <use href="#carlsonFour-inverted" x="42"/>
      <use href="#carlsonT-inverted" x="36" y="6"/>
      <use href="#carlsonFrown-r180-inverted" x="42" y="6"/>
      <use href="#carlsonX-inverted" x="42" y="36"/>
      <use href="#carlsonPlus-inverted" x="36" y="42"/>
      <use href="#carlsonPlus-inverted" x="72" y="12"/>
      <use href="#carlsonFour-inverted" x="78" y="12"/>
      <use href="#carlsonX-inverted" x="78" y="18"/>
    </g>
    <g id="layer-3" transform="translate(-0.5 -0.5) scale(0.25)">
      <use href="#carlsonFour" y="72"/>
      <use href="#carlsonX" x="6" y="72"/>
      <use href="#carlsonX" y="78"/>
      <use href="#carlsonFrown-r90" x="6" y="78"/>
      <use href="#carlsonMinus" x="12" y="84"/>
      <use href="#carlsonSlash" x="18" y="84"/>
      <use href="#carlsonPlus" x="12" y="90"/>
      <use href="#carlsonX" x="18" y="90"/>
      <use href="#carlsonT-r90" x="72" y="72"/>
      <use href="#carlsonFrown" x="78" y="72"/>
      <use href="#carlsonSlash" x="72" y="78"/>
      <use href="#carlsonFrown" x="78" y="78"/>
      <use href="#carlsonFrown" x="84" y="84"/>
      <use href="#carlsonMinus-r90" x="90" y="84"/>
      <use href="#carlsonMinus" x="84" y="90"/>
      <use href="#carlsonFour" x="90" y="90"/>
      <use href="#carlsonX" x="144" y="36"/>
      <use href="#carlsonX" x="150" y="36"/>
      <use href="#carlsonPlus" x="144" y="42"/>
      <use href="#carlsonT" x="150" y="42"/>
    </g>
    <line x1="6" y1="0" x2="6" y2="24" class="carlson_grid"/>
    <line x1="12" y1="0" x2="12" y2="24" class="carlson_grid"/>
    <line x1="18" y1="0" x2="18" y2="24" class="carlson_grid"/>
    <line x1="24" y1="0" x2="24" y2="24" class="carlson_grid"/>
    <line x1="30" y1="0" x2="30" y2="24" class="carlson_grid"/>
    <line x1="36" y1="0" x2="36" y2="24" class="carlson_grid"/>
    <line x1="42" y1="0" x2="42" y2="24" class="carlson_grid"/>
    
    <line x1="0" y1="6" x2="48" y2="6" class="carlson_grid"/>
    <line x1="0" y1="12" x2="48" y2="12" class="carlson_grid"/>
    <line x1="0" y1="18" x2="48" y2="18" class="carlson_grid"/>
    
    <line x1="21" y1="0" x2="21" y2="6" class="carlson_grid"/>
    <line x1="18" y1="3" x2="24" y2="3" class="carlson_grid"/>
    
    <line x1="39" y1="6" x2="39" y2="12" class="carlson_grid"/>
    <line x1="36" y1="9" x2="42" y2="9" class="carlson_grid"/>
    
    <line x1="37.5" y1="9" x2="37.5" y2="12" class="carlson_grid"/>
    <line x1="36" y1="10.5" x2="39" y2="10.5" class="carlson_grid"/>
    
    <line x1="3" y1="18" x2="3" y2="24" class="carlson_grid"/>
    <line x1="0" y1="21" x2="6" y2="21" class="carlson_grid"/>
    
    <line x1="1.5" y1="18" x2="1.5" y2="24" class="carlson_grid"/>
    <line x1="0" y1="19.5" x2="3" y2="19.5" class="carlson_grid"/>
    <line x1="0" y1="22.5" x2="6" y2="22.5" class="carlson_grid"/>
    <line x1="4.5" y1="21" x2="4.5" y2="24" class="carlson_grid"/>
    
    <line x1="21" y1="18" x2="21" y2="24" class="carlson_grid"/>
    <line x1="18" y1="21" x2="24" y2="21" class="carlson_grid"/>
    
    <line x1="19.5" y1="18" x2="19.5" y2="21" class="carlson_grid"/>
    <line x1="18" y1="19.5" x2="21" y2="19.5" class="carlson_grid"/>
    
    <line x1="22.5" y1="21" x2="22.5" y2="24" class="carlson_grid"/>
    <line x1="21" y1="22.5" x2="24" y2="22.5" class="carlson_grid"/>
  </svg>
  <style>
    .carlson_grid.hidden {
      display: none;
    }
  </style>
  <script>
    function toggleGridLines() {
      const isChecked = document.querySelector("#toggleGridLines").checked;
      document.querySelectorAll("#gridlinesDemo .carlson_grid").forEach(
        line => isChecked ? line.classList.remove("hidden") : line.classList.add("hidden")
      );
    }
  </script>
  <figcaption style="text-align: center;">
    <input type="checkbox" id="toggleGridLines" name="toggleGridLines" checked onchange="toggleGridLines()">
    <label for="toggleGridLines">
      show gridlines
    </label>
  </figcaption>
</figure>

Conceptually, we're giving the computer a bag of tiles, letting it pull tiles out at random, and watching what happens when it places them on the page.

In this post, I'll explain how to do this: filling the bag of tiles with parametric SVGs, then placing them randomly at different sizes.
I'm assuming you're familiar with SVG and JavaScript, but I'll explain the geometry as we go.

## Filling the bag of tiles

Although Carlson's set has fifteen different tiles, they're made of just four primitives, which I call the base, the slash, the wedge, and the bar.

<figure class="columns_4" style="width: 600px;">
  {% assign primitives = "#base #slash #wedge #bar" | split: " " %}
  {% for tile in primitives %}
    <svg viewBox="0 0 12 12" style="width: 100%;" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="12" height="12" class="carlson_bg"/>
      <use href="{{ tile }}" x="1" y="1" class="fg"/>
      <rect x="3" y="3" width="6" height="6" class="carlson_grid"/>
    </svg>
  {% endfor %}
</figure>

The first step is to write SVG definitions for each of these primitives that we can reuse.

Whenever I'm doing this sort of generative art, I like to define it parametrically -- writing a template that takes inputs I can change, so I can always see the relationship between the inputs and the result, and I can tweak the settings later.
There are lots of templating tools; I'm going to write pseudo-code rather than focus on one in particular.

For these primitives, there are two variables, which I call the *inner radius* and *outer radius*.
The outer radius is the radius of the larger wings on the corner of the tile, while the inner radius is the radius of the foreground components on the middle of each edge.
For the slash, the wedge, and the bar, the inner radius is half the width of the shape where it meets the edge of the tile.

This diagram shows the two variables, plus two variables I compute in the template:

<figure style="width: 500px;">
  <svg viewBox="0 0 28 17.2" style="width: 100%;" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <style>
        circle.blue { fill: var(--green); }
        .carlson_grid_blue {
          stroke: var(--green);
        }
      
        path.dimensions {
          stroke: currentColor;
          stroke-width: 0.1px;
        }
        
        .grid_thin {
          stroke-width: 0.15px;
        }
      </style>
    </defs>
    <g transform="translate(8 0)">
      <rect x="0" y="0" width="12" height="12" class="carlson_bg"/>
      <use href="#base" x="1" y="1" class="fg"/>
      <rect x="3" y="3" width="6" height="6" class="carlson_grid grid_thin"/>

      <circle cx="3" cy="3" r="2" class="carlson_grid carlson_grid_blue"/>
      <circle cx="9" cy="6" r="1" class="carlson_grid carlson_grid_blue"/>
    
      <circle cx="3" cy="3" r="0.25" class="blue"/>
      <circle cx="9" cy="6" r="0.25" class="blue"/>
    </g>
    
    <text x="6.5" y="2" font-size="1px" dominant-baseline="middle" text-anchor="end">outer radius</text>
    <path class="dimensions"
      d="M 6.8 3
         l 0.6 0 l -0.3 0
         l 0 -2
         l -0.3 0
         l 0.6 0
         l -0.3 0
         l 0 2
         l -0.3 0"/>
    
    <path class="dimensions"
      d="M 20.6 6
         l 0.6 0 l -0.3 0
         l 0 -1
         l -0.3 0
         l 0.6 0
         l -0.3 0
         l 0 1
         l -0.3 0"/>
    <text x="21.5" y="5.5" font-size="1px" dominant-baseline="middle" text-anchor="start">inner radius</text>
    
    <path class="dimensions"
      d="M 11 12.6
         l 0 0.6 l 0 -0.3
         l 6 0
         l 0 -0.3
         l 0 0.6
         l 0 -0.3
         l -6 0
         l 0 -0.3"/>
    <text x="14" y="14.2" font-size="1px" dominant-baseline="text-top" text-anchor="middle">tile size</text>
  
    <path class="dimensions"
      d="M 9 14.8
         l 0 0.6 l 0 -0.3
         l 2 0
         l 0 -0.3
         l 0 0.6
         l 0 -0.3
         l -2 0
         l 0 -0.3"/>
    <text x="10" y="16.6" font-size="1px" dominant-baseline="text-top" text-anchor="middle">padding</text>
  </svg>
</figure>

Here's the template for these primitives:

```xml
{%- raw %}
<!-- What's the length of one side of the tile, in the red dashed area?
     tileSize = (innerR + outerR) * 2 -->

<!-- How far is the tile offset from the edge of the symbol/path?
     padding = max(innerR, outerR) -->

<symbol id="base">
  <!--
    For the background, draw a square that fills the whole tile, then
    four circles on each of the corners.
    -->
  <g class="background">
    <rect x="{{ padding }}" y="{{ padding }}" width="{{ tileSize }}" height="{{ tileSize }}"/>
    <circle cx="{{ padding }}"            cy="{{ padding }}"            r="{{ outerR }}"/>
    <circle cx="{{ padding + tileSize }}" cy="{{ padding }}"            r="{{ outerR }}"/>
    <circle cx="{{ padding }}"            cy="{{ padding + tileSize }}" r="{{ outerR }}"/>
    <circle cx="{{ padding + tileSize }}" cy="{{ padding + tileSize }}" r="{{ outerR }}"/>
  </g>
  <!--
    For the foreground, draw four circles on the middle of each tile edge.
    -->
  <g class="foreground">
    <circle cx="{{ padding }}"            cy="{{ tileSize / 2 }}"       r="{{ innerR }}"/>
    <circle cx="{{ padding + tileSize }}" cy="{{ tileSize / 2 }}"       r="{{ innerR }}"/>
    <circle cx="{{ tileSize / 2 }}"       cy="{{ padding }}"            r="{{ innerR }}"/>
    <circle cx="{{ tileSize / 2 }}"       cy="{{ padding + tileSize }}" r="{{ innerR }}"/>
  </g>
</symbol>

<!--
  Slash:
    - Move to the top edge, left-hand vertex of the slash
    - Line to the top edge, right-hand vertex
    - Smaller arc to left egde, upper vertex
    - Line down to left edge, lower vertex
    - Larger arc back to the start
-->
<path
  id="slash"
  d="M {{ padding + outerR }} {{ padding }}
     l {{ 2 * innerR }} 0
     a {{ outerR }} {{ outerR }} 0 0 0 {{ outerR }} {{ outerR }}
     l 0 {{ 2 * innerR }}
     a {{ innerR*2 + outerR }} {{ innerR*2 + outerR }} 0 0 1 {{ -innerR*2 - outerR }} {{ -innerR*2 - outerR }}"/>

<!--
  wedge:
    - Move to the top edge, left-hand vertex of the slash
    - Line to the top edge, right-hand vertex
    - Smaller arc to left egde, upper vertex
    - Line to centre of the tile
    - Line back to the start
-->
<path
  id="wedge"
  d="M {{ padding + outerR }} {{ padding }}
     l {{ 2 * innerR }} 0
     a {{ outerR }} {{ outerR }} 0 0 0 {{ outerR }} {{ outerR }}
     l {{ 0 }} {{ 2 * innerR }}
     l {{ -innerR*2 - outerR }} 0"/>

<!--
  Bar: horizontal rectangle that spans the tile width and is the same height
  as a circle on the centre of an edge.
  -->
<rect
  id="bar"
  x="{{ padding }}" y="{{ padding + outerR }}"
  width="{{ tileSize }}"
  height="{{ 2 * innerR }}"/>{% endraw %}
```

The `foreground`/`background` classes are defined in CSS, so I can choose the colour of each.

This template is more verbose than the rendered SVG, but I can see all the geometric expressions -- I find this far more readable than a file full of numbers.
This also allows easy experimentation -- I can change an input, re-render the template, and instantly see the new result.

I can then compose the tiles by referencing these primitive shapes with a [`<use>` element][mdn-use-element].
For example, the "T" tile is made of a base and two wedge shapes:

```xml
{%- raw %}
<!-- The centre of rotation is the centre of the whole tile, including padding.
     centreRotation = outerR + innerR -->

<symbol id="carlsonT">
  <use href="#base"/>
  <use href="#wedge" class="foreground"/>
  <use href="#wedge" class="foreground" transform="rotate(90 {{ centreRotation }} {{ centreRotation }})"/>
</symbol>{% endraw %}
```

After this, I write a similar `<symbol>` definition for all the other tiles, plus inverted versions that swap the background and foreground.

Now we have a bag full of tiles, let's tell the computer how to place them.

## Placing the tiles on the page

Suppose the computer has drawn a tile from the bag.
To place it on the page, it needs to know:

*   The *x*, *y* position, and
*   The layer -- should it place a full-size tile, or is it a smaller tile subdividing a larger tile

From these two properties, it can work out everything else -- in particular, whether to invert the tile, and how large to scale it.

The procedure is straightforward: get the position of all the tiles in a layer, then decide if any of those tiles are going to be subdivided into smaller tiles.
Use those to position the next layer, and repeat.
Continue until the next layer is empty, or you hit the maximum number of layers you want.

Here's an implementation of that procedure in JavaScript:

{% code lang="javascript" names="0:getTilePositions 1:columns 2:rows 3:tileSize 4:maxLayers 5:subdivideChance 6:tiles 7:i 11:j 24:layer 28:previousLayer 35:layerTileSize 40:tile" %}
function getTilePositions({
  columns,
  rows,
  tileSize,
  maxLayers,
  subdivideChance,
}) {
  let tiles = [];
  
  // Draw layer 1 of tiles, which is a full-sized tile for
  // every row and column.
  for (i = 0; i < columns; i++) {
    for (j = 0; j < rows; j++) {
      tiles.push({ x: i * tileSize, y: j * tileSize, layer: 1 });
    }
  }
  
  // Now go through each layer up to maxLayers, and decide which
  // tiles from the previous layer to subdivide into four smaller tiles.
  for (layer = 2; layer <= maxLayers; layer++) {
    let previousLayer = tiles.filter(t => t.layer === layer - 1);
    
    // The size of tiles halves with each layer.
    // On layer 2, the tiles are 1/2 the size of the top layer.
    // On layer 3, the tiles are 1/4 the size of the top layer.
    // And so on.
    let layerTileSize = tileSize * (0.5 ** (layer - 1));
    
    previousLayer.forEach(tile => {
      if (Math.random() < subdivideChance) {
        tiles.push(
          { layer, x: tile.x,                 y: tile.y                 },
          { layer, x: tile.x + layerTileSize, y: tile.y                 },
          { layer, x: tile.x,                 y: tile.y + layerTileSize },
          { layer, x: tile.x + layerTileSize, y: tile.y + layerTileSize },
        )
      }
    })
  }
  
  return tiles;
}
{% endcode %}

Once we know the positions, we can lay them out in our SVG element.

We need to make sure we scale down smaller tiles to fit, and adjust the position -- remember each Carlson tile only "owns" the red square in the middle, and the wings are meant to spill out of the tile area.
Here's the code:

{% code lang="javascript" names="0:drawTruchetTiles 1:svg 2:tileTypes 3:tilePositions 4:padding 8:tileName 25:scale 28:adjustment" %}
function drawTruchetTiles(svg, tileTypes, tilePositions, padding) {
  tilePositions.forEach(c => {
    // We need to invert the tiles every time we subdivide, so we use
    // the inverted tiles on even-numbered layers.
    let tileName = c.layer % 2 === 0
      ? tileTypes[Math.floor(Math.random() * tileTypes.length)] + "-inverted"
      : tileTypes[Math.floor(Math.random() * tileTypes.length)];
      
    // The full-sized tiles are on layer 1, and every layer below
    // that halves the tile size.
    const scale = 0.5 ** (c.layer - 1);
    
    // We don't want to draw a tile exactly at (x, y) because that
    // would include the wings -- we add negative padding to offset.
    //
    // At layer 1, adjustment = padding
    // At layer 2, adjustment = padding * 1/2
    // At layer 3, adjustment = padding * 1/2 + padding * 1/4
    //
    const adjustment = -padding * Math.pow(0.5, c.layer - 1);

    svg.innerHTML += `
      <use
        href="${tileName}"
        x="${c.x / scale}"
        y="${c.y / scale}"
        transform="translate(${adjustment} ${adjustment}) scale(${scale})"/>`;
  });
}
{% endcode %}

<script>
  function getTilePositions({
    columns,
    rows,
    tileSize,
    maxLayers,
    subdivideChance,
  }) {
    let tiles = [];
  
    // Draw layer 1 of tiles, which is a full-sized tile for
    // every row and column.
    for (i = 0; i < columns; i++) {
      for (j = 0; j < rows; j++) {
        tiles.push({
          x: i * tileSize,
          y: j * tileSize,
          layer: 1,
        });
      }
    }
  
    // Now go through each layer up to maxLayers, and decide which
    // tiles from the previous layer to subdivide into four smaller tiles.
    for (layer = 2; layer <= maxLayers; layer++) {
      let previousLayer = tiles.filter(t => t.layer === layer - 1);
    
      // The size of tiles halves with each layer.
      // On layer 2, the tiles are 1/2 the size of the top layer.
      // On layer 3, the tiles are 1/4 the size of the top layer.
      // And so on.
      let layerTileSize = tileSize * (0.5 ** (layer - 1));
    
      previousLayer.forEach(tile => {
        if (Math.random() < subdivideChance) {
          tiles.push(
            { layer, x: tile.x,                 y: tile.y,                },
            { layer, x: tile.x + layerTileSize, y: tile.y,                },
            { layer, x: tile.x,                 y: tile.y + layerTileSize },
            { layer, x: tile.x + layerTileSize, y: tile.y + layerTileSize },
          )
        }
      })
    }
  
    return tiles;
  }

  function drawTruchetTiles(svg, tileTypes, tilePositions, padding) {
    tilePositions.forEach(c => {
      // We need to invert the tiles every time we subdivide, so we use
      // the inverted tiles on even-numbered layers.
      let tileName = c.layer % 2 === 0
        ? tileTypes[Math.floor(Math.random() * tileTypes.length)] + "-inverted"
        : tileTypes[Math.floor(Math.random() * tileTypes.length)];
      
      // The full-sized tiles are on layer 1, and every layer below
      // that halves the tile size.
      const scale = 0.5 ** (c.layer - 1);
    
      // We don't want to draw a tile exactly at (x, y) because that
      // would include the wings -- we add negative padding to offset.
      //
      // At layer 1, adjustment = padding
      // At layer 2, adjustment = padding * 1/2
      // At layer 3, adjustment = padding * 1/2 + padding * 1/4
      //
      const adjustment = -padding * Math.pow(0.5, c.layer - 1);

      svg.innerHTML += `
        <use
          href="${tileName}"
          x="${c.x / scale}"
          y="${c.y / scale}"
          transform="translate(${adjustment} ${adjustment}) scale(${scale})"/>`;
    });
  }
  
  var customColors = false;
  
  function redrawRandomCarlson() {
    console.log('redrawRandomCarlson');
    const innerRadius = 1;
    const outerRadius = 2;
    const tileTypes = "#carlsonFour #carlsonT #carlsonT-r90 #carlsonT-r180 #carlsonT-r270 #carlsonPlus #carlsonSlash #carlsonSlash-r90 #carlsonMinus #carlsonMinus-r90 #carlsonX #carlsonFrown #carlsonFrown-r90 #carlsonFrown-r180 #carlsonFrown-r270".split(" ");
    const svg = document.querySelector("#randomCarlson");
    const padding = Math.max(innerRadius, outerRadius);
    const tilePositions = getTilePositions({
      rows: 4,
      columns: 8,
      tileSize: 6,
      maxLayers: 3,
      subdivideChance: 0.2,
    });
    drawTruchetTiles(svg, tileTypes, tilePositions, padding);
    
    /* Select some random colours to show on the diagram */
    const rootStyles = getComputedStyle(document.documentElement);
    const colorVarNames = ["--white", "--black", "--red", "--green", "--blue", "--magenta", "--yellow"];
    const colors = colorVarNames.map(n => rootStyles.getPropertyValue(n));
    
    if (!customColors) {
      /* Make sure we pick different foreground / background colours. */
      let foreground = colors[Math.floor(Math.random() * colors.length)];
      
      let background = colors[Math.floor(Math.random() * colors.length)];
      while (foreground === background) {
        background = colors[Math.floor(Math.random() * colors.length)]
      }
      
      const svg = document.querySelector("#randomCarlson");
      
      svg.style.setProperty("--foreground", foreground);
      svg.style.setProperty("--background", background);
      
      document.querySelector("#foreground").value = foreground;
      document.querySelector("#background").value = background;
    }
  }
  
  document.addEventListener("DOMContentLoaded", redrawRandomCarlson);
</script>
  
The padding was fiddly and took me a while to work out, but now it works fine.
The tricky bits are another reason I like defining my SVGs parametrically -- it forces me to really understand what's going on, rather than tweaking values until I get something that looks correct.



## Demo

Here's a drawing that uses this code to draw Carlson truchet tiles:

<figure style="width: 650px;">
  <svg viewBox="0 0 48 24" xmlns="http://www.w3.org/2000/svg" class="border" id="randomCarlson">
    <g id="layer-1" transform="translate(-2 -2) ">
      <use href="#carlsonT-r90"/>
      <use href="#carlsonFour" y="6"/>
      <use href="#carlsonX" y="12"/>
      <use href="#carlsonPlus" x="6"/>
      <use href="#carlsonX" x="6" y="6"/>
      <use href="#carlsonMinus-r90" x="6" y="12"/>
      <use href="#carlsonFrown" x="6" y="18"/>
      <use href="#carlsonMinus-r90" x="12"/>
      <use href="#carlsonFour" x="12" y="6"/>
      <use href="#carlsonFour" x="12" y="12"/>
      <use href="#carlsonSlash" x="12" y="18"/>
      <use href="#carlsonMinus-r90" x="18" y="6"/>
      <use href="#carlsonPlus" x="18" y="12"/>
      <use href="#carlsonPlus" x="24"/>
      <use href="#carlsonT-r90" x="24" y="6"/>
      <use href="#carlsonX" x="24" y="12"/>
      <use href="#carlsonSlash" x="24" y="18"/>
      <use href="#carlsonX" x="30"/>
      <use href="#carlsonT" x="30" y="6"/>
      <use href="#carlsonFour" x="30" y="12"/>
      <use href="#carlsonFrown-r270" x="30" y="18"/>
      <use href="#carlsonFour" x="36"/>
      <use href="#carlsonMinus" x="36" y="12"/>
      <use href="#carlsonFour" x="36" y="18"/>
      <use href="#carlsonFrown-r270" x="42"/>
      <use href="#carlsonMinus-r90" x="42" y="6"/>
      <use href="#carlsonSlash-r90" x="42" y="12"/>
      <use href="#carlsonFrown-r180" x="42" y="18"/>
    </g>
    <g id="layer-2" transform="translate(-1 -1) scale(0.5)">
      <use href="#carlsonX-inverted" x="6" y="36"/>
      <use href="#carlsonMinus-inverted" y="42"/>
      <use href="#carlsonSlash-r90-inverted" x="36"/>
      <use href="#carlsonFour-inverted" x="42"/>
      <use href="#carlsonT-inverted" x="36" y="6"/>
      <use href="#carlsonFrown-r180-inverted" x="42" y="6"/>
      <use href="#carlsonX-inverted" x="42" y="36"/>
      <use href="#carlsonPlus-inverted" x="36" y="42"/>
      <use href="#carlsonPlus-inverted" x="72" y="12"/>
      <use href="#carlsonFour-inverted" x="78" y="12"/>
      <use href="#carlsonX-inverted" x="78" y="18"/>
    </g>
    <g id="layer-3" transform="translate(-0.5 -0.5) scale(0.25)">
      <use href="#carlsonFour" y="72"/>
      <use href="#carlsonX" x="6" y="72"/>
      <use href="#carlsonX" y="78"/>
      <use href="#carlsonFrown-r90" x="6" y="78"/>
      <use href="#carlsonMinus" x="12" y="84"/>
      <use href="#carlsonSlash" x="18" y="84"/>
      <use href="#carlsonPlus" x="12" y="90"/>
      <use href="#carlsonX" x="18" y="90"/>
      <use href="#carlsonT-r90" x="72" y="72"/>
      <use href="#carlsonFrown" x="78" y="72"/>
      <use href="#carlsonSlash" x="72" y="78"/>
      <use href="#carlsonFrown" x="78" y="78"/>
      <use href="#carlsonFrown" x="84" y="84"/>
      <use href="#carlsonMinus-r90" x="90" y="84"/>
      <use href="#carlsonMinus" x="84" y="90"/>
      <use href="#carlsonFour" x="90" y="90"/>
      <use href="#carlsonX" x="144" y="36"/>
      <use href="#carlsonX" x="150" y="36"/>
      <use href="#carlsonPlus" x="144" y="42"/>
      <use href="#carlsonT" x="150" y="42"/>
    </g>
  </svg>
  <figcaption style="display: grid; grid-template-columns: auto auto; grid-column-gap: var(--grid-gap);">
    <input type="color" id="foreground" name="foreground" value="#000000" style="margin-left: auto;" onchange="setDemoColours()">
    <label for="foreground" style="margin-right: auto;">foreground</label>
    <input type="color" id="background" name="background" value="#ffffff" style="margin-left: auto;" onchange="setDemoColours()">
    <label for="background" style="margin-right: auto;">background</label>
    <div style="grid-column: 1 / span 2; text-align: center;">
      <button onclick="redrawRandomCarlson()">draw new shapes</button>
    </div>
  </figcaption>
  <script>
    function setDemoColours() {
      const foreground = document.querySelector("#foreground").value;
      const background = document.querySelector("#background").value;
      
      const svg = document.querySelector("#randomCarlson");
      
      svg.style.setProperty("--foreground", foreground);
      svg.style.setProperty("--background", background);
      
      customColors = true;
    }
  </script>
</figure>

It was generated by your browser when you loaded the page, and there are so many possible combinations that it’s a unique image.

If you want a different picture, reload the page, or tell the computer to <a href="#randomCarlson" onclick="redrawRandomCarlson()">draw some new tiles</a>.

These pictures put me in mind of an alien language -- something I'd expect to see etched on the wall in a sci-fi movie.
I can imagine eyes, tentacles, roads, and warnings left by a long-gone civilisation.

It's fun, but not really the tone I want for this site -- I've scrapped my plan to use Truchet tiles as header images.
I'll save them for something else, and in the meantime, I had a lot of fun.

[nedbat-truchet]: https://nedbatchelder.com/blog/202208/truchet_images.html
[wiki-truchet]: https://en.wikipedia.org/wiki/Truchet_tile
[carlson]: https://christophercarlson.com/portfolio/multi-scale-truchet-patterns/
[mdn-use-element]: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/use
