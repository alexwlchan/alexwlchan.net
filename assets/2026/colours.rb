require 'chunky_png'
require 'color'

# Given a given hex colour as a string (e.g. '#123456') generate
# an infinite sequence of colours which vary only in brightness.
def get_hsl_colours_like(hex)
  # Seed the random to get consistent outputs
  # seeded_random = Random.new(hex[1..].to_i(16))

  # Convert the colour to the HSL colour space
  hsl = Color::RGB.by_hex(hex).to_hsl

  # Establish the range of luminosity (or lightness) to vary within
  luminosity = hsl.luminosity

  min_luminosity = luminosity * 7 / 8
  max_luminosity = luminosity * 8 / 7
  luminosity_diff = max_luminosity - min_luminosity

  # Repeatedly generate colours with the same hue and saturation, but
  # with luminosity between (min_luminosity..max_luminosity).
  Enumerator.new do |enum|
    loop do
      new_hsl = Color::HSL.from_values(
        hsl.hue,
        hsl.saturation,
        min_luminosity + (Random.rand * luminosity_diff)
      )
      enum.yield new_hsl.to_rgb
    end
  end
end

def get_lab_colours_like(hex, _clamped)
  seeded_random = Random.new(hex[1..].to_i(16))

  lab = Color::RGB.by_hex(hex).to_lab

  min_lightness = lightness_at_distance(lab, 'darker',  5)
  max_lightness = lightness_at_distance(lab, 'lighter', 5)
  lightness_diff = max_lightness - min_lightness

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

# Find the perceptual lightness of a CIELAB colour that's a specific
# perceptual difference (target_distance) from the original colour, while
# maintaining the original hue and colourfulness.
def lightness_at_distance(original_lab, direction, target_distance)
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
    if (candidate_delta - target_distance).abs < (best_delta - target_distance).abs
      best_lab = candidate_lab
      best_delta = candidate_delta
    end

    if candidate_delta < target_distance
      # We need more distance, move away from the original L*
      direction == 'lighter' ? (low_l = mid_l) : (high_l = mid_l)
    else
      # We've gone too far, move back toward the original L*
      direction == 'lighter' ? (high_l = mid_l) : (low_l = mid_l)
    end
  end

  best_lab.l
end

def create_header_image(tint_color)
  # return if File.file?(out_path)

  hsl_colors = get_hsl_colours_like(tint_color)
  lab_colors = get_lab_colours_like(tint_color, true)
  squares1 = squares_for(400, 400, 50)

  image = ChunkyPNG::Image.new(400, 400)

  squares1.each do |rect|
    x0, y0, x1, y1 = rect

    if [0, 50, 100].include?(y0)
      # puts "hsl"
      color = hsl_colors.next
    elsif [150, 200].include?(y0)
      #   # puts "fixed"
      color = Color::RGB.by_hex(tint_color)
    else
      # puts "lab"
      color = lab_colors.next
    end

    # puts color

    image.rect(
      x0, y0, x1, y1,
      ChunkyPNG::Color.rgba(0, 0, 0, 0),
      ChunkyPNG::Color.rgb(
        color.red.to_i,
        color.green.to_i,
        color.blue.to_i
      )
      # color
    )
  end

  image.save("#{tint_color.sub('#', '')}_combo.png", :best_compression)
end

create_header_image('#101c75')
create_header_image('#4b4b4b')
create_header_image('#470906')
create_header_image('#d01c11')
create_header_image('#f69b96')
