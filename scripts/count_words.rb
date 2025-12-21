#!/usr/bin/env ruby
# Count the number of posts I've published each year.

require 'date'

def get_word_count(path)
  contents = File.read(path)

  md = contents.split('---', 3)[2]
  md = md.lines.map(&:strip).reject { |line| line.start_with?('>') }.join("\n")

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
  in_block_statement = 0

  char_sequences.each do |c|
    if ['{%', '<svg'].include?(c)
      in_block_statement += 1
      next
    end

    if ['%}', '</svg>'].include?(c)
      in_block_statement -= 1
      next
    end

    if in_block_statement.zero?
      words.push(c)
    end
  end

  words
end

def pprint_number(num, padding)
  num.to_s.gsub(/\B(?=(...)*\b)/, ',').rjust(padding)
end

Date.today.year

puts '             articles            TIL          total'
puts '====== ============== ============== =============='

(2012..Date.today.year).each do |year|
  article_words = Dir["src/_posts/#{year}/*.md"].map { |f| get_word_count(f) }
  til_words = Dir["src/_til/#{year}/*.md"].map { |f| get_word_count(f) }

  print "#{year}\t"

  print pprint_number(article_words.flatten.length, 7)
  print "(#{article_words.length})".rjust(6)

  print '   '

  print pprint_number(til_words.flatten.length, 6)
  print "(#{til_words.length})".rjust(6)

  print '   '

  print pprint_number(article_words.flatten.length + til_words.flatten.length, 6)
  print "(#{article_words.length + til_words.length})".rjust(6)

  puts
end

unless Dir['src/_drafts/*.md'].empty?
  draft_words = Dir['src/_drafts/*.md'].map { |f| get_word_count(f) }

  print "drafts\t"

  print pprint_number(draft_words.flatten.length, 7)
  print "(#{draft_words.length})".rjust(6)

  print '   '

  print '            '.rjust(6)

  print '   '

  print pprint_number(draft_words.flatten.length, 6)
  print "(#{draft_words.length})".rjust(6)

  puts
end

article_words = Dir['src/_posts/**/*.md'].map { |f| get_word_count(f) } + Dir['src/_drafts/*.md'].map do |f|
  get_word_count(f)
end
til_words = Dir['src/_til/**/*.md'].map { |f| get_word_count(f) }

puts '====== ============== ============== =============='

print 'TOTAL  '

print pprint_number(article_words.flatten.length, 8)
print "(#{article_words.length})".rjust(6)

print '  '

print pprint_number(til_words.flatten.length, 7)
print "(#{til_words.length})".rjust(6)

print '  '

print pprint_number(article_words.flatten.length + til_words.flatten.length, 6)
print "(#{article_words.length + til_words.length})".rjust(6)

puts
