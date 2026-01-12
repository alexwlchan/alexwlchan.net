require 'fileutils'

require 'color'
require 'chunky_png'
require 'shell/executer'

require_relative '../vendored/ico'

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
  sass_source = File.read 'src/_scss/variables.css'

  match = sass_source.match('\-\-default-primary\-color\-light: (?<color>#[0-9a-f]{6});')

  match.named_captures['color']
end

# Get the dark color that will be used as the default colour if
# no override tint color is specified.
def read_default_dark_color
  sass_source = File.read 'src/_scss/variables.css'

  match = sass_source.match('\-\-default-primary\-color\-dark:\s+(?<color>#[0-9a-f]{6});')

  match.named_captures['color']
end

# Given a given hex colour as a string (e.g. '#123456') generate
# an infinite sequence of colours which vary only in lightness.
def get_colours_like(hex_colour)
  # 1. Seed the random to get consistent outputs.  This ensures the
  #    images created in local builds are the same as ones on the
  #    server, and I can delete the folder and regenerate without
  #    changing the appearance of already-published pages.
  seeded_random = Random.new(hex_colour[1..].to_i(16))

  # 2. Convert the hex colour to RGB, then to CIELAB.
  rgb = Color::RGB.by_hex(hex_colour)
  lab = rgb.to_lab

  # 3. Work out the min/max lightness that gets us a fixed delta
  #    away from the original color.
  #
  #    Note(2025-12-24): although it's currently the same +/- in
  #    both directions, but maybe it should be different and depend
  #    on whether you're in light/dark mode?
  min_lightness = get_lightness_for_delta(lab, 'darker', 6)
  max_lightness = get_lightness_for_delta(lab, 'lighter', 6)

  lightness_diff = max_lightness - min_lightness

  if lightness_diff.zero?
    raise "No lightness diff for hex colour: #{hex_colour}"
  end

  # 4. Generate random CIELAB colours in this (min, max) lightness range,
  #    then convert them to RGB.
  Enumerator.new do |enum|
    loop do
      new_lab = Color::CIELAB.from_values(
        min_lightness + (seeded_random.rand * lightness_diff),
        lab.a,
        lab.b
      )

      # Discard colours which don't map cleanly from CIELAB to sRGB
      if new_lab.delta_e2000(new_lab.to_rgb.to_lab) > 1
        next
      end

      enum.yield new_lab.to_rgb
    end
  end
end

# Find the lightness of a CIELAB colour that gets a specific perceptual
# difference (target_delta) from the original colour, while maintaining
# the original chromaticity.
def get_lightness_for_delta(original_lab, direction, target_delta)
  # 1. Define the search range for L*
  if direction == 'lighter'
    low_l = original_lab.l
    high_l = 100
  else
    low_l = 0
    high_l = original_lab.l
  end

  # 2. Run a binary search on L*
  best_lab = original_lab
  best_delta = 0

  15.times do
    mid_l = (low_l + high_l) / 2.0

    candidate_lab = Color::CIELAB.from_values(mid_l, original_lab.a, original_lab.b)
    candidate_delta = original_lab.delta_e2000(candidate_lab)

    # Are we closer than the current best colour? If so, replace it.
    if (candidate_delta - target_delta).abs < (best_delta - target_delta).abs
      best_lab = candidate_lab
      best_delta = candidate_delta
    end

    if candidate_delta < target_delta
      # We need more distance, move away from the original L*
      direction == 'lighter' ? (low_l = mid_l) : (high_l = mid_l)
    else
      # We've gone too far, move back toward the original L*
      direction == 'lighter' ? (high_l = mid_l) : (low_l = mid_l)
    end
  end

  best_lab.l
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
  FileUtils.mkdir_p '_site/h'

  out_path = "_site/h/#{tint_color.sub('#', '')}.png"

  return if File.file?(out_path)

  colors = get_colours_like(tint_color)
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
