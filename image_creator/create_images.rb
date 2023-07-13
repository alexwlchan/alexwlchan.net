#!/usr/bin/env ruby

require 'fileutils'
require 'json'
require 'shellwords'

require 'shell/executer'

# Returns true if an image has transparent pixels, false otherwise
def transparent_pixels?(path)
  output = `identify -format '%[opaque]' #{Shellwords.escape(path)}`.downcase

  case output
  when 'true' # the image is all opaque pixels => no transparent
    false
  when 'false' # the image is not all opaque pixels => some transparent
    true
  else
    raise "Unexpected output from identify: #{output.inspect}"
  end
end

if File.exist? '.missing_images.json'
  jobs = Queue.new

  File.readlines('.missing_images.json').uniq.each do |line|
    jobs.push(JSON.parse(line))
  end

  puts "Creating #{jobs.length} image#{jobs.length > 1 ? 's' : ''}..."

  workers = 5.times.map do
    Thread.new do
      while (this_job = jobs.pop(true))
        FileUtils.mkdir_p File.dirname(this_job['out_path'])

        resize = "#{this_job['width']}x#{this_job['height']}"
        in_file = Shellwords.escape(this_job['source_path'])
        out_file = Shellwords.escape(this_job['out_path'])

        Shell.execute("convert #{in_file} -resize #{resize} #{out_file}")

        # This is to detect an issue I had with ImageMagick and AVIF images;
        # I had ImageMagick 6.9.11 installed, which was incorrectly
        # changing the background of transparent PNGs to black.
        if transparent_pixels?(this_job['source_path']) && !transparent_pixels?(this_job['out_path'])
          File.delete(this_job['out_path'])
          raise "Source image #{this_job['source_path']} has transparency, but output image #{this_job['out_path']} doesn’t!"
        end
      end
    rescue ThreadError
    end
  end

  workers.map(&:join)
end
