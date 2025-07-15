module ICO
  class IconDir < BitStruct
    LENGTH_IN_BYTES = 6

    default_options endian: :little

    unsigned  :reserved,    16,  'Reserved. Must always be 0.', default: 0

    unsigned  :type,        16,  'Specifies image type: 1 for icon (.ICO) ' \
                                 'image, 2 for cursor (.CUR) image. Other ' \
                                 'values are invalid.',                        default: 1

    unsigned  :image_count, 16,  'Specifies number of images in the file.',    default: 0

    rest      :data,             'IconDirEntry + IconImage sections as binary data strings'
  end
end
