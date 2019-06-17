heart10 = """
 XX    XX
XXXX  XXXX
XXXXXXXXXX
XXXXXXXXXX
XXXXXXXXXX
XXXXXXXXXX
 XXXXXXXX
  XXXXXX
   XXXX
    XX
"""

from PIL import Image, ImageDraw

im = Image.new("L", size=(100, 100))
draw = ImageDraw.Draw(im)

for i, line in enumerate(heart10.splitlines()):
    if not line.strip():
        continue

    for j, char in enumerate(line.rstrip()):
        if char == "X":
            draw.polygon(
                [
                    (j * 10, (i - 1) * 10),
                    (j * 10, i * 10),
                    ((j + 1) * 10, i * 10),
                    ((j + 1) * 10, (i - 1) * 10),
                ],
                fill="red"
            )
        print((i, j), char)
    # print(i)
    # ImageDraw.draw(im).polygon
    # print(line)

im.save("heart10.png")



heart8 = """
  XX    XX
 XXXX  XXXX
XXXXXXXXXXXX
XXXXXXXXXXXX
XXXXXXXXXXXX
XXXXXXXXXXXX
XXXXXXXXXXXX
 XXXXXXXXXX
  XXXXXXXX
   XXXXXX
    XXXX
     XX
"""

from PIL import Image, ImageDraw

im = Image.new("L", size=(120, 120))
draw = ImageDraw.Draw(im)

for i, line in enumerate(heart8.splitlines()):
    if not line.strip():
        continue

    for j, char in enumerate(line.rstrip()):
        if char == "X":
            draw.polygon(
                [
                    (j * 10, (i - 1) * 10),
                    (j * 10, i * 10),
                    ((j + 1) * 10, i * 10),
                    ((j + 1) * 10, (i - 1) * 10),
                ],
                fill="red"
            )
        print((i, j), char)
    # print(i)
    # ImageDraw.draw(im).polygon
    # print(line)

im.save("heart8.png")
