module ICO
  class IconImage < BitStruct
    HEADER_SIZE_IN_BYTES = 40

    default_options endian: :little

    # BITMAPINFOHEADER
    unsigned  :header_size,           32, nil, default: HEADER_SIZE_IN_BYTES
    unsigned  :width,                 32
    unsigned  :height,                32
    unsigned  :planes,                16, nil,  default: 1
    unsigned  :bit_count,             16, nil,  default: 32
    unsigned  :compression,           32, nil,  default: 0
    unsigned  :size_image,            32
    unsigned  :x_pixels_per_meter,    32, nil,  default: 0
    unsigned  :y_pixels_per_meter,    32, nil,  default: 0
    unsigned  :colors_used,           32, nil,  default: 0
    unsigned  :colors_important,      32, nil,  default: 0

    # IMAGEDATA
    rest      :data,                  '32bit RGBQUAD written: BGRA'
  end
end
