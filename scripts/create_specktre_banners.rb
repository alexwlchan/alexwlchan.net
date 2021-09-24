#!/usr/bin/env ruby
# You can set a theme colour for a page by setting keys in the YAML:
#
#     theme:
#       color: 531b93
#
# This includes a speckled image created using Specktre [1], which acts
# as the page header.  This script creates any header images required.
# This isn't included in the Jekyll Docker image because I add new images
# relatively infrequently, and keeping it as a separate process reduces
# the size of the Docker image.
#
# Tested with Specktre 0.2.0.
#
# [1]: https://github.com/alexwlchan/specktre
#

require "yaml"

Dir.glob("src/**/*.md") do |path|
  metadata = YAML.load_file(path)

  # If there isn't a theme color set on this page, there's nothing to do.
  color = metadata.fetch("theme", {}).fetch("color", nil)
  if color == nil
    next
  end

  # If the banner for this page already exists, there's nothing to do.
  banner_file = "src/theme/specktre_#{color}.png"
  if File.file?(banner_file)
    next
  end

  puts("Building the banner file for #{color} in #{path}")

  red   = (color.to_i(16) >> 16) % 256
  green = (color.to_i(16) >> 8) % 256
  blue  = (color.to_i(16) % 256)

  start_color = (
    red * 0.9 * 65536 +
    green * 0.9 * 256 +
    blue * 0.9).to_i()
  end_color = (
    [red * 1.05, 255].min.to_i() * 65536 +
    [green * 1.05, 255].min.to_i() * 256 +
    [blue * 1.05, 255].min.to_i())

  start_color = "%06x" % start_color
  end_color = "%06x" % end_color

  if !system("specktre new --size=3000x250 --start=#{start_color} --end=#{end_color} --squares --name=#{banner_file}")
    raise RuntimeError, "Error running the Specktre process for #{color}!"
  end

  if !system("optipng #{banner_file}")
    raise RuntimeError, "Error running optipng on #{banner_file}"
  end
end
