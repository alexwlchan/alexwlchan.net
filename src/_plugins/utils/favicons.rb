require 'chunky_png'

require_relative '../vendored/ico'

# Given a ChunkyPNG image with grayscale pixels and a tint colour, create
# a colourised version of that image.
def colorise_image(image, tint_color)
  0.upto(image.width - 1) do |x|
    0.upto(image.height - 1) do |y|
      image.set_pixel(
        x, y,
        ChunkyPNG::Color.rgba(
          tint_color.red.to_i,
          tint_color.green.to_i,
          tint_color.blue.to_i,
          image.get_pixel(x, y)
        )
      )
    end
  end
end

# Create PNG and ICO variants of the favicon for this tint colour.
def create_favicon(tint_color)
  FileUtils.mkdir_p '_site/f'

  hex_string = tint_color.gsub('#', '')

  ico_path = "_site/f/#{hex_string}.ico"

  return if File.exist? ico_path

  image16 = ChunkyPNG::Image.from_file('src/theme/_favicons/template-16x16.png')
  image32 = ChunkyPNG::Image.from_file('src/theme/_favicons/template-32x32.png')

  fill_color = Color::RGB.by_hex(tint_color)

  colorise_image(image16, fill_color)
  image16.save("_site/f/#{hex_string}-16x16.png", :best_compression)

  colorise_image(image32, fill_color)
  image32.save("_site/f/#{hex_string}-32x32.png", :best_compression)

  ico = ICO.new(["_site/f/#{hex_string}-16x16.png", "_site/f/#{hex_string}-32x32.png"])
  File.write(ico_path, ico)
end
