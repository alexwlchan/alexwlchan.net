#!/usr/bin/env ruby

require "chunky_png"





def draw_image(args)
  dimension = args[:dimension]
  cell_size = args[:cell_size]

  png = ChunkyPNG::Image.new(dimension, dimension)

  cell_boundaries = (0..dimension-1).each_slice(cell_size).to_a

  for x_cell in cell_boundaries
    for y_cell in cell_boundaries
      if x_cell[0] * y_cell[0] == 0 and (x_cell[0] != 0 or y_cell[0] != 0)
        color = ChunkyPNG::Color.from_hex("#d01c11")
      else
        color = darken(ChunkyPNG::Color.from_hex("#d01c11"))
      end


      # color = get_random_color_from(
      #   ChunkyPNG::Color.from_hex("#d01c11"),
      #   max_distance: 72
      # )

      for x in x_cell
        for y in y_cell
          png[x, y] = color
        end
      end
    end
  end

  overlay = ChunkyPNG::Image.from_file("overlay_#{dimension}x#{dimension}.png")
  png.compose!(overlay, 0, 0)

  png.save("favicon_#{dimension}.png")
end


def darken(color)
  ChunkyPNG::Color.rgb(
    (ChunkyPNG::Color.r(color) * 0.).to_i,
    (ChunkyPNG::Color.g(color) * 0.).to_i,
    (ChunkyPNG::Color.b(color) * 0.).to_i,
  )
end


def get_random_color_from(original, max_distance: 0)
  red_min = [ChunkyPNG::Color.r(original) * 0.9, 0].max.to_i
  red_max = [ChunkyPNG::Color.r(original) * 1.05, 255].min.to_i

  green_min = [ChunkyPNG::Color.g(original) * 0.9, 0].max.to_i
  green_max = [ChunkyPNG::Color.g(original) * 1.05, 255].min.to_i

  blue_min = [ChunkyPNG::Color.b(original) * 0.9, 0].max.to_i
  blue_max = [ChunkyPNG::Color.b(original) * 1.05, 255].min.to_i

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



draw_image(
  dimension: 32,
  cell_size: 16
)


def color_from_hex(hex_str)
  value = ChunkyPNG::Color.from_hex("#d01c11")
  get_random_color_from(value, max_distance: 16)
end

puts color_from_hex("#d01c11")






# for x in 0..15
#   for y in 0..15
#     png[x, y] = ChunkyPNG::Color.rgb(255, 0, 0)
#   end
#
#   for y in 16..31
#     png[x, y] = ChunkyPNG::Color.rgb(255, 128, 0)
#   end
# end
#
# for x in 16..31
#   for y in 16..31
#     png[x, y] = ChunkyPNG::Color.rgb(255, 0, 0)
#   end
#
#   for y in 0..15
#     png[x, y] = ChunkyPNG::Color.rgb(255, 128, 0)
#   end
# end
#
#
# png.compose!(overlay, 0, 0)
#
# png.save("favicon.png")