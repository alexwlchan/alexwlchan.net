#!/usr/bin/env ruby

require "fileutils"
require "yaml"

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

# Escape a couple of characters I don't want to put into the title directly.
markdown_title =
  title
    .gsub("<", "&lt;")
    .gsub(">", "&gt;")

frontmatter = {
  "layout" => "post",
  "title" => markdown_title,
  "summary" => nil,
  "tags" => nil,
}

File.open(path, 'w') { |f| f.write(frontmatter.to_yaml + "---\n") }

finish(path)
