#!/usr/bin/env python3

import math

radius = 250
height = 100
angle = math.pi / 6

print("""<svg viewBox="0 0 2500 550" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      path {
        stroke: currentColor;
        stroke-width: 1.5;
        stroke-linecap: round;
      }
    </style>""")

print(f"""

    <path id="shape1"
          d="M 0 {radius}
             a {radius} {radius}
             0 0 0
             {radius * math.sin(angle)} {-1 * radius * (1 - math.cos(angle))}
             a {radius} {radius}
             0 0 1
             {radius * math.sin(angle)} {-1 * radius * (1 - math.cos(angle))}
             a {radius} {radius}
             0 0 1
             {radius * math.sin(angle)} {radius * (1 - math.cos(angle))}
             a {radius} {radius}
             0 0 0
             {radius * math.sin(angle)} {radius * (1 - math.cos(angle))}
             l 0 {height}
             a {radius} {radius}
             0 0 1
             {-radius * math.sin(angle)} {-radius * (1 - math.cos(angle))}
             a {radius} {radius}
             0 0 0
             {-radius * math.sin(angle)} {-radius * (1 - math.cos(angle))}
             a {radius} {radius}
             0 0 0
             {-radius * math.sin(angle)} {radius * (1 - math.cos(angle))}
             a {radius} {radius}
             0 0 1
             {-radius * math.sin(angle)} {radius * (1 - math.cos(angle))}
             Z"/>
  </defs>

  <rect width="2500" height="550" fill="yellow"/>
""")

for y in range(7):
    print(f'<svg y="{height * (y-3)}">')
    for x in range(20):

        import random

        grey = random.randint(int(255 * .25), int(255 * .75))

        print(f"""
        <use x="{x * 4 * radius * math.sin(angle)}" href="#shape1" fill="rgb({int(grey)}, {int(grey)}, {int(grey)})"/>
        """)

    print("</svg>")

print('<rect width="2500" height="550" fill="none" stroke="yellow"/>')

print("</svg>")