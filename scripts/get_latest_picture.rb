#!/usr/bin/env ruby
# This script creates a basic {% picture %} plugin tag for the
# newest image in the `_images` folder.
#
# It's meant for use in text expansion macros.
#
# I'm not currently using it, but I'm keeping it here as something
# I might want to reuse in future.

require 'date'

images_folder = "src/_images/#{Date.today.year}"

newest_filename, = Dir.entries(images_folder)
                      .select { |f| File.file?(File.join(images_folder, f)) }
                      .map { |f| [f, File.mtime(File.join(images_folder, f))] }
                      .max_by { |_f, mtime| mtime }

puts <<~MD
  {%
    picture
    filename="#{newest_filename}"
    width="750"
    alt=""
  %}
MD
