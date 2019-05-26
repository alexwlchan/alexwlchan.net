#!/usr/bin/env ruby

require "chunky_png"


def create_speckle(png, dimensions, colors)
  dimensions.zip(colors) { |dim, color|
    dim.map { |x, y|
      png[x, y] = color
    }
  }
end


def get_dimensions(dimension, cell_size)
  cell_boundaries = (0..dimension-1).each_slice(cell_size).to_a

  dimensions = []

  for x_cell in cell_boundaries
    for y_cell in cell_boundaries
      dimensions << x_cell.product(y_cell)
    end
  end

  dimensions
end


def draw_image(args)
  dimension = args[:dimension]
  cell_size = args[:cell_size]

  png = ChunkyPNG::Image.new(dimension, dimension)

  dimensions = get_dimensions(dimension, cell_size)

  if cell_size * 2 == dimension
    colors = [
      darken(ChunkyPNG::Color.from_hex("#d01c11")),
      ChunkyPNG::Color.from_hex("#d01c11"),
      ChunkyPNG::Color.from_hex("#d01c11"),
      darken(ChunkyPNG::Color.from_hex("#d01c11")),
    ]
  else
    colors = dimensions.map { |_|
      get_random_color_from(ChunkyPNG::Color.from_hex("#d01c11"))
    }
  end

  create_speckle(png, dimensions, colors)

  overlay = ChunkyPNG::Image.from_file("overlay_#{dimension}x#{dimension}.png")
  png.compose!(overlay, 0, 0)

  png
end


def darken(color)
  ChunkyPNG::Color.rgb(
    (ChunkyPNG::Color.r(color) * 0.85).to_i,
    (ChunkyPNG::Color.g(color) * 0.85).to_i,
    (ChunkyPNG::Color.b(color) * 0.85).to_i,
  )
end


def get_random_color_from(original, max_distance: 1000)
  red_min = [ChunkyPNG::Color.r(original) * 0.85, 0].max.to_i
  red_max = [ChunkyPNG::Color.r(original) * 1.1, 255].min.to_i

  green_min = [ChunkyPNG::Color.g(original) * 0.85, 0].max.to_i
  green_max = [ChunkyPNG::Color.g(original) * 1.1, 255].min.to_i

  blue_min = [ChunkyPNG::Color.b(original) * 0.85, 0].max.to_i
  blue_max = [ChunkyPNG::Color.b(original) * 1.1, 255].min.to_i

  while true
    new_color = ChunkyPNG::Color.rgb(
      rand(red_min..red_max),
      rand(green_min..green_max),
      rand(blue_min..blue_max)
    )

    if ChunkyPNG::Color.euclidean_distance_rgba(original, new_color) < max_distance
      return new_color
    end
  end
end

draw_image(dimension: 512, cell_size: 64).save("android-chrome-512x512.png")
draw_image(dimension: 192, cell_size: 32).save("android-chrome-192x192.png")
draw_image(dimension: 180, cell_size: 45).save("apple-touch-icon.png")
draw_image(dimension: 150, cell_size: 25).save("mstile-150x150.png")
draw_image(dimension: 32, cell_size: 16).save("favicon-32x32.png")
draw_image(dimension: 16, cell_size: 8).save("favicon-16x16.png")
