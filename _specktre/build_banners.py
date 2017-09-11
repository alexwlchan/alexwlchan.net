#!/usr/bin/env python3
# -*- encoding: utf-8
"""
Build the Specktre banners for the blog.
"""

import os
import subprocess

from specktre.cli import check_color_input
from specktre.colors import RGBColor
from specktre.specktre import save_speckled_wallpaper, Settings
from specktre.tilings import generate_squares


ROOT = subprocess.check_output(
    ['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

# TODO: Determine the required colours in a less manual way
BANNER_COLOURS = [
    'd01c11', '008000',
]

for c in BANNER_COLOURS:
    print(f'Creating banner for {c}')
    color = check_color_input(c)

    start_color = RGBColor(*[int(c * 0.9) for c in color])
    end_color = RGBColor(*[min(int(c * 1.05), 255) for c in color])
    filename = os.path.join(
        ROOT, 'theme', 'specktre_%02x%02x%02x.png' % color
    )

    if os.path.exists(filename):
        continue

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    settings = Settings(
        generator=generate_squares,
        width=3000,
        height=250,
        start_color=start_color,
        end_color=end_color,
        name=filename
    )

    save_speckled_wallpaper(settings)

    subprocess.check_call(['optipng', filename])
