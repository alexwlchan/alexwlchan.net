#!/usr/bin/env python
# -*- encoding: utf-8

TOP_PATTERNS = """
X.
..

X.
X.

XX
..

XX
.X

X.
.X

XX
X.

XX
XX

X.
XX

.X
X.

.X
XX
"""

BOTTOM_PATTERNS = [
    ("first",   ".."),
    ("second",  "X."),
    ("third",   "XX"),
    ("fourth",  ".X"),
]

print("""
<svg viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg" stroke="black" stroke-width="0.5" fill="white">
""".strip())

for i, pattern in enumerate(TOP_PATTERNS.split("\n\n"), start=1):
    pattern = pattern.strip()

    print(f"""
  <svg x="{(i - 1) * 30}" y="0">
    <circle cx="5" cy="5" r="3.5"%s/>
    <circle cx="15" cy="5" r="3.5"%s/>
    <circle cx="5" cy="15" r="3.5"%s/>
    <circle cx="15" cy="15" r="3.5"%s/>
    <circle cx="5" cy="25" r="3.5" stroke-dasharray="1,1"/>
    <circle cx="15" cy="25" r="3.5" stroke-dasharray="1,1"/>

    <text x="10" y="42" fill="black" font-size="10px" stroke-width="0" text-anchor="middle" font-family="sans-serif">{i}</text>
  </svg>""" % (
        ' fill="black"' if pattern[0] == "X" else "",
        ' fill="black"' if pattern[1] == "X" else "",
        ' fill="black"' if pattern[3] == "X" else "",
        ' fill="black"' if pattern[4] == "X" else ""
    ))


for i, (ordinal, pattern) in enumerate(BOTTOM_PATTERNS, start=1):
    print(f"""
  <svg x="{50 * i}" y="60">
    <circle cx="15" cy="5" r="3.5" stroke-dasharray="1,1"/>
    <circle cx="25" cy="5" r="3.5" stroke-dasharray="1,1"/>
    <circle cx="15" cy="15" r="3.5" stroke-dasharray="1,1"/>
    <circle cx="25" cy="15" r="3.5" stroke-dasharray="1,1"/>
    <circle cx="15" cy="25" r="3.5"%s/>
    <circle cx="25" cy="25" r="3.5"%s/>

    <text x="20" y="42" fill="black" font-size="10px" stroke-width="0" text-anchor="middle" font-family="sans-serif">{ordinal}</text>
    <text x="20" y="53" fill="black" font-size="10px" stroke-width="0" text-anchor="middle" font-family="sans-serif">decade</text>
  </svg>
    """ % (
        ' fill="black"' if pattern[0] == "X" else "",
        ' fill="black"' if pattern[1] == "X" else ""
    ))

print("""</svg>""")
