require 'chunky_png'
require 'shell/executer'

require_relative '../pillow/create_ico_image'

# Given the front matter from a page, get the CSS colors (if any).
def get_css_colors(page)
  colors = page.fetch('colors', {})

  primary_color_light = colors['css_light']
  primary_color_dark = colors['css_dark']

  return if primary_color_light.nil? && primary_color_dark.nil?

  { 'light' => primary_color_light, 'dark' => primary_color_dark }
end

# Get the light color that will be used as the default colour if
# no override tint color is specified.
#
# This looks for the `--default-primary-color-light` variable.
def read_default_light_color
  sass_source = File.read 'src/_scss/variables.scss'

  match = sass_source.match('\-\-default-primary\-color\-light: (?<color>#[0-9a-f]{6});')

  match.named_captures['color']
end

# Given a given hex colour as a string (e.g. '#123456') generate
# an infinite sequence of colours which vary only in brightness.
def get_colors_like(hex_color)
  # Seed the random to get consistent outputs
  seeded_random = Random.new(hex_color[1..].to_i(16))

  hsl_color = Color::RGB.by_hex(hex_color).to_hsl

  luminosity = hsl_color.luminosity

  min_luminosity = luminosity * 7 / 8
  max_luminosity = luminosity * 8 / 7

  luminosity_diff = max_luminosity - min_luminosity

  Enumerator.new do |enum|
    loop do
      hsl_color.luminosity = min_luminosity + (seeded_random.rand * luminosity_diff)
      enum.yield hsl_color.to_rgb
    end
  end
end

def squares_for(width, height, square_size)
  Enumerator.new do |enum|
    x0 = 0
    y0 = 0

    while x0 < width
      while y0 < height
        enum.yield [x0, y0, x0 + square_size - 1, y0 + square_size - 1]
        y0 += square_size
      end

      x0 += square_size
      y0 = 0
    end
  end
end

# Create the "speckled" header image for a given hex color.
def create_header_image(tint_color)
  FileUtils.mkdir_p '_site/headers'

  out_path = "_site/headers/specktre_#{tint_color.sub('#', '')}.png"

  return if File.file?(out_path)

  colors = get_colors_like(tint_color)
  squares = squares_for(2500, 250, 50)

  image = ChunkyPNG::Image.new(2500, 250)

  squares.zip(colors).each do |rect, fill_color|
    x0, y0, x1, y1 = rect

    image.rect(
      x0, y0, x1, y1,
      ChunkyPNG::Color.rgba(0, 0, 0, 0),
      ChunkyPNG::Color.rgb(
        fill_color.red.to_i,
        fill_color.green.to_i,
        fill_color.blue.to_i
      )
    )
  end

  image.save(out_path, :best_compression)
end

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

def create_favicon(tint_color)
  FileUtils.mkdir_p '_site/favicons'

  hex_string = tint_color.gsub('#', '')

  ico_path = "_site/favicons/#{hex_string}.ico"
  png_path = "_site/favicons/#{hex_string}.png"

  return if (File.exist? ico_path) && (File.exist? png_path)

  image16 = ChunkyPNG::Image.from_file('src/theme/_favicons/template-16x16.png')
  image32 = ChunkyPNG::Image.from_file('src/theme/_favicons/template-32x32.png')

  Dir.mktmpdir do |tmp_dir|
    fill_color = Color::RGB.by_hex(tint_color)

    colorise_image(image16, fill_color)
    image16.save("#{tmp_dir}/favicon-16x16.png", :best_compression)

    colorise_image(image32, fill_color)
    image32.save("#{tmp_dir}/favicon-32x32.png", :best_compression)

    create_ico_image(
      "#{tmp_dir}/favicon-16x16.png",
      "#{tmp_dir}/favicon-32x32.png",
      "#{tmp_dir}/favicon.ico"
    )

    FileUtils.mv "#{tmp_dir}/favicon-32x32.png", png_path
    FileUtils.mv "#{tmp_dir}/favicon.ico", ico_path
  end
end
