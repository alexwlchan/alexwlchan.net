#!/usr/bin/env ruby

require 'fileutils'
require 'json'
require 'shellwords'

require 'shell/executer'

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

        Shell.execute!("convert #{in_file} -resize #{resize} #{out_file}")
      end
    rescue ThreadError
    end
  end

  workers.map(&:join)
end
