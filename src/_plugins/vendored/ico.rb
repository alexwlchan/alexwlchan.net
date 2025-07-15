require_relative 'bmp'

require 'bit-struct'
require 'chunky_png'

require_relative 'ico/version'
require_relative 'ico/utils'
require_relative 'ico/icon_dir'
require_relative 'ico/icon_dir_entry'
require_relative 'ico/icon_image'

#
# @see https://en.wikipedia.org/wiki/ICO_(file_format)
#
module ICO
  # make all methods class-methods

  module_function

  # create ICO object
  #
  # @param filename_array [String, Array<String>] filename, or array of filenames
  # @return               [BitStruct]
  #
  def new(filename_array)
    raise ArgumentError unless filename_array.is_a?(Array) || filename_array.is_a?(String)

    # ensure non-nested array
    fn_array = [filename_array].flatten

    # ensure .png extensions
    raise "more than PNG format files in #{filename_array.inspect}" if ICO::Utils.contains_other_than_ext?(fn_array,
                                                                                                           :png)

    fn_array_length       = fn_array.length
    icon_dir              = ICO::IconDir.new
    icon_dir.image_count  = fn_array.length
    offset                = ICO::IconDir::LENGTH_IN_BYTES + (fn_array_length * ICO::IconDirEntry::LENGTH_IN_BYTES)
    entries               = Array.new(fn_array_length) { ICO::IconDirEntry.new }
    images                = Array.new(fn_array_length) { ICO::IconImage.new }
    # reorder by image size
    images_array          = ICO::Utils.sizes_hash(fn_array, true, true).values

    images_array.each_with_index do |fn, i|
      img                 = ChunkyPNG::Image.from_file(fn)
      # img_hash            = BMP::Utils.parse_image(img, ICO::IconImage::HEADER_SIZE_IN_BYTES)
      img_hash            = BMP::Utils.parse_image(img)
      mask_size           = img_hash[:image_width] * 4
      mask                = "\x00\x00\x00\x00" * img_hash[:image_width]
      image_size          = (img_hash[:image_width] * img_hash[:image_height] * 4) + mask_size
      file_size           = image_size + ICO::IconImage::HEADER_SIZE_IN_BYTES

      entry               = entries[i]
      entry.width         = img_hash[:image_width]
      entry.height        = img_hash[:image_height]
      entry.bytes_in_res  = file_size
      entry.image_offset  = offset

      image               = images[i]
      image.width         = img_hash[:image_width]
      image.height        = (img_hash[:image_height] * 2)
      image.size_image    = image_size
      image.data          = img_hash[:pixel_array] + mask

      offset += file_size
    end

    # IconDirEntry + IconImage section as binary data string
    icon_dir.data = entries.join + images.join

    icon_dir
  end
end
