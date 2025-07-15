require 'bit-struct'

module BMP
  class Obj < BitStruct
    default_options endian: :little

    #
    # BMP Header
    #
    char      :signature,             16, 'ID field ["BM" (42h, 4Dh)]', default: 'BM'
    unsigned  :file_size,             32, 'Size of the BMP file [(122+N) bytes]'
    unsigned  :reserved_1,            16, 'Application specific [unused]',                        default: 0
    unsigned  :reserved_2,            16, 'Application specific [unused]',                        default: 0

    # Wikipedia:
    # unsigned  :file_offset,           32, 'Offset where the pixel array (bitmap data) can be ' +
    #                                      'found [122 bytes (14+108)]',                           :default => 122
    # IRL:
    unsigned  :file_offset, 32, 'Offset where the pixel array (bitmap data) can be ' \
                                'found [54 bytes (14+40)]', default: 54

    #
    # DIB Header
    #
    # Wikipedia:
    # unsigned  :dib_header_size,       32,  'Number of bytes in the DIB header (from this point) ' +
    #                                       '[108 bytes]',                                         :default => 108
    # IRL:
    unsigned  :dib_header_size,       32, 'Number of bytes in the DIB header (from this point) ' \
                                          '[40 bytes]', default: 40

    unsigned  :image_width,           32, 'Width of the bitmap in pixels (left to right order) ' \
                                          '[pixels]'
    unsigned  :image_height,          32, 'Height of the bitmap in pixels (bottom to top order) ' \
                                          '[pixels]'
    unsigned  :planes,                16, 'Number of color planes being used [1 plane]',          default: 1
    unsigned  :bits_per_pixel,        16, 'Number of bits per pixel [32 bits]',                   default: 32

    # Wikipedia:
    # unsigned  :compression,           32,  'BI_BITFIELDS, no pixel array compression used [3]',   :default => 3
    # IRL:
    unsigned  :compression,           32, 'BI_BITFIELDS, no pixel array compression used [3]',    default: 0

    unsigned  :image_size,            32, 'Size of the raw bitmap data (including padding)'
    unsigned  :x_pixels_per_meter,    32, 'Print resolution of the image, 72 DPI × 39.3701 ' \
                                          'inches per meter yields 2834.6472 [2835 pixel/meter ' \
                                          'horizontal]', default: 2835
    unsigned  :y_pixels_per_meter,    32, 'Print resolution of the image, 72 DPI × 39.3701 ' \
                                          'inches per meter yields 2834.6472 [2835 pixel/meter ' \
                                          'horizontal]',                                          default: 2835
    unsigned  :number_of_colors,      32, 'Number of colors in the palette [0 colors]',           default: 0
    unsigned  :important_colors,      32, '0 means all colors are important [0]',                 default: 0

    # Wikipedia:
    # hex_octets  :red_bitmask,         32,  'Red channel bit mask (valid because BI_BITFIELDS ' +
    #                                       'is specified) [00FF0000 in big-endian]',              :default => "00:00:FF:00", :endian => :big
    # hex_octets  :geen_bitmask,        32,  'Green channel bit mask (valid because BI_BITFIELDS ' +
    #                                       'is specified) [0000FF00 in big-endian]',              :default => "00:FF:00:00", :endian => :big
    # hex_octets  :blue_bitmask,        32,  'Blue channel bit mask (valid because BI_BITFIELDS ' +
    #                                       'is specified) [000000FF in big-endian]',              :default => "FF:00:00:00", :endian => :big
    # hex_octets  :alpha_bitmask,       32,  'Alpha channel bit mask [FF000000 in big-endian]',     :default => "00:00:00:FF", :endian => :big
    # char        :color_space,         32,  'LCS_WINDOWS_COLOR_SPACE [little-endian "Win "]',      :default => 'Win '
    # unsigned    :cs_endpoints,        288, 'CIEXYZTRIPLE Color Space endpoints [unused for LCS ' +
    #                                       '"Win " or "sRGB"]',                                   :default => 0
    # unsigned    :red_gamma,           32,  'Red Gamma - Unused for LCS "Win " or "sRGB"',         :default => 0
    # unsigned    :green_gamma,         32,  'Green Gamma - Unused for LCS "Win " or "sRGB"',       :default => 0
    # unsigned    :blue_gamma,          32,  'Blue Gamma - Unused for LCS "Win " or "sRGB"',        :default => 0
    # IRL:
    # nil

    rest      :pixel_array,               'Image Data'
    note                                  '     rest is application defined image data'
  end
end
