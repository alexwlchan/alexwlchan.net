#!/usr/bin/env ruby

require 'date'

images_folder = "src/_images/#{Date.today.year}"

newest_filename, _ = Dir.entries(images_folder)
  .select { |f| File.file?(File.join(images_folder, f)) }
  .map { |f| [f, File.mtime(File.join(images_folder, f))]}
  .max_by { |f, mtime| mtime }

puts <<~EOF
{%
  picture
  filename="#{newest_filename}"
  width="750"
  alt=""
%}
EOF
