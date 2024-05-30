class ImageFormat
  AVIF = { extension: '.avif', mime_type: 'image/avif' }

  WEBP = { extension: '.webp', mime_type: 'image/webp' }

  JPEG = { extension: '.jpg',  mime_type: 'image/jpeg' }
  PNG  = { extension: '.png',  mime_type: 'image/png' }
end

def get_format(image_path, image)
  case image['format']
  when 'PNG'
    ImageFormat::PNG
  when 'JPEG'
    ImageFormat::JPEG
  else
    raise "Unrecognised image extension in #{image_path} (#{image['format']})"
  end
end

def create_source_elements(sources, source_im_format, options)
  format_order = [ImageFormat::AVIF, ImageFormat::WEBP, source_im_format]
                 .reject { |im_format| sources[im_format].nil? }
                 .filter { |im_format| options[:desired_formats].include? im_format }

  source_elements = format_order.map do |im_format|
    if options[:dark_mode]
      <<~HTML
        <source
          srcset="#{sources[im_format].join(', ')}"
          sizes="#{options[:sizes]}"
          type="#{im_format[:mime_type]}"
          media="(prefers-color-scheme: dark)"
        >
      HTML
    else
      <<~HTML
        <source
          srcset="#{sources[im_format].join(', ')}"
          sizes="#{options[:sizes]}"
          type="#{im_format[:mime_type]}"
        >
      HTML
    end
  end

  source_elements.join
end
