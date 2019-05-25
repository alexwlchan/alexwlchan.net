#!/usr/bin/env ruby

require "chunky_png"

png = ChunkyPNG::Image.new(32, 32, ChunkyPNG::Color::TRANSPARENT)

for x in 0..15
  for y in 0..15
    png[x, y] = ChunkyPNG::Color.rgb(255, 0, 0)
  end

  for y in 16..31
    png[x, y] = ChunkyPNG::Color.rgb(255, 128, 0)
  end
end

for x in 16..31
  for y in 16..31
    png[x, y] = ChunkyPNG::Color.rgb(255, 0, 0)
  end

  for y in 0..15
    png[x, y] = ChunkyPNG::Color.rgb(255, 128, 0)
  end
end

overlay = ChunkyPNG::Image.from_file("overlay_32x32.png")
png.compose!(overlay, 0, 0)

png.save("favicon.png")