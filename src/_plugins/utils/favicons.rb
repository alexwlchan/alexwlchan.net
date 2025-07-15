require 'chunky_png'

require_relative '../vendored/ico'

# Given a ChunkyPNG image with grayscale pixels and a tint colour, create
# a colourised version of that image.
def colorise_image(image, tint_color)
  fill_color = Color::RGB.by_hex(tint_color)

  0.upto(image.width - 1) do |x|
    0.upto(image.height - 1) do |y|
      image.set_pixel(
        x, y,
        ChunkyPNG::Color.rgba(
          fill_color.red.to_i,
          fill_color.green.to_i,
          fill_color.blue.to_i,
          image.get_pixel(x, y)
        )
      )
    end
  end
end

# Create PNG, SVG and ICO variants of the favicon for this tint colour.
def create_favicon(tint_color)
  FileUtils.mkdir_p '_site/f'

  hex_string = tint_color.gsub('#', '')

  ico_path = "_site/f/#{hex_string}.ico"

  return if File.exist? ico_path

  # Create colorised versions of the SVG icon at 32x32 and 16x16 sizes
  svg16 = File.read('src/theme/_favicons/favicon-16x16.svg').gsub('#000000', tint_color)
  svg32 = File.read('src/theme/_favicons/favicon-32x32.svg').gsub('#000000', tint_color)

  File.write("_site/f/#{hex_string}-16x16.svg", svg16)
  File.write("_site/f/#{hex_string}-32x32.svg", svg32)

  # Create colorised versions of the PNG icon at 32x32 and 16x16 sizes
  png16 = ChunkyPNG::Image.from_file('src/theme/_favicons/template-16x16.png')
  png32 = ChunkyPNG::Image.from_file('src/theme/_favicons/template-32x32.png')

  colorise_image(png16, tint_color)
  png16.save("_site/f/#{hex_string}-16x16.png", :best_compression)

  colorise_image(png32, tint_color)
  png32.save("_site/f/#{hex_string}-32x32.png", :best_compression)

  # Create an ico favicon file from the two PNG sizes
  ico = ICO.new(["_site/f/#{hex_string}-16x16.png", "_site/f/#{hex_string}-32x32.png"])
  File.write(ico_path, ico)
end
