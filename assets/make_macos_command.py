#!/usr/bin/env python3

import math

# (50, 25, 4)

L = 5
circle_r = 1
number_of_sides = 5

# assert L > 2 * r

# import q; q.q(inner_L)



paths = []

# for _ in range(number_of_sides):
#     print(_)


  # <path d="M 20 120 L 120 120 A 50 50, 0, 1, 0 70 70" fill="none"/>

theta = 360 - 360 / number_of_sides

r = circle_r * math.tan((180 - theta / 2) * math.pi / 180)

import q; q.q(r)

inner_L = (L - 2 * r) / 2

side = int(math.ceil(2 * math.sqrt(2) * (inner_L + 5 * circle_r)))

center = side / 2

print(f"""<svg viewBox="0 0 {side} {side}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      path {{
        stroke-width: 0.5;
        stroke-linecap: round;
      }}
    </style>
  </defs>

  <rect width="{side}" height="{side}" fill="yellow"/>

""")

# print(f'<circle cx="{center}" cy="{center}" r="3" fill="black"/>')


for i in range(number_of_sides):
    print(f'''
    <path d="M
          {center - L / 2} {center - inner_L / math.tan(math.pi / number_of_sides)}
        L {center + L / 2} {center - inner_L / math.tan(math.pi / number_of_sides)}"
        fill="none"
        transform="rotate({360 / number_of_sides * i}, {center}, {center})"
        style="stroke: black;"
        />
    ''')
    print(f'''
    <path d="M {center + L / 2} {center - inner_L / math.tan(math.pi / number_of_sides)}
        a {circle_r} {circle_r}, 0, 1, 0
        {circle_r * math.sin(theta * math.pi / 180)} {circle_r * math.cos(theta * math.pi / 180) - circle_r}
        " fill="none"
        transform="rotate({360 / number_of_sides * i}, {center}, {center})"
        style="stroke: black;"
        />
    ''')

print("</svg>")