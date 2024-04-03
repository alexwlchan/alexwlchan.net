#!/usr/bin/env python3
"""
Code for drawing circular arcs in SVG.

From https://alexwlchan.net/2022/08/circle-party/
"""

import math


def get_circular_arc_path_command(*, centre_x, centre_y, radius, start_angle, sweep_angle, angle_unit):
    """
    Returns a path command to draw a circular arc in an SVG <path> element.

    See https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#line_commands
    """
    if angle_unit == "radians":
        pass
    elif angle_unit == "degrees":
        start_angle = start_angle / 180 * math.pi
        sweep_angle = sweep_angle / 180 * math.pi
    else:
        raise ValueError(f"Unrecognised angle unit: {angle_unit}")

    # We need to work out the x-y coordinates of where the arc will end,
    # which we can do with trig identities.
    #
    #                R cos Θ
    #               +-------+
    #               |      /
    #               |     /
    #               |    /
    #       R sin Θ |   / R = radius
    #               |  /
    #               |Θ/
    #               |/
    #               + (centre_x, centre_y)
    #

    # For the start of the arc, Θ = start_angle
    start_x = centre_x + radius * math.sin(start_angle)
    start_y = centre_y - radius * math.cos(start_angle)

    # For the end of the arc, Θ = start_angle + sweep_angle
    end_x = centre_x + radius * math.sin(start_angle + sweep_angle)
    end_y = centre_y - radius * math.cos(start_angle + sweep_angle)

    # An arc path in SVG defines an ellipse/curve between two points.
    # The `x_axis_rotation` parameter defines how an ellipse is rotated,
    # if at all, but circles don't change under rotation, so it's irrelevant.
    x_axis_rotation = 0

    # For a given radius, there are two circles that intersect the
    # start/end points.
    #
    # The `sweep-flag` parameter determines whether we move in
    # a positive angle (=clockwise) or negative (=counter-clockwise).
    # I'only doing clockwise sweeps, so this is constant.
    sweep_flag = 1

    # There are now two arcs available: one that's more than 180 degrees,
    # one that's less than 180 degrees (one from each of the two circles).
    # The `large-arc-flag` decides which to pick.
    if sweep_angle > math.pi:
        large_arc_flag = 1
    else:
        large_arc_flag = 0

    return (
        f"M {start_x} {start_y} "
        f"A {radius} {radius} "
        f"{x_axis_rotation} {large_arc_flag} {sweep_flag} {end_x} {end_y}"
    )


if __name__ == "__main__":
    print('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">')

    print(
        f'<circle cx="50" cy="50" r="40" stroke="grey" stroke-width="1" fill="none"/>'
    )

    path = get_circular_arc_path_command(
        centre_x=50,
        centre_y=50,
        radius=40,
        start_angle=math.pi,
        sweep_angle=math.pi,
        angle_unit="radians"
    )

    print(f'<path d="{path}" stroke="black" stroke-width="5" fill="none"/>')

    print("</svg>")
