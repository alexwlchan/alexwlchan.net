#!/usr/bin/env ruby
# Count the number of posts I've published each year.

require 'date'

def get_word_count(path)
  contents = File.read(path)

  md = contents.split('---', 3)[2]
  md = md.lines.reject { |line| line.start_with?('>') }.join

  char_sequences = md.scan(/\S+/)
                     .reject { |w| w == '-' }
                     .reject { |w| w == '--' }
                     .reject { |w| w == '---' }
                     .reject { |w| w == '–' }
                     .reject { |w| w == '{' }
                     .reject { |w| w == '}' }
                     .reject { |w| w == '=' }
                     .reject { |w| w == '*' }
                     .reject { |w| w == '#' }
                     .reject { |w| w == '##' }
                     .reject { |w| w.start_with? '```' }

  words = []
  in_liquid_statement = false

  char_sequences.each do |c|
    if c == '{%'
      in_liquid_statement = true
      next
    end

    if c == '%}'
      in_liquid_statement = false
      next
    end

    unless in_liquid_statement
      words.push(c)
    end
  end

  words
end

def pprint_number(num)
  num.to_s.gsub(/\B(?=(...)*\b)/, ',').rjust(6)
end

Date.today.year

puts '            articles             TIL           total'
puts '==== =============== =============== ==============='

(2012..Date.today.year).each do |year|
  article_words = Dir["src/_posts/#{year}/*.md"].map { |f| get_word_count(f) }
  til_words = Dir["src/_til/#{year}/*.md"].map { |f| get_word_count(f) }

  print "#{year}\t"

  print pprint_number(article_words.flatten.length)
  print "(#{article_words.length})".rjust(5)

  print "\t"

  print pprint_number(til_words.flatten.length)
  print "(#{til_words.length})".rjust(6)

  print "\t"

  print pprint_number(article_words.flatten.length + til_words.flatten.length)
  print "(#{article_words.length + til_words.length})".rjust(6)

  puts
end

#
#   puts "#{article_count.to_s.rjust(5)}\t#{til_count.to_s.rjust(6)}\t#{(article_count + til_count).to_s.rjust(7)}"
#
#   articles += article_count
#   til += til_count
# end
#
# puts '==== ======== ======== ========'
# puts "    \t#{articles.to_s.rjust(5)}\t#{til.to_s.rjust(6)}\t#{(articles + til).to_s.rjust(7)}"
