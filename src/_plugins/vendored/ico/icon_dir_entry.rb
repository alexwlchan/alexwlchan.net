module ICO
  class IconDirEntry < BitStruct
    LENGTH_IN_BYTES = 16

    default_options endian: :little

    unsigned  :width,         8,  'Specifies image width in pixels. Can be ' \
                                  'any number between 0 and 255. Value 0 ' \
                                  'means image width is 256 pixels.'

    unsigned  :height,        8,  'Specifies image height in pixels. Can be ' \
                                  'any number between 0 and 255. Value 0 ' \
                                  'means image width is 256 pixels.'

    unsigned  :color_count,   8,  'Specifies number of colors in the color ' \
                                  'palette. Should be 0 if the image does ' \
                                  'not use a color palette.',                   default: 0

    unsigned  :reserved,      8,  'Reserved. Should be 0. [NOTES 2]',           default: 0

    unsigned  :planes,        16, 'In ICO format: Specifies color planes. ' \
                                  "Should be 0 or 1.\n" \
                                  'In CUR format: Specifies the horizontal ' \
                                  'coordinates of the hotspot in number of ' \
                                  'pixels from the left.', default: 1

    unsigned  :bit_count,     16, 'In ICO format: Specifies bits per pixel. ' \
                                  "[NOTES 4]\n" \
                                  'In CUR format: Specifies the vertical ' \
                                  'coordinates of the hotspot in number of ' \
                                  'pixels from the top.', default: 32

    unsigned  :bytes_in_res,  32, 'Specifies the size of the image\'s data ' \
                                  'in bytes'

    unsigned  :image_offset,  32, 'Specifies the offset of BMP or PNG data ' \
                                  'from the beginning of the ICO/CUR file'
  end
end
