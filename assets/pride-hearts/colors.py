# -*- encoding: utf-8 -*-

import math
import random
import re

import attr


HEX_COLOR_RE = re.compile(r"^#?(?P<hex_str>[a-fA-F0-9]{3}|[a-fA-F0-9]{6})$")


@attr.s
class RGBColor(object):
    red = attr.ib()
    green = attr.ib()
    blue = attr.ib()

    @classmethod
    def from_hex_string(cls, hex_str):
        m = HEX_COLOR_RE.match(hex_str)
        assert m is not None, hex_str

        if len(m.group("hex_str")) == 3:
            hex_value = u"".join(2 * s for s in m.group("hex_str"))
        else:
            hex_value = m.group("hex_str")

        assert len(hex_value) == 6, hex_value

        red = int(hex_value[0:2], 16)
        green = int(hex_value[2:4], 16)
        blue = int(hex_value[4:6], 16)

        return cls(red, green, blue)


def euclidean_distance(c1, c2):
    return math.sqrt(
        (c1.red - c2.red) ** 2 +
        (c1.green - c2.green) ** 2 +
        (c1.blue - c2.blue) ** 2
    )


def random_colors_near(c, threshold=100):
    while True:
        new_c = RGBColor(
            red=random.randint(0, 255),
            green=random.randint(0, 255),
            blue=random.randint(0, 255),
        )

        if euclidean_distance(c, new_c) < threshold:
            yield new_c
