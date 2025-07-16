def create_base64_avatar(path, size)
  require 'base64'
  require 'vips'

  cache = Jekyll::Cache.new('Base64Avatars')
  mtime = File.mtime(path).to_i

  cache.getset("#{path}--#{mtime}--#{size}") do
    im = Vips::Image.new_from_file path

    if im.width != im.height
      raise "Avatar is not square: #{path}"
    end

    # Resize the image to match the target size
    scale = size.to_f / im.width
    resized = im.resize(scale)

    # Now write the image to a buffer, and convert it to base64.
    #
    # We preserve the original format, which is likely to be the most
    # efficient encoding for this image.
    case im.get 'vips-loader'
    when 'jpegload'
      jpeg_bytes = resized.write_to_buffer('.jpg')
      base64_string = Base64.strict_encode64(jpeg_bytes)
      "data:image/jpeg;base64,#{base64_string}"
    when 'pngload'
      png_bytes = resized.write_to_buffer('.png')
      base64_string = Base64.strict_encode64(png_bytes)
      "data:image/png;base64,#{base64_string}"
    else
      raise "Unrecognised vips loader for #{path}: #{im.get 'vips-loader'}"
    end
  end
end
