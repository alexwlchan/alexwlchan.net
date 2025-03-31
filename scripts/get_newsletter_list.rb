#!/usr/bin/env ruby

require 'date'
require 'yaml'

def print_uri(path)
  metadata = YAML.load_file(path, permitted_classes: [Date, Time])
  title = metadata['title']
  slug = File.basename(path).gsub(/^[0-9]{4}-[0-9]{2}-[0-9]{2}-/, '').gsub(/\.md$/, '')
  year = File.basename(path).split('-')[0]

  if path.include? '_til'
    url = "https://alexwlchan.net/til/#{year}/#{slug}/"
  else
    url = "https://alexwlchan.net/#{year}/#{slug}/"
  end

  puts "* [#{title}](#{url})"
end

if ARGV.empty?
  yyyy_mm = Date.today.strftime('%Y-%m')
elsif ARGV.length == 1
  yyyy_mm = ARGV[0]
else
  puts 'Usage: get_newsletter_list.rb [<YYYY-MM>]'
  exit 1
end

puts '== Articles =='

Dir["src/_posts/**/#{yyyy_mm}*.md"].each { |p| print_uri(p) }

puts ''

puts '== Today I Learned =='

Dir["src/_til/**/#{yyyy_mm}*.md"].each { |p| print_uri(p) }
