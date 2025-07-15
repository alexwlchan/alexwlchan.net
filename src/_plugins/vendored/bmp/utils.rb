module BMP
  module Utils
    module_function

    # @return [Integer]
    def calc_image_data_size(arg_width, arg_height)
      ((BMP::BITS_PER_PIXEL * arg_width) / 32.0).ceil * 4 * arg_height
    end

    # @return [Integer]
    def calc_file_size(img_size, header_size = BMP::HEADER_SIZE)
      img_size + header_size
    end

    def pixel_array_template(arg_width, arg_height)
      Array.new(arg_height) { Array.new(arg_width) { nil } }
    end

    def write_pixel_array(img_px)
      str = ''

      img_px.reverse_each do |row|
        row.each do |color|
          str << pixel_binstring(color)
        end
      end

      str
    end

    def pixel_binstring(rgba_string)
      raise ArgumentError unless rgba_string =~ /\A\h{8}\z/

      [rgba_string].pack('H*')
    end

    def parse_image(img_in)
      img_width             = img_in.width
      img_height            = img_in.height
      img_data_size         = calc_image_data_size(img_width, img_height)
      img_file_size         = calc_file_size(img_data_size)
      img_pixels            = pixel_array_template(img_width, img_height)

      img_height.times do |row|
        img_width.times do |col|
          rgba = ChunkyPNG::Color.to_hex(img_in.get_pixel(row, col), true)[1..]
          rr, gg, bb, aa = rgba.scan(/../)
          img_pixels[col][row] = [bb, gg, rr, aa].join

          # puts row.to_s + ',' + col.to_s + ' => ' + rgba.inspect if @debug
        end
      end

      hash = {}
      hash[:file_size]     = img_file_size
      hash[:image_size]    = img_data_size
      hash[:image_width]   = img_width
      hash[:image_height]  = img_height
      hash[:pixel_array]   = write_pixel_array(img_pixels)

      hash
    end
  end
end
