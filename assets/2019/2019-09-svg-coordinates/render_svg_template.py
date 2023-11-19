#!/usr/bin/env python
# -*- encoding: utf-8

import math
import os
import re
import sys

from lxml import etree
from jinja2 import Environment, FileSystemLoader


def triangular_to_cartesian(coordinate1, coordinate2):
    """Convert triangular coordinates to Cartesian."""
    # Quick trig reminder: suppose we have a triangle ABC, like so:
    #
    #             + B
    #            /|
    #           / |
    #          /  |
    #         /   |
    #        /    |
    #     A +-----+ C
    #
    # Here angle A is 60°, angle B is 30° and angle C is 90° (a right angle).
    #
    # Suppose the length of AB is 1.  Then starting at angle A, we have:
    #
    #       cos(60) = adjacent / hypotenuse
    #               = AC / AB
    #               = AC
    #
    #       sin(60) = opposite / hypotenuse
    #               = BC / AB
    #               = BC
    #
    # So (coordinate1, coordinate2) becomes:
    #
    #       coordinate1 => (x, 0)
    #       coordinate2 => (x cos 60, y sin 60)
    #
    x = coordinate1 + coordinate2 * math.cos(math.radians(60))
    y = coordinate2 * math.sin(math.radians(60))

    return (x, y)


if "hex" in sys.argv[1]:
    X_OFFSET = 3
    Y_OFFSET = 3
else:
    X_OFFSET = 0
    Y_OFFSET = 0


def triangular_x(coords):
    return triangular_to_cartesian(*coords)[0] + X_OFFSET

def triangular_y(coords):
    return triangular_to_cartesian(*coords)[1] + Y_OFFSET

def polygon_xy(coords):
    x, y = triangular_to_cartesian(*coords)
    return ",".join(["%.6f" % (x + X_OFFSET), "%.6f" % (y + Y_OFFSET)])


def get_rendered_xml(template_path):
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    env.filters["triangular_x"] = triangular_x
    env.filters["triangular_y"] = triangular_y
    env.filters["polygon_xy"] = polygon_xy

    template = env.get_template(os.path.basename(template_path))

    return template.render()


def minify_xml(xml_str):
    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    elem = etree.XML(xml_str, parser=parser)
    return re.sub(b'\s+', b' ', etree.tostring(elem))


if __name__ == "__main__":
    try:
        template_path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <TEMPLATE>")

    xml_str = get_rendered_xml(template_path)
    print(minify_xml(xml_str).decode('utf8'))
