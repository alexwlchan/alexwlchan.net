require 'bit-struct'
require 'chunky_png'

require_relative 'bmp/version'
require_relative 'bmp/utils'
require_relative 'bmp/obj'

module BMP
  HEADER_SIZE       = 54
  BITS_PER_PIXEL    = 32

  # make all methods class-methods
  module_function

  # PNG to BMP
  #
  # @param  input_filename  [String] "/path/to/example.png"
  # @param  output_filename [String] "/path/to/example_generated.bmp"
  # @return                 [void]
  #
  def png_to_bmp(input_filename, output_filename)
    bmp = BMP.new(input_filename)

    File.write(output_filename, bmp)
  end

  #
  # @param  input_filename  [PNG] including path
  # @return                 [BitStruct]
  #
  def new(input_filename)
    img               = ChunkyPNG::Image.from_file(input_filename)
    img_hash          = BMP::Utils.parse_image(img)

    bmp               = BMP::Obj.new
    bmp.file_size     = img_hash[:file_size]
    bmp.image_size    = img_hash[:image_size]
    bmp.image_width   = img_hash[:image_width]
    bmp.image_height  = img_hash[:image_height]
    bmp.pixel_array   = img_hash[:pixel_array]

    bmp
  end
end
