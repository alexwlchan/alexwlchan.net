# frozen_string_literal: true

# Make sure every test file is correctly sourced in this file.
Dir.glob('tests/*.rb')
   .reject { |f| f == 'tests/run_all_tests.rb' }
   .reject { |f| f == 'tests/utils.rb' }
   .each do |f|
     name = File.basename(f, '.rb')

     next if File.open('tests/run_all_tests.rb').readlines.include? "require_relative '#{name}'\n"

     open('tests/run_all_tests.rb', 'a') do |out_file|
       out_file.puts "require_relative '#{name}'\n"
     end
end

require_relative 'test_site_is_up'
require_relative 'test_alternate_domains'
require_relative 'test_analytics'
require_relative 'test_http_security_headers'
require_relative 'test_https_certificate_expiry'
require_relative 'test_mastodon'
require_relative 'test_errors'
require_relative 'test_redirects'
