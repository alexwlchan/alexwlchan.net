# Make sure every test file is correctly sourced in this file.
Dir.glob('src/_tests/*.rb')
   .each do |f|
  name = File.basename(f, '.rb')

  if f == 'src/_tests/tests.rb'
    next
  end

  next if File.open('src/_tests/tests.rb').readlines.include? "require_relative '#{name}'\n"

  open('src/_tests/tests.rb', 'a') do |out_file|
    out_file.puts "require_relative '#{name}'\n"
  end
end

require_relative 'test_atom_feed_filters'
require_relative 'test_attrs'
require_relative 'test_filter_cleanup_text'
require_relative 'test_inline_styles'
require_relative 'test_picture'
require_relative 'test_pillow'
require_relative 'test_tag_tweet'
