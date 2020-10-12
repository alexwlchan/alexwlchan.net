#!/usr/bin/env ruby

require "fileutils"

unless ARGV.length <= 2
  puts "Usage: create_post.rb <TITLE> [<SLUG>]"
  exit 1
end

title = ARGV[0]

slug = if ARGV.length == 2
  ARGV[1]
else
  title
    .downcase
    .gsub(/[^a-z0-9]/, "-")
    .gsub(/\-{2,}/, "-")
    .chomp("-")
end

out_dir = File.join("src", "_drafts")
FileUtils.mkdir_p out_dir

path = File.join(out_dir, "#{slug}.md")

def finish(path)
  puts path
  `open #{path}`
  exit 0
end

if File.exist? path
  finish(path)
end

doc = "---\nlayout: post\ntitle: #{title}\nsummary: \ntags: \n---\n\n"
File.open(path, 'w') { |f| f.write(doc) }

finish(path)
