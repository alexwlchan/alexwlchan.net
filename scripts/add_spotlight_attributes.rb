#!/usr/bin/env ruby

require 'English'
require 'date'
require 'open3'
require 'yaml'

def set_finder_comment(path)
  metadata = YAML.load_file(path, permitted_classes: [Date, Time])
  title = metadata['title']

  status = system('set_finder_comment', path, title)
  raise "Command failed with status #{$CHILD_STATUS.exitstatus}" unless status
end

Dir['src/_posts/**/*.md'].each { |p| set_finder_comment(p) }
Dir['src/_til/**/*.md'].each { |p| set_finder_comment(p) }
