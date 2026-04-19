"""
Create icons for the /files/ view in my Git repositories.
"""

# Overall dimensions of the SVG
icon_width = 20
icon_height = 20

# Dimensions of the folder
folder_width = 18
folder_height = 12

# Dimensions of the tab
tab_width = 7
tab_height = 2.5

# Small/large corner radius
radius_s = 1.25
radius_l = 2

# Offset of the "open folder" overlay compared to the background
open_offset_x = radius_s + radius_l
open_offset_y = 3.25

# Starting x/y values for the folder icon
folder_x = (icon_width - folder_width) / 2
folder_y = (icon_height - folder_height) / 2

# Dimensions of the file icon
file_width = 14
file_height = 18

# Amount to cut off the corner of the file icon
file_corner_size = 6.5

# Starting x/y values for the file icon
file_x = (icon_width - file_width) / 2
file_y = (icon_height - file_height) / 2

# Stroke width
stroke_width = 2


def closed_folder_icon(tint_colour: str) -> str:
    """
    Draw an SVG for the closed folder icon. This starts on the top-left of
    the tab and goes clockwise around the shape.

        X------\
       /        \
      |          --------+
      |                  |
      |                  |
      +------------------+
    """
    return f'''
        <svg viewBox="0 0 {icon_width} {icon_height}" width="{icon_width}" xmlns="http://www.w3.org/2000/svg">
          <path
            stroke="{tint_colour}"
            stroke-width="{stroke_width}"
            fill="{tint_colour}"
            d="M {folder_x + radius_s} {folder_y}
               h {tab_width - radius_s * 2}
               a {radius_s} {radius_s} 0 0 1 {radius_s} {radius_s}
               v {tab_height - radius_s * 2}
               a {radius_s} {radius_s} 0 0 0 {radius_s} {radius_s}
               h {folder_width - tab_width - radius_s * 2}
               a {radius_s} {radius_s} 0 0 1 {radius_s} {radius_s}
               v {folder_height - radius_s * 2}
               a {radius_s} {radius_s} 0 0 1 {-radius_s} {radius_s}
               h {-folder_width + radius_s * 2}
               a {radius_s} {radius_s} 0 0 1 {-radius_s} {-radius_s}
               v {-folder_height - tab_height + 2 * radius_s}
               a {radius_s} {radius_s} 0 0 1 {radius_s} {-radius_s}"/>
        </svg>
    '''


def open_folder_icon(tint_colour: str, background_colour: str) -> str:
    """
    Draw an SVG for the open folder icon.
    """
    return f'''
        <svg viewBox="0 0 {icon_width} {icon_height}" width="{icon_width}" xmlns="http://www.w3.org/2000/svg">
          <path
            stroke="{tint_colour}"
            stroke-width="{stroke_width}"
            fill="{background_colour}"
            d="M {folder_x + radius_s} {folder_y}
                     h {tab_width - radius_s * 2}
                     a {radius_s} {radius_s} 0 0 1 {radius_s} {radius_s}
                     v {tab_height - radius_s * 2}
                     a {radius_s} {radius_s} 0 0 0 {radius_s} {radius_s}
                     h {folder_width - tab_width - radius_s * 2 - open_offset_x}
                     a {radius_s} {radius_s} 0 0 1 {radius_s} {radius_s}
                     v {folder_height - radius_s * 2}
                     a {radius_s} {radius_s} 0 0 1 {-radius_s} {radius_s}
                     h {-folder_width + radius_s * 2 + open_offset_x}
                     a {radius_s} {radius_s} 0 0 1 {-radius_s} {-radius_s}
                     v {-folder_height - tab_height + 2 * radius_s}
                     a {radius_s} {radius_s} 0 0 1 {radius_s} {-radius_s}"
                     />
          <path
            stroke="{tint_colour}"
            stroke-width="{stroke_width}"
            fill="{tint_colour}"
            d="M {folder_x + radius_s} {folder_y + tab_height + folder_height}
               a {radius_l} {radius_l} 0 0 0 {radius_l} {-radius_l}
               v {-(folder_height - radius_l - open_offset_y - radius_s)}
               a {radius_s} {radius_s} 0 0 1 {radius_s} {-radius_s}
               h {folder_width - radius_s * 3 - radius_l}
               a {radius_s} {radius_s} 0 0 1 {radius_s} {radius_s}
               v {(folder_height - radius_l - open_offset_y - radius_s)}
               a {radius_l} {radius_l} 0 0 1 {-radius_l} {radius_l}
               Z"/>
        </svg>
    '''


def file_icon(tint_colour: str, background_colour: str) -> str:
    """
    Draw an SVG for the file icon.
    """
    return f'''
        <svg viewBox="0 0 {icon_width} {icon_height}" width="{icon_width}" xmlns="http://www.w3.org/2000/svg">
          <path
            stroke="{tint_colour}"
            stroke-width="{stroke_width}"
            fill="{background_colour}"
            stroke-linecap="round"
            d="M {file_x} {file_y + radius_l}
               a {radius_l} {radius_l} 0 0 1 {radius_l} {-radius_l}
               h {file_width - radius_l - file_corner_size}
               v {(file_corner_size) - radius_s}
               a {radius_s} {radius_s} 0 0 0 {radius_s} {radius_s}
               h {(file_corner_size) - radius_s}
               v {file_height - radius_l - file_corner_size}
               a {radius_l} {radius_l} 0 0 1 {-radius_l} {radius_l}
               h {-file_width + 2 * radius_l}
               a {radius_l} {radius_l} 0 0 1 {-radius_l} {-radius_l}
               v {-file_height + 2 * radius_l}
               Z"/>
          <path
            stroke="{tint_colour}"
            stroke-width="{stroke_width * 0.85}"
            stroke-linecap="round"
            fill="none"
            d="M {file_x} {file_y + radius_l}
               a {radius_l} {radius_l} 0 0 1 {radius_l} {-radius_l}
               h {file_width - radius_l - file_corner_size + 0.45}
               l {file_corner_size - 0.45} {file_corner_size - 0.45}
               "/>
        </svg>
    '''


def svg_data_uri(svg: str) -> str:
    """
    Encode an SVG as a data URI to use in a CSS url().
    """
    minified_xml = " ".join([ln.strip() for ln in svg.strip().splitlines()])
    text = minified_xml.replace("#", "%23").replace('"', "'")
    return f"data:image/svg+xml;utf8,{text}"
