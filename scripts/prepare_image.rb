#!/usr/bin/env ruby

require 'fileutils'
require 'optparse'
require 'shellwords'



# Parse command-line arguments
#
# This returns a hash of options, describing the image to be processed --
# including the path to the original image, and the target width for resizing.
def parse_opts
  options = {
    :path => nil,
    :link_to_full_size => true,
    :target_width => nil,
  }

  OptionParser.new do |parser|
    parser.banner = "Usage: prepare_image.rb PATH [options]"

    parser.on("--width WIDTH", "The target width of the image on the page") { |o| options[:target_width] = o.to_i }
    parser.on("--nolink", "Don't link to a full-sized copy of the image") { |o| options[:link_to_full_size] = false }
  end.parse!

  if ARGV.length == 1
    options[:path] = ARGV[0]
  else
    STDERR.puts parser
    exit
  end

  profile = `exiftool -quiet -quiet -printFormat '$profileDescription' #{Shellwords.escape(options[:path])}`
  if profile != "" and profile != "sRGB"
    STDERR.puts "Unrecognised image profile: #{profile.inspect}"
    exit 1
  end

  options
end



# Returns the dimensions of an image as a width/height pair.
def get_dimensions(path)
  width = `identify -format '%[fx:w]' #{Shellwords.escape(path)}`.to_i
  height = `identify -format '%[fx:w]' #{Shellwords.escape(path)}`.to_i

  {:width => width, :height => height}
end



# Get some useful info about the file format
def get_format(path)
  case File.extname(path)
    when ".png"
      {:extension => ".png", :mime_type => "image/png", :label => "PNG"}
    when ".jpeg", ".jpg"
      {:extension => ".jpg", :mime_type => "image/jpeg", :label => "JPEG"}
    else
      STDERR.puts "Unrecognised image extension: #{File.extname(path)}"
      exit 1
  end
end



opts = parse_opts
dimensions = get_dimensions(opts[:path])

year = Time.new.year
name = File.basename(opts[:path], ".*")

im_format = get_format(opts[:path])

sources = Hash.new { [] }

puts "Creating alternative image sizes..."

for pixel_density in 1..4
  width = pixel_density * opts[:target_width]

  if dimensions[:width] >= width
    out_name = "#{name}_#{pixel_density}x#{im_format[:extension]}"
    out_path = "src/_images/#{year}/#{out_name}"
    `convert #{Shellwords.escape(opts[:path])} -resize #{width}x #{Shellwords.escape(out_path)}`
    `/Applications/ImageOptim.app/Contents/MacOS/ImageOptim #{Shellwords.escape(out_path)} >/dev/null 2>&1`

    sources[im_format[:mime_type]] <<= "/images/#{year}/#{out_name} #{pixel_density}x"

    webp_name = "#{name}_#{pixel_density}x.webp"
    webp_path = "src/_images/#{year}/#{webp_name}"
    `convert #{Shellwords.escape(opts[:path])} -resize #{width}x #{Shellwords.escape(webp_path)}`
    `/Applications/ImageOptim.app/Contents/MacOS/ImageOptim #{Shellwords.escape(webp_path)} >/dev/null 2>&1`

    sources["image/webp"] <<= "/images/#{year}/#{webp_name} #{pixel_density}x"
  end
end

inner_html = <<-EOF
<picture>
  <source
    srcset="#{sources["image/webp"].join(",\n            ")}"
    type="image/webp"
  >
  <source
    srcset="#{sources[im_format[:mime_type]].join(",\n            ")}"
    type="#{im_format[:mime_type]}"
  >
  <img
    src="#{sources[im_format[:mime_type]][0].gsub(" 1x", "")}"
  >
</picture>
EOF

if opts[:link_to_full_size]
  full_size_path = "src/_images/#{year}/#{File.basename(opts[:path])}"
  if File.realdirpath(opts[:path]) != File.realdirpath(full_size_path)
    FileUtils.cp(opts[:path], full_size_path)
  end

  puts <<-EOF
\e[0;35m<a href="/images/#{year}/#{File.basename(opts[:path])}">
#{inner_html.split("\n").map { |s| "  #{s}"}.join("\n")}
</a>\e[0m
  EOF
else
  puts <<-EOF

  \e[0;35m#{inner_html}\e[0m
  EOF
end


