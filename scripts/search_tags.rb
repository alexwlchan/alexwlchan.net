#!/usr/bin/env ruby
# This is a small command-line tool that lets me search the
# tags on my blog posts.
#
# I use it when I'm writing new posts, and I want to see what
# tags I've used in the past.
#
# This requires fzf (https://github.com/junegunn/fzf) to work,
# which lets me search my tags.

require 'date'
require 'yaml'

tally = Hash.new(0)

Dir.glob('src/_posts/**/*.md') do |path|
  next if File.basename(path) == 'README.md'

  metadata = YAML.load_file(path, permitted_classes: [Date, Time])
  tags = metadata['tags']

  next if tags.nil?

  tags.each do |t|
    tally[t] += 1
  end
end

fzf_string = tally
             .sort_by { |t, _| t }
             .map { |t, count| "#{t} (#{count})" }
             .join("\n")

`echo "#{fzf_string}" | fzf`
