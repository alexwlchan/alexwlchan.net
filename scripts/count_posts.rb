#!/usr/bin/env ruby
# Count the number of posts I've published each year.

require 'date'

Date.today.year

articles = 0
til = 0

puts '     articles      TIL    total'
puts '==== ======== ======== ========'

(2012..Date.today.year).each do |year|
  article_count = Dir["src/_posts/#{year}/*.md"].length
  til_count = Dir["src/_til/#{year}/*.md"].length

  puts "#{year}\t#{article_count.to_s.rjust(5)}\t#{til_count.to_s.rjust(6)}\t#{(article_count + til_count).to_s.rjust(7)}"

  articles += article_count
  til += til_count
end

puts '==== ======== ======== ========'
puts "    \t#{articles.to_s.rjust(5)}\t#{til.to_s.rjust(6)}\t#{(articles + til).to_s.rjust(7)}"
