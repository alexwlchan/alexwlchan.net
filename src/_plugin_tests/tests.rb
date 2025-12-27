# frozen_string_literal: true

# Make sure every test file is correctly sourced in this file.
Dir.glob('src/_plugin_tests/*.rb')
   .reject { |f| f == 'src/_plugin_tests/tests.rb' }
   .each do |f|
  name = File.basename(f, '.rb')

  next if File.open('src/_plugin_tests/tests.rb').readlines.include? "require_relative '#{name}'\n"

  open('src/_plugin_tests/tests.rb', 'a') do |out_file|
    out_file.puts "require_relative '#{name}'\n"
  end
end

require_relative 'test_add_utm_source'
require_relative 'test_atom_feed_filters'
require_relative 'test_attrs'
require_relative 'test_inline_styles'
require_relative 'test_picture_utils'
require_relative 'test_tag_tweet'
require_relative 'test_text_utils'
require_relative 'test_tint_colors'
