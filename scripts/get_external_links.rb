#!/usr/bin/env ruby

require 'nokogiri'

def get_all_links(html_dir)
  Dir["#{html_dir}/**/*.html"]
    .map { |path| Nokogiri::HTML(File.read(path)) }
    .flat_map { |html| html.css('a') }
    .map { |a| a[:href] }
    .compact
    .to_set
end

links = get_all_links('_site')
        .reject { |url| url.start_with?('/') }
        .reject { |url| url.start_with?('?') }
        .reject { |url| url.start_with?('javascript:') }
        .reject { |url| url.start_with?('mailto:') }
        .reject { |url| url.start_with?('https://alexwlchan.net/') }
        .reject { |url| url.start_with?('https://books.alexwlchan.net/') }
        .reject { |url| url.start_with?('https://github.com/alexwlchan/') }

puts links.inspect
puts links.size
