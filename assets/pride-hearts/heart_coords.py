# -*- encoding: utf-8

HEART_10 = """\
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

HEART_12 = """\
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


def get_heart_rows(heart_ascii_art):
    for row_idx, line in enumerate(heart_ascii_art.splitlines()):
        col_indices = [
            col_idx
            for col_idx, char in enumerate(line.rstrip())
            if char == "X"
        ]
        row = [
            [
                (col_idx, row_idx),
                (col_idx, row_idx + 1),
                (col_idx + 1, row_idx + 1),
                (col_idx + 1, row_idx),
            ]
            for col_idx in col_indices
        ]
        yield row


def scale(polygon, factor):
    return [(x * factor, y * factor) for (x, y) in polygon]
