#!/usr/bin/env python
# -*- encoding: utf-8

from PIL import Image, ImageDraw

from heart_coords import get_heart_rows, scale, HEART_10, HEART_12


im = Image.new("L", size=(100, 100))
draw = ImageDraw.Draw(im)

for row in get_heart_rows(HEART_10):
    for rect in row:
        draw.polygon(scale(rect, factor=10), fill="red")

im.save("heart10.png")


im = Image.new("L", size=(120, 120))
draw = ImageDraw.Draw(im)

for row in get_heart_rows(HEART_12):
    for rect in row:
        draw.polygon(scale(rect, factor=10), fill="red")

im.save("heart12.png")
