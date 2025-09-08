#!/usr/bin/env python3

import math

r = 75

margin = 45

x1 = margin + r
y1 = margin + r

x2 = x1 + r * 4

unit = 5

w = unit * 13.75

x_unit = unit
y_unit = unit * 3/4

h = x_unit * 11 * 5/8

y_unit = h / 9

x = f"""
<svg viewBox="0 0 {x2 + r + margin} {y1 + r + margin}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="dark_aware">
  <defs>
    <style>
      line, path {{
        stroke: currentColor;
        stroke-width: 4;
        stroke-linecap: round;
        fill: none;
      }}

      circle {{
        stroke-width: 3;
        stroke: grey;
        fill: none;
      }}
      
      #baseImage rect {{
        stroke: currentColor;
        fill: yellow;
      }}

      text {{
        stroke: none;
        text-anchor: middle;
        dominant-baseline: middle;
        fill: currentColor;
      }}
    </style>

    <g id="baseImage">
      <rect width="{w}" height="{h}"/>
      
      <path d="M {x_unit * 2} {y_unit * 2}
               l {x_unit * 2.5} 0 m {x_unit * -2.5} 0
               l 0 {y_unit * 5} m 0 {y_unit * -2.5}
               l {x_unit * 2} 0"/>
      <path d="M {x_unit * 6.25} {y_unit * 2}
               l 0 {y_unit * 5}
               m {x_unit * 2.5} 0
               l {x_unit * -2.5} 0"/>
      <path d="M {x_unit * 9.5} {y_unit * 2}
               l {x_unit * 1.25} {y_unit * 2.5}
               l {x_unit * 1.25} {y_unit * -2.5}
               m {x_unit * -1.25} {y_unit * 2.5}
               l 0 {y_unit * 2.5}"/>
    </g>
  </defs>

  <circle cx="{x1}" cy="{y1}" r="{r}"  stroke-dasharray="3,3" />
  
  <text x="{x1}" y="{y1 - r - h * 6/7}">1</text>
  <text x="{x1 - r - h * 6/7}" y="{y1}">6</text>
  <text x="{x1 + r + h * 6/7}" y="{y1}">8</text>
  <text x="{x1}" y="{y1 + r + h}">3</text>

  <use xlink:href="#baseImage" transform="translate({x1 - w / 2} {y1 - r - h/2})" />
  <use xlink:href="#baseImage" transform="translate({x1 + r - w/2} {y1 - h / 2}) rotate(90 {w / 2} {h / 2}) " />
  <use xlink:href="#baseImage" transform="translate({x1 - w / 2} {y1 + r - h/2 }) rotate(180 {w / 2} {h / 2})" />
  <use xlink:href="#baseImage" transform="translate({x1 - r - w/2} {y1 - h/2}) rotate(270 {w / 2} {h / 2})" />

  <text x="{x2}" y="{y1 - r - 6/7 * h}">2</text>
  <text x="{x2 - r - 6/7 * h}" y="{y1}">5</text>
  <text x="{x2 + r + 6/7 * h}" y="{y1}">7</text>
  <text x="{x2}" y="{y1 + r + h}">4</text>

  <circle cx="{x2}" cy="{y1}" r="{r}" stroke-dasharray="3,3" />
  
  <use xlink:href="#baseImage" transform="translate({x2 - w / 2 + w} {y1 - r - h/2}) scale(-1 1)" />
  <use xlink:href="#baseImage" transform="translate({x2 + r - w/2} {y1 - h / 2 + w}) rotate(90 {w / 2} {h / 2})  scale(-1 1)" />
  <use xlink:href="#baseImage" transform="translate({x2 - w / 2 - w} {y1 + r - h/2 }) rotate(180 {w / 2} {h / 2}) scale(-1 1)" />
  <use xlink:href="#baseImage" transform="translate({x2 - r - w/2} {y1 - h/2 - w}) rotate(270 {w / 2} {h / 2}) scale(-1 1)" />


</svg>
"""

print(x.strip())